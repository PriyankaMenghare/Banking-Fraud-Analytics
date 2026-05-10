from databricks import sql
import pandas as pd
import os
import streamlit as st

def get_connection():
    try:
        host = st.secrets["DATABRICKS_HOST"]
        http_path = st.secrets["DATABRICKS_HTTP_PATH"]
        token = st.secrets["DATABRICKS_TOKEN"]
    except Exception:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path='../.env')
        host = os.getenv("DATABRICKS_HOST")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        token = os.getenv("DATABRICKS_TOKEN")

    if not all([host, http_path, token]):
        st.error("⚠️ Missing Databricks credentials. Check your .env file or Streamlit secrets.")
        st.stop()

    return sql.connect(
        server_hostname=host,
        http_path=http_path,
        access_token=token,
        use_cloud_fetch=False
    )

@st.cache_data(ttl=3600, show_spinner=False)
def run_query(query: str) -> pd.DataFrame | None:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(result, columns=columns)
    except Exception as e:
        st.error(f"⚠️ Query failed: {str(e)}")
        return None