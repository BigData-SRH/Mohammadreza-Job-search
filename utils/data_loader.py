# utils/data_loader.py
import streamlit as st
import pandas as pd
import os
import json

def download_kaggle_dataset():
    """
    Download dataset from Kaggle using API credentials from Streamlit secrets.
    Falls back to local file if already exists.
    """
    dataset_path = 'data/ai_job_dataset.csv'

    # If file already exists locally, use it
    if os.path.exists(dataset_path):
        return dataset_path

    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    try:
        # Try to use Streamlit secrets (works on Streamlit Cloud)
        if hasattr(st, 'secrets') and 'kaggle' in st.secrets:
            # Set up kaggle credentials
            os.environ['KAGGLE_USERNAME'] = st.secrets['kaggle']['username']
            os.environ['KAGGLE_KEY'] = st.secrets['kaggle']['key']

            # Import kaggle library
            from kaggle.api.kaggle_api_extended import KaggleApi

            # Download dataset
            api = KaggleApi()
            api.authenticate()

            # Download the specific dataset
            # Replace with your actual Kaggle dataset identifier
            api.dataset_download_files(
                'pratyushpuri/global-ai-job-market-trend-2025',
                path='data/',
                unzip=True
            )

            return dataset_path
        else:
            raise Exception("Kaggle credentials not found in secrets")

    except Exception as e:
        st.error(f"Could not download dataset from Kaggle: {e}")
        st.info("Please ensure the dataset file is available in the data/ directory")
        return None

@st.cache_data(ttl=3600)
def load_dataset():
    """
    Load the AI job dataset with caching.
    """
    try:
        # First, try to ensure dataset is available
        dataset_path = download_kaggle_dataset()

        if dataset_path and os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
            df['salary_usd'] = pd.to_numeric(df['salary_usd'], errors='coerce')
            df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce')
            df = df.dropna(subset=['salary_usd', 'posting_date'])

            # Add work_type categorization
            def categorize_work_type(ratio):
                if pd.isna(ratio):
                    return 'Unknown'
                if ratio == 0:
                    return 'On-site'
                elif ratio == 100:
                    return 'Remote'
                else:
                    return 'Hybrid'

            if 'remote_ratio' in df.columns:
                df['work_type'] = df['remote_ratio'].apply(categorize_work_type)
            else:
                df['work_type'] = 'Unknown'

            return df
        else:
            st.error("Dataset file not found at data/ai_job_dataset.csv")
            return None

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None
