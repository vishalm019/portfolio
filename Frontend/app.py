import streamlit as st
import requests
import pandas as pd

st.title("My Portfolio dashboard")

res = requests.get("http://127.0.0.1:5000/get_projects")

if res.status_code == 200:
    projects = res.json()["details"]
    df = pd.DataFrame(projects)
    st.subheader("Project")
    st.dataframe(df)