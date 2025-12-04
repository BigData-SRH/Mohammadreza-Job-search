# pages/02_Search_Jobs.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Search Jobs", page_icon="🔍", layout="wide")

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'  # Default to light theme
if 'default_currency' not in st.session_state:
    st.session_state.default_currency = 'USD'
if 'currency_rates' not in st.session_state:
    st.session_state.currency_rates = {}
if 'last_rate_update' not in st.session_state:
    st.session_state.last_rate_update = None

# Unified theme application
def apply_theme():
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .main {
            background-color: #0e1117;
        }
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
            color: #fafafa !important;
        }
        .stTextInput label, .stSelectbox label, .stMultiSelect label, .stNumberInput label {
            color: #fafafa !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #31333F;
        }
        .main {
            background-color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
            color: #31333F !important;
        }
        .stTextInput label, .stSelectbox label, .stMultiSelect label, .stNumberInput label {
            color: #31333F !important;
        }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# Fetch currency rates
@st.cache_data(ttl=3600)
def fetch_currency_rates():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['rates']
        else:
            raise Exception("API request failed")
    except:
        return {
            'USD': 1.0,
            'EUR': 0.92,
            'GBP': 0.79,
            'CAD': 1.39,
            'AUD': 1.54,
            'INR': 83.12,
            'JPY': 149.50
        }

if not st.session_state.currency_rates or not st.session_state.last_rate_update or \
   (datetime.now() - st.session_state.last_rate_update) > timedelta(hours=1):
    st.session_state.currency_rates = fetch_currency_rates()
    st.session_state.last_rate_update = datetime.now()

CURRENCY_RATES = st.session_state.currency_rates

def convert_to_target_currency(amount_usd, target_currency='USD'):
    if target_currency == 'USD':
        return amount_usd
    return amount_usd * CURRENCY_RATES.get(target_currency, 1.0)

# Load real data from CSV
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/ai_job_dataset.csv')
        
        # Convert salary_usd to numeric
        df['salary_usd'] = pd.to_numeric(df['salary_usd'], errors='coerce')
        
        # Parse dates
        df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce')
        
        # Handle missing values
        df = df.dropna(subset=['salary_usd', 'posting_date'])
        
        return df
    except FileNotFoundError:
        st.error("Dataset file not found at data/ai_job_dataset.csv")
        return None

df = load_data()

if df is None:
    st.stop()

# Theme toggle in the sidebar
with st.sidebar:
    st.markdown("### ⚙️ Display Settings")
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("🌙 Dark", use_container_width=True, 
                    disabled=(st.session_state.theme == 'dark')):
            st.session_state.theme = 'dark'
            st.rerun()
    with theme_col2:
        if st.button("☀️ Light", use_container_width=True,
                    disabled=(st.session_state.theme == 'light')):
            st.session_state.theme = 'light'
            st.rerun()
    st.markdown("---")

st.title("🔍 Search & Filter Jobs")
st.markdown("Find AI/ML jobs that match your criteria")

target_currency = st.session_state.default_currency
df['salary_target'] = df['salary_usd'].apply(lambda x: convert_to_target_currency(x, target_currency))

# Sidebar filters
st.sidebar.header("🔧 Filters")

# Mapping dictionaries
experience_level_map = {
    'EN': 'Entry',
    'MI': 'Mid',
    'SE': 'Senior',
    'CT': 'Contract',
    'FL': 'Freelance',
    'EX': 'Executive',
    # Add more if needed
}
employment_type_map = {
    'FT': 'Full-Time',
    'PT': 'Part-Time',
    'CT': 'Contract',
    'FL': 'Freelance',
    # Add more if needed
}
company_size_map = {
    'S': 'Small',
    'M': 'Medium',
    'L': 'Large',
    'E': 'Enterprise',
    # Add more if needed
}

# Experience Level
exp_all_options = sorted(df['experience_level'].unique())
exp_full_options = [experience_level_map.get(opt, opt) for opt in exp_all_options]
experience_selection = st.sidebar.multiselect(
    "⭐ Career Level",
    options=exp_full_options,
    default=exp_full_options,
    key='exp_filter'
)
experience_options = [k for k, v in experience_level_map.items() if v in experience_selection]
if not experience_options:
    experience_options = exp_all_options
    st.sidebar.warning("At least one option must be selected")

# Employment Type
employment_all_options = sorted(df['employment_type'].unique())
employment_full_options = [employment_type_map.get(opt, opt) for opt in employment_all_options]
employment_selection = st.sidebar.multiselect(
    "💼 Job Type",
    options=employment_full_options,
    default=employment_full_options,
    key='employment_filter'
)
employment_options = [k for k, v in employment_type_map.items() if v in employment_selection]
if not employment_options:
    employment_options = employment_all_options
    st.sidebar.warning("At least one option must be selected")

# Location
loc_all_options = sorted(df['company_location'].unique())
location_options = st.sidebar.multiselect(
    "📍 Location",
    options=loc_all_options,
    default=loc_all_options,
    key='loc_filter'
)
if not location_options:
    location_options = loc_all_options
    st.sidebar.warning("At least one option must be selected")

# Company Size
size_all_options = sorted(df['company_size'].unique())
size_full_options = [company_size_map.get(opt, opt) for opt in size_all_options]
company_size_selection = st.sidebar.multiselect(
    "🏭 Organization Size",
    options=size_full_options,
    default=size_full_options,
    key='size_filter'
)
company_size_options = [k for k, v in company_size_map.items() if v in company_size_selection]
if not company_size_options:
    company_size_options = size_all_options
    st.sidebar.warning("At least one option must be selected")

# Company Name
company_all_options = sorted(df['company_name'].unique())
company_options = st.sidebar.multiselect(
    "🏢 Company",
    options=company_all_options,
    default=company_all_options,
    key='company_filter'
)
if not company_options:
    company_options = company_all_options

# Minimum Salary
min_salary = st.sidebar.number_input(
    f"💵 Minimum Salary",
    min_value=0,
    value=0,
    step=10000,
    format="%d"
)

# Skills
all_skills = set()
if 'required_skills' in df.columns:
    for skills in df['required_skills'].dropna():
        all_skills.update([s.strip() for s in str(skills).split(',')])

skills_options = st.sidebar.multiselect(
    "💻 Required Skills",
    options=sorted(all_skills),
    key='skills_filter'
)

# Apply filters button
st.sidebar.divider()
col1, col2 = st.sidebar.columns(2)
with col1:
    apply_filters = st.button("🔍 Apply", use_container_width=True)
with col2:
    if st.button("🔄 Clear", use_container_width=True):
        st.rerun()

# Filter data
filtered_df = df.copy()

filtered_df = filtered_df[filtered_df['experience_level'].isin(experience_options)]
filtered_df = filtered_df[filtered_df['employment_type'].isin(employment_options)]
filtered_df = filtered_df[filtered_df['company_location'].isin(location_options)]
filtered_df = filtered_df[filtered_df['company_size'].isin(company_size_options)]
filtered_df = filtered_df[filtered_df['company_name'].isin(company_options)]
filtered_df = filtered_df[filtered_df['salary_target'] >= min_salary]

if skills_options:
    filtered_df = filtered_df[filtered_df['required_skills'].apply(
        lambda x: any(skill in str(x) for skill in skills_options) if pd.notna(x) else False
    )]

# Display table
if len(filtered_df) > 0:
    # Mapping for user-friendly values
    experience_level_map = {
        'EN': 'Entry',
        'MI': 'Mid',
        'SE': 'Senior',
        'CT': 'Contract',
        'FL': 'Freelance',
        'EX': 'Executive', 
        # Add more if needed
    }
    employment_type_map = {
        'FT': 'Full-Time',
        'PT': 'Part-Time',
        'CT': 'Contract',
        'FL': 'Freelance',
        # Add more if needed
    }
    company_size_map = {
        'S': 'Small',
        'M': 'Medium',
        'L': 'Large',
        'E': 'Enterprise',
        # Add more if needed
    }

    display_df = filtered_df.copy()
    display_df['salary_display'] = display_df['salary_target'].apply(
        lambda x: f"{x:,.0f} {target_currency}"
    )
    if 'experience_level' in display_df.columns:
        display_df['experience_level'] = display_df['experience_level'].map(experience_level_map).fillna(display_df['experience_level'])
    if 'employment_type' in display_df.columns:
        display_df['employment_type'] = display_df['employment_type'].map(employment_type_map).fillna(display_df['employment_type'])
    if 'company_size' in display_df.columns:
        display_df['company_size'] = display_df['company_size'].map(company_size_map).fillna(display_df['company_size'])

    display_columns = {
        'job_title': 'Job Title',
        'company_name': 'Company',
        'experience_level': 'Career Level',
        'employment_type': 'Job Type',
        'company_location': 'Location',
        'company_size': 'Organization Size',
        'salary_display': 'Salary',
        'remote_ratio': 'Remote %'
    }

    available_cols = [col for col in display_columns.keys() if col in display_df.columns]
    display_columns = {col: display_columns[col] for col in available_cols}

    st.dataframe(
        display_df[available_cols].rename(columns=display_columns),
        use_container_width=True,
        height=500,
        column_config={
            "Remote %": st.column_config.ProgressColumn(
                "Remote %",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
        }
    )
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="aiml_jobs_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.warning("⚠️ No jobs match your criteria. Try adjusting the filters.")

st.divider()

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8rem;'>
    <p>© 2025 Mohammadreza Hendiani</p>
</div>
""", unsafe_allow_html=True)