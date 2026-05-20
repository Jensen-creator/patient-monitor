import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Patient Database Platform", layout="wide")

st.title("🏥 Patient Monitoring Database")

# connect to database
conn = sqlite3.connect("patients.db")

# load data
df = pd.read_sql_query("SELECT * FROM vitals ORDER BY id DESC", conn)

conn.close()

# -------------------------
# SEARCH SECTION
# -------------------------
st.sidebar.header("Search Filters")

patient_id_filter = st.sidebar.text_input("Search Patient ID")
min_spo2 = st.sidebar.number_input("Min SpO2", 0, 100, 0)

# apply filters
if patient_id_filter:
    df = df[df["patient_id"].astype(str).str.contains(patient_id_filter)]

df = df[df["spo2"] >= min_spo2]

# -------------------------
# SUMMARY STATS
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Unique Patients", df["patient_id"].nunique())
col3.metric("Avg SpO2", round(df["spo2"].mean(), 1) if len(df) > 0 else 0)

# -------------------------
# DATA TABLE
# -------------------------
st.subheader("Patient Records")

st.dataframe(df, use_container_width=True)

# -------------------------
# SELECT PATIENT DETAIL VIEW
# -------------------------
st.subheader("Patient Detail Viewer")

selected_patient = st.selectbox("Select Patient ID", df["patient_id"].unique() if len(df) > 0 else [])

if selected_patient:
    patient_df = df[df["patient_id"] == selected_patient]

    st.write("Latest Readings")
    st.dataframe(patient_df)

    st.line_chart(patient_df[["spo2"]])