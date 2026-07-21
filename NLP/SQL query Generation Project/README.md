# 📊 Natural Language Text-to-SQL Analytics Engine

An interactive, AI-powered data analytics platform built with Streamlit, SQLAlchemy, and Groq's high-speed Llama models. This application allows users to upload custom CSV datasets, type plain English queries, and instantly receive executed SQL queries, structured tabular results, and dynamic data visualizations.

---

## ✨ Features

- **📁 Custom CSV Upload**: Upload any structured `.csv` file and automatically infer its schema in real-time.
- **🤖 Natural Language to SQL**: Converts plain English commands into strict, read-only SQLite queries using `llama-3.3-70b-versatile` / `llama-3.1-8b-instant`.
- **🛡️ Built-in Security Guardrails**: Sanitizes generated queries to prevent destructive SQL actions (`DROP`, `DELETE`, `UPDATE`, `ALTER`).
- **⚡ In-Memory Sandbox**: Executes queries safely inside an isolated SQLite memory database engine using SQLAlchemy.
- **📈 Dynamic Auto-Visualization**: Automatically detects numerical and categorical columns to generate bar charts and plots on the fly using Matplotlib and Streamlit.

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: Streamlit
- **LLM Engine**: Groq API (`llama-3.3-70b-versatile` / `llama-3.1-8b-instant`)
- **Database Sandbox**: SQLAlchemy, SQLite (In-Memory)
- **Data Manipulation & Plotting**: Pandas, Matplotlib
- **Language**: Python 3.9+

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python installed on your system.

### 2. Install Dependencies

```bash
pip install streamlit pandas sqlalchemy groq matplotlib


<img width="1858" height="853" alt="image" src="https://github.com/user-attachments/assets/55504d56-be8c-4389-bd59-20924fae0823" />
<img width="1877" height="852" alt="image" src="https://github.com/user-attachments/assets/8090a4e1-01f6-48d9-a39f-28f650c851ca" />
