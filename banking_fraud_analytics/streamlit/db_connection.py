from databricks import sql
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv(dotenv_path='../.env')

def get_connection():
    return sql.connect(
        server_hostname=os.getenv("DATABRICKS_HOST"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN"),
        use_cloud_fetch=False
    )
# Optimized - graceful error handling
@st.cache_data(ttl=3600, show_spinner=False)
def run_query(query):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(result, columns=columns)
    except Exception as e:
        st.error(f"⚠️ Database connection error: {str(e)}")
        return None