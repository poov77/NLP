import os
import io
import base64
import streamlit as st
from groq import Groq

# ==========================================
# 1. GEMINI DESIGN STYLING & CORE CONFIGS
# ==========================================
st.set_page_config(page_title="Gemini Audio Workspace", page_icon="✨", layout="wide")

# Inject Gemini UI modern dark workspace styling variables
st.markdown("""
<style>
    /* Main Background Base Overhaul */
    .stApp {
        background-color: #0F111A !important;
        color: #E3E2E6 !important;
    }
    
    /* Top Navigation Header Header Styles */
    .gemini-header {
        font-family: 'Google Sans', 'Inter', sans-serif;
        font-weight: 500;
        background: linear-gradient(90deg, #4285F4 0%, #9B51E0 50%, #E91E63 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
    }
    
    .gemini-subtitle {
        color: #8E918F;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Minimal Gemini Card Wrapper Layouts */
    div[data-testid="stVerticalBlock"] > div:has(div.gemini-card) {
        background: #1E202A;
        border: 1px solid #2A2D3D;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    
    .panel-title {
        font-size: 1.15rem;
        font-weight: 500;
        color: #C4C7C5;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Main Application Title Context Display
st.markdown('<h1 class="gemini-header">✨ Gemini Audio Workspace</h1>', unsafe_allow_html=True)
st.markdown('<p class="gemini-subtitle">Superfast Multilingual Transcription & Note-taking Intelligence</p>', unsafe_allow_html=True)

# Load Groq API key from environment variable
if not os.getenv("GROQ_API_KEY"):
    st.error("❌ GROQ_API_KEY environment variable is not set. Please configure it in your .env file.")

@st.cache_resource
def init_groq():
    return Groq()

client = init_groq()

# Manage persistent variables across app streams
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "notes" not in st.session_state:
    st.session_state.notes = "*No notes generated yet. Speak using the hardware terminal control orb panel.*"

# ==========================================
# 2. SIDEBAR WORKSPACE SIDEBAR OPTIONS
# ==========================================
st.sidebar.markdown("### ⚙️ Workspace Configuration")

# User language dropdown feature selector matrix 
target_language = st.sidebar.selectbox(
    "Translate & Structure Into:",
    ["English", "Tamil", "Hindi", "Spanish", "French", "German", "Japanese", "Telugu", "Kannada"],
    index=0
)

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Active Session Data", use_container_width=True):
    st.session_state.transcript = ""
    st.session_state.notes = "*No notes generated yet. Speak using the hardware terminal control orb panel.*"
    st.rerun()

# ==========================================
# 3. HIGH-SPEED DUAL AGENT AI PIPELINES
# ==========================================
def transcribe_audio_file(audio_bytes):
    """Sends audio bytes safely to the Groq Whisper API endpoint."""
    try:
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        return client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            response_format="text"
        )
    except Exception as e:
        return f"[Transcription Error: {str(e)}]"

def compile_structured_notes(full_text, language):
    """Structures raw transcripts using the high-speed instant deployment model configuration."""
    system_prompt = f"""
    You are an expert technical note-taker and master linguist translator. 
    Your mission is to parse the raw transcript text, translate it accurately, and organize it into the target language: '{language}'.
    
    Format the complete output in '{language}' using exactly these sections:
    ### 🎯 Key Takeaways
    (Bullet points tracking core items discussed)
    
    ### ⚡ Action Items
    (Actionable assignments extracted from context statements)
    
    ### ❓ Follow-up Questions
    (Points left open or needing verification)
    
    Make your execution snappy and omit conversation filler notes. Respond strictly in the script/language requested.
    """
    try:
        # Utilizing the lightning fast instant architecture iteration pipeline
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_text}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Formatting pipeline speed drop error: {str(e)}"

# ==========================================
# 4. INTUITIVE JS MICROPHONE AUDIO ORB CONTROL
# ==========================================
def render_gemini_orb():
    """Renders a pulsing circular audio terminal orb component context layout frame."""
    custom_html = """
    <div style="background: #1E202A; border: 1px solid #2A2D3D; padding: 25px; border-radius: 16px; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        
        <div id="orb-box" style="position: relative; width: 110px; height: 110px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center;">
            <div id="core-orb" class="orb-idle"></div>
            <div id="glow-layer"></div>
        </div>

        <div style="display: flex; gap: 12px; margin-bottom: 10px;">
            <button id="startRec" style="background: #1A73E8; color: white; border: none; padding: 10px 24px; font-weight: 500; font-size: 14px; border-radius: 24px; cursor: pointer; transition: background 0.2s;">🎙️ Start Recording</button>
            <button id="stopRec" style="background: #E8EAED; color: #3C4043; border: none; padding: 10px 24px; font-weight: 500; font-size: 14px; border-radius: 24px; cursor: pointer;" disabled>🛑 Stop & Process</button>
        </div>
        <p id="label" style="color: #8E918F; font-size: 12px; font-weight: 500; margin: 5px 0 0 0; letter-spacing: 0.05em;">READY</p>
    </div>

    <style>
        #core-orb {
            width: 75px;
            height: 75px;
            border-radius: 50%;
            position: absolute;
            z-index: 2;
            transition: all 0.4s ease;
        }
        #glow-layer {
            width: 85px;
            height: 85px;
            border-radius: 50%;
            position: absolute;
            z-index: 1;
            filter: blur(20px);
            opacity: 0.5;
            transition: all 0.4s ease;
        }
        .orb-idle {
            background: radial-gradient(circle at 30% 30%, #4285F4, #174EA6);
            animation: floating 3s infinite ease-in-out;
        }
        .orb-idle + #glow-layer { background: #4285F4; }
        
        .orb-rec {
            background: radial-gradient(circle at 30% 30%, #A569BD, #E91E63) !important;
            animation: pulsing 1s infinite ease-in-out !important;
            transform: scale(1.08);
        }
        .orb-rec + #glow-layer { background: #E91E63; filter: blur(25px); opacity: 0.8; }

        @keyframes floating {
            0% { transform: scale(1); }
            50% { transform: scale(1.04); }
            100% { transform: scale(1); }
        }
        @keyframes pulsing {
            0% { transform: scale(1); opacity: 0.9; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); opacity: 0.9; }
        }
        button:hover:not([disabled]) { filter: brightness(0.95); }
        button:disabled { background: #3C4043 !important; color: #80868B !important; cursor: not-allowed; }
    </style>

    <script>
        let recorder;
        let pieces = [];
        const start = document.getElementById('startRec');
        const stop = document.getElementById('stopRec');
        const lbl = document.getElementById('label');
        const orb = document.getElementById('core-orb');

        start.onclick = async () => {
            pieces = [];
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                recorder = new MediaRecorder(stream);
                recorder.ondataavailable = e => { pieces.push(e.data); };
                recorder.onstop = async () => {
                    const blob = new Blob(pieces, { type: 'audio/wav' });
                    const rdr = new FileReader();
                    rdr.readAsDataURL(blob);
                    rdr.onloadend = () => {
                        const b64 = rdr.result.split(',')[1];
                        window.parent.postMessage({
                            type: 'streamlit:setComponentValue',
                            value: b64
                        }, '*');
                    };
                    lbl.innerText = "PROCESSING OVER VIEW MATRIX...";
                    orb.className = "orb-idle";
                };
                recorder.start();
                start.disabled = true;
                stop.disabled = false;
                lbl.innerText = "LISTENING LIVE FEED...";
                orb.className = "orb-rec";
            } catch (err) {
                lbl.innerText = "ERROR: CAPTURE NOT ACTIVE";
            }
        };

        stop.onclick = () => {
            recorder.stop();
            recorder.stream.getTracks().forEach(t => t.stop());
            start.disabled = false;
            stop.disabled = true;
            lbl.innerText = "COMPILING DATA STREAM...";
        };
    </script>
    """
    st.components.v1.html(custom_html, height=210)

# ==========================================
# 5. DUAL CARD GRID WORKSPACE ENGINE
# ==========================================
col_ui, col_doc = st.columns([4, 5], gap="medium")

with col_ui:
    st.markdown('<div class="gemini-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🎙️ Capture Engine Interface</div>', unsafe_allow_html=True)
    
    # Mount live voice handler component
    render_gemini_orb()
    
    # Securely retrieve raw Base64 data strings out of embedded custom objects
    captured_stream = st.text_input("Stream Target", label_visibility="collapsed")
    
    if captured_stream and st.session_state.transcript == "":
        with st.spinner("Processing lightning-fast execution sequence arrays..."):
            audio_data_bytes = base64.b64decode(captured_stream)
            raw_transcription = transcribe_audio_file(audio_data_bytes)
            
            if raw_transcription.strip() and not raw_transcription.startswith("["):
                st.session_state.transcript = raw_transcription
                st.session_state.notes = compile_structured_notes(st.session_state.transcript, target_language)
                st.rerun()
                
    st.markdown('<div class="panel-title" style="margin-top: 24px;">📝 Active Rolling Transcript</div>', unsafe_allow_html=True)
    if st.session_state.transcript:
        st.info(st.session_state.transcript)
    else:
        st.caption("_Voice text transcription updates will render instantly here..._")
    st.markdown('</div>', unsafe_allow_html=True)

with col_doc:
    st.markdown('<div class="gemini-card" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">📋 Document Summary ({target_language})</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(st.session_state.notes)
    st.markdown('</div>', unsafe_allow_html=True)