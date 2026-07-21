import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
from groq import Groq

# ==========================================
# 1. SETUP PAGE STYLING & LLM CLIENT
# ==========================================
st.set_page_config(
    page_title="Natural Language Data Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Natural Language Data Analytics Engine")
st.markdown("Upload any CSV dataset, type a plain English query, and let the AI generate the SQL code and visualize your results instantly.")

# Load Groq API key from environment variable
if not os.getenv("GROQ_API_KEY"):
    st.error("❌ GROQ_API_KEY environment variable is not set. Please configure it in your .env file.")

@st.cache_resource
def get_groq_client():
    return Groq()

client = get_groq_client()

# ==========================================
# 2. SCHEMA AND TRANSLATION AGENT LOGIC
# ==========================================
def extract_dataframe_schema(df: pd.DataFrame) -> str:
    """Analyzes the DataFrame to construct a text-to-SQL schema layout."""
    schema_parts = ["Table: user_dataset", "Columns:"]
    for col, dtype in zip(df.columns, df.dtypes):
        sql_type = "TEXT"
        if pd.api.types.is_numeric_dtype(dtype):
            sql_type = "REAL" if pd.api.types.is_float_dtype(dtype) else "INTEGER"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            sql_type = "DATETIME"
        schema_parts.append(f"  - {col} ({sql_type})")
    return "\n".join(schema_parts)

def generate_sql_query(user_question: str, schema_context: str) -> str:
    """Uses Groq's Llama model to compile natural text into an explicit SQLite instruction."""
    system_instruction = f"""
    You are an expert Text-to-SQL compiler engine.
    Translate the user's plain English request into clean SQLite code targeting the 'user_dataset' table ONLY.
    
    Database Schema Layout:
    {schema_context}
    
    Rules for output:
    1. Output ONLY the raw executable SQL query string. Do not include markdown formatting, backticks, or text explanations.
    2. Always use explicit columns or expressions matching the given schema columns.
    3. Make sure all queries are highly efficient read-only SELECT statements.
    4. If column names contain empty spaces or special characters, wrap them in square brackets like [Column Name].
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_question}
            ],
            temperature=0.0
        )
        raw_sql = response.choices[0].message.content.strip()
        
        # Clean up any rogue formatting wrappers the LLM might have returned
        if raw_sql.startswith("```"):
            lines = raw_sql.splitlines()
            cleaned_lines = [line for line in lines if not line.startswith("```")]
            raw_sql = " ".join(cleaned_lines).strip()
        if raw_sql.startswith("sql"):
            raw_sql = raw_sql[3:].strip()
        if raw_sql.startswith("[") and raw_sql.endswith("]"):
            raw_sql = raw_sql[1:-1].strip()
            
        return raw_sql
    except Exception as e:
        return f"Error: LLM Processing error occurred: {str(e)}"

def validate_sql_security(sql_query: str) -> tuple[bool, str]:
    """Ensures incoming generated code strictly adheres to read-only queries."""
    upper_query = sql_query.upper()
    if "ERROR:" in upper_query:
        return False, sql_query
        
    destructive_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'GRANT']
    for word in destructive_keywords:
        if word in upper_query:
            return False, f"Security Refusal: Destructive operational keyword '{word}' is strictly forbidden."
            
    if not upper_query.strip().startswith("SELECT"):
        return False, "Security Refusal: Executable syntax statement violates read-only SELECT requirements."
        
    return True, "Passed"

# ==========================================
# 3. INTERACTIVE WEB INTERFACE LAYOUT
# ==========================================
st.sidebar.header("📁 Step A: Data Source Loading")
uploaded_file = st.sidebar.file_uploader("Upload your data matrix (CSV format)", type=["csv"])

if uploaded_file is not None:
    # Read CSV file directly into memory
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded '{uploaded_file.name}' successfully!")
    
    # Create the internal temporary SQLite connection engine
    db_engine = create_engine('sqlite:///:memory:')
    df.to_sql('user_dataset', db_engine, index=False, if_exists='replace')
    
    # Process custom schema block dynamically
    detected_schema = extract_dataframe_schema(df)
    
    with st.sidebar.expander("🔍 View Detected Schema Layout"):
        st.code(detected_schema, language="text")
        
    # Main Dashboard Window Elements
    st.subheader("💬 Step B: Converse Natural Commands")
    
    # Input panel and execution controls
    user_command = st.text_input(
        label="Ask your dataset a question or issue a calculation directive:",
        value="Show me total sales revenue grouped by region",
        placeholder="e.g., Show me the average production sorted by year"
    )
    
    if st.button("Process Query", type="primary"):
        if not user_command.strip():
            st.warning("Please enter a valid command phrase statement first.")
        else:
            with st.spinner("🧠 Step 1: Parsing user instruction logic..."):
                generated_query = generate_sql_query(user_command, detected_schema)
                
            # Security verification
            is_safe, security_msg = validate_sql_security(generated_query)
            
            if not is_safe:
                st.error(f"❌ Guardrail Exception: {security_msg}")
            else:
                st.info("🤖 **Step 2: Formulated Target Query Statement**")
                st.code(generated_query, language="sql")
                
                # Execute the code against the database sandbox
                st.success("📊 **Step 3: Running inside dataset sandbox engine layer...**")
                try:
                    with db_engine.connect() as conn:
                        result_df = pd.read_sql_query(text(generated_query), conn)
                    
                    st.write("### 🎉 Execution Outcome Complete! Result Rows:")
                    st.dataframe(result_df, use_container_width=True)
                    
                    # Automated visual rendering suite
                    if not result_df.empty and len(result_df.columns) >= 2:
                        numeric_cols = result_df.select_dtypes(include=['number']).columns
                        object_cols = result_df.select_dtypes(exclude=['number']).columns
                        
                        if len(numeric_cols) > 0 and len(object_cols) > 0:
                            st.write("### 📈 Automated Chart Visualization")
                            fig, ax = plt.subplots(figsize=(10, 4.5))
                            
                            ax.bar(result_df[object_cols[0]].astype(str), result_df[numeric_cols[0]], color='#008080')
                            ax.set_title(f"Visualized: {numeric_cols[0]} relative to {object_cols[0]} values", fontsize=12, pad=15)
                            ax.set_ylabel(numeric_cols[0])
                            ax.set_xlabel(object_cols[0])
                            plt.xticks(rotation=30, ha='right')
                            plt.tight_layout()
                            
                            st.pyplot(fig)
                            
                except Exception as db_err:
                    st.error("❌ Execution Failure: The query syntax generated broken database logic.")
                    st.caption(f"**Error Details:** {str(db_err)}")
else:
    # Landing page state warning notification display
    st.info("💡 Get started by uploading a valid `.csv` data table via the left sidebar panel.")