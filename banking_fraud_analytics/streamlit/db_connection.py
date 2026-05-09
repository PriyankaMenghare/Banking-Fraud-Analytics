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
@st.cache_data(ttl=3600)   # cache for 1 hour
def run_query(query):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=columns)