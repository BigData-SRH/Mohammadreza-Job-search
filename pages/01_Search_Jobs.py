# pages/01_Search_Jobs.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Search Jobs", page_icon="magnifying_glass", layout="wide")

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'default_currency' not in st.session_state:
    st.session_state.default_currency = 'USD'
if 'currency_rates' not in st.session_state:
    st.session_state.currency_rates = {}
if 'last_rate_update' not in st.session_state:
    st.session_state.last_rate_update = None

# Theme application with sidebar support
def apply_theme():
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
        /* Main app background */
        .stApp { background-color: #0e1117; color: #fafafa; }
        .main { background-color: #0e1117; }

        /* Top header bar */
        header[data-testid="stHeader"] { background-color: #0e1117; }
        [data-testid="stToolbar"] { background-color: #0e1117; }
        [data-testid="stDecoration"] { background-color: #0e1117; }

        /* Sidebar */
        [data-testid="stSidebar"] { background-color: #262730; }
        [data-testid="stSidebar"] * { color: #fafafa !important; }
        [data-testid="stSidebarContent"] { background-color: #262730; }

        /* Text elements */
        h1, h2, h3, h4, h5, h6 { color: #fafafa !important; }
        p, span, label, .stMarkdown { color: #e0e0e0 !important; }
        .stMarkdown p { color: #e0e0e0 !important; }

        /* Labels for inputs */
        .stTextInput label, .stSelectbox label, .stMultiSelect label, .stNumberInput label {
            color: #fafafa !important;
        }

        /* Buttons */
        .stButton > button {
            background-color: #3a3a4a;
            color: #fafafa;
            border: 1px solid #5a5a6a;
        }
        .stButton > button:hover {
            background-color: #4a4a5a;
            border-color: #6a6a7a;
            color: #ffffff;
        }
        .stButton > button:disabled {
            background-color: #2a2a3a;
            color: #7a7a8a;
        }
        .stDownloadButton > button {
            background-color: #3a3a4a;
            color: #fafafa;
            border: 1px solid #5a5a6a;
        }
        .stDownloadButton > button:hover {
            background-color: #4a4a5a;
        }

        /* Expander */
        [data-testid="stExpander"] {
            background-color: #1a1a2a;
            border: 1px solid #3a3a4a;
            border-radius: 4px;
        }
        [data-testid="stExpander"] details {
            background-color: #1a1a2a;
        }
        [data-testid="stExpander"] summary {
            color: #fafafa !important;
            background-color: #1a1a2a;
        }
        [data-testid="stExpander"] summary:hover {
            background-color: #2a2a3a;
        }
        [data-testid="stExpander"] summary span {
            color: #fafafa !important;
        }
        [data-testid="stExpander"] svg {
            fill: #fafafa !important;
            stroke: #fafafa !important;
        }
        .streamlit-expanderHeader {
            background-color: #1a1a2a;
            color: #fafafa !important;
        }
        .streamlit-expanderContent {
            background-color: #1a1a2a;
        }

        /* Selectbox and Multiselect */
        .stSelectbox > div > div { background-color: #262730; color: #fafafa; }
        .stMultiSelect > div > div { background-color: #262730; color: #fafafa; }
        .stSelectbox [data-baseweb="select"] { background-color: #262730 !important; }
        .stMultiSelect [data-baseweb="select"] { background-color: #262730 !important; }
        [data-baseweb="select"] { background-color: #262730 !important; }
        [data-baseweb="select"] > div { background-color: #262730 !important; color: #fafafa !important; }
        [data-baseweb="select"] input { color: #fafafa !important; }
        [data-baseweb="popover"] { background-color: #262730 !important; }
        [data-baseweb="popover"] > div { background-color: #262730 !important; }
        [data-baseweb="menu"] { background-color: #262730 !important; }
        [data-baseweb="menu"] li { background-color: #262730 !important; color: #fafafa !important; }
        [role="listbox"] { background-color: #262730 !important; }
        [role="option"] { background-color: #262730 !important; color: #fafafa !important; }
        [role="option"]:hover { background-color: #3a3a4a !important; }
        .stMultiSelect span[data-baseweb="tag"] {
            color: #fafafa !important;
            background-color: #3a3a4a !important;
        }

        /* Number input - Complete styling */
        .stNumberInput > div > div > input {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a5a !important;
        }
        .stNumberInput input {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        .stNumberInput [data-baseweb="input"] {
            background-color: #262730 !important;
        }
        .stNumberInput [data-baseweb="base-input"] {
            background-color: #262730 !important;
        }
        input[type="number"] {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        /* Number input buttons (+/-) */
        .stNumberInput button {
            background-color: #3a3a4a !important;
            color: #fafafa !important;
            border-color: #4a4a5a !important;
        }
        .stNumberInput button:hover {
            background-color: #4a4a5a !important;
        }
        .stNumberInput svg {
            fill: #fafafa !important;
        }

        /* Dataframe/Table - Complete dark theme */
        .stDataFrame {
            background-color: #1a1a2a !important;
        }
        [data-testid="stDataFrame"] {
            background-color: #1a1a2a !important;
        }
        [data-testid="stDataFrame"] > div {
            background-color: #1a1a2a !important;
        }
        .stDataFrame iframe {
            background-color: #1a1a2a !important;
        }
        /* DataFrame inner elements */
        [data-testid="stDataFrame"] div[data-testid="stDataFrameResizable"] {
            background-color: #1a1a2a !important;
        }
        [data-testid="stDataFrame"] canvas {
            filter: invert(1) hue-rotate(180deg);
        }
        /* Multiselect placeholder and empty state */
        .stMultiSelect [data-baseweb="select"] [aria-selected="false"] {
            color: #a0a0b0 !important;
        }
        .stMultiSelect input::placeholder {
            color: #a0a0b0 !important;
        }
        /* Placeholder text when no selection */
        .stMultiSelect div[data-baseweb="select"] > div {
            color: #a0a0b0 !important;
        }
        /* "No results" message in dropdown */
        [data-baseweb="menu"] [role="presentation"] {
            background-color: #262730 !important;
            color: #a0a0b0 !important;
        }
        [data-baseweb="menu"] li[role="presentation"] {
            background-color: #262730 !important;
            color: #a0a0b0 !important;
        }
        /* Empty state / placeholder value */
        .stMultiSelect [class*="placeholder"] {
            color: #a0a0b0 !important;
        }
        .stMultiSelect [class*="singleValue"] {
            color: #fafafa !important;
        }
        /* Selectbox placeholder */
        .stSelectbox div[data-baseweb="select"] > div {
            color: #a0a0b0 !important;
        }
        .stSelectbox [class*="placeholder"] {
            color: #a0a0b0 !important;
        }

        /* Metrics */
        [data-testid="stMetric"] { background-color: #262730; border-color: #4a4a5a; }
        [data-testid="stMetricValue"] { color: #fafafa !important; }
        [data-testid="stMetricLabel"] { color: #c0c0c0 !important; }

        /* Divider */
        hr { border-color: #3a3a4a !important; }
        [data-testid="stDivider"] { background-color: #3a3a4a; }

        /* Caption */
        .stCaption, [data-testid="stCaptionContainer"] { color: #a0a0b0 !important; }

        /* Warning/Info boxes */
        .stAlert { background-color: #262730; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background-color: #ffffff; color: #1a1a2e; }
        .main { background-color: #ffffff; }
        [data-testid="stSidebar"] { background-color: #f8f9fa; }
        h1, h2, h3, h4, h5, h6 { color: #1a1a2e !important; }
        p, span, div, label, .stMarkdown { color: #2d3748 !important; }
        .stTextInput label, .stSelectbox label, .stMultiSelect label, .stNumberInput label { color: #1a1a2e !important; }

        /* Expander light theme */
        [data-testid="stExpander"] {
            background-color: #f8f9fa;
            border: 1px solid #e2e8f0;
        }
        [data-testid="stExpander"] summary span { color: #1a1a2e !important; }

        /* Buttons light theme */
        .stButton > button {
            background-color: #f8f9fa;
            color: #1a1a2e;
            border: 1px solid #e2e8f0;
        }
        .stButton > button:hover {
            background-color: #e2e8f0;
        }
        .stDownloadButton > button {
            background-color: #3b82f6;
            color: #ffffff;
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
            'USD': 1.0, 'EUR': 0.92, 'GBP': 0.79, 'CAD': 1.39,
            'AUD': 1.54, 'INR': 83.12, 'JPY': 149.50
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
        df['salary_usd'] = pd.to_numeric(df['salary_usd'], errors='coerce')
        df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce')
        df = df.dropna(subset=['salary_usd', 'posting_date'])

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
    except FileNotFoundError:
        st.error("Dataset file not found at data/ai_job_dataset.csv")
        return None

# Sidebar settings
with st.sidebar:
    st.markdown("### Display Settings")

    st.markdown("**Theme**")
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("Dark", use_container_width=True, disabled=(st.session_state.theme == 'dark'), key="dark_btn"):
            st.session_state.theme = 'dark'
            st.rerun()
    with theme_col2:
        if st.button("Light", use_container_width=True, disabled=(st.session_state.theme == 'light'), key="light_btn"):
            st.session_state.theme = 'light'
            st.rerun()

    st.markdown("---")

    st.markdown("**Currency**")
    currency_options = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'INR', 'JPY']
    currency_labels = {
        'USD': 'USD - US Dollar', 'EUR': 'EUR - Euro', 'GBP': 'GBP - British Pound',
        'CAD': 'CAD - Canadian Dollar', 'AUD': 'AUD - Australian Dollar',
        'INR': 'INR - Indian Rupee', 'JPY': 'JPY - Japanese Yen'
    }

    selected_currency = st.selectbox(
        "Display Currency",
        options=currency_options,
        format_func=lambda x: currency_labels[x],
        index=currency_options.index(st.session_state.default_currency),
        label_visibility="collapsed",
        key="currency_select"
    )

    if selected_currency != st.session_state.default_currency:
        st.session_state.default_currency = selected_currency
        st.rerun()

    st.markdown("---")

    if st.session_state.last_rate_update:
        st.caption(f"Rates updated: {st.session_state.last_rate_update.strftime('%Y-%m-%d %H:%M')}")

st.title("Search and Filter Jobs")
st.markdown("Find AI/ML jobs that match your criteria")

with st.spinner("Loading job data..."):
    df = load_data()

if df is None:
    st.stop()

target_currency = st.session_state.default_currency
df['salary_target'] = df['salary_usd'].apply(lambda x: convert_to_target_currency(x, target_currency))

# Mapping dictionaries
experience_level_map = {
    'EN': 'Entry', 'MI': 'Mid', 'SE': 'Senior',
    'CT': 'Contract', 'FL': 'Freelance', 'EX': 'Executive'
}
employment_type_map = {
    'FT': 'Full-Time', 'PT': 'Part-Time', 'CT': 'Contract', 'FL': 'Freelance'
}
company_size_map = {
    'S': 'Small', 'M': 'Medium', 'L': 'Large', 'E': 'Enterprise'
}

# Get all options for filters
work_type_all = sorted(df['work_type'].unique().tolist())
exp_all_options = sorted(df['experience_level'].unique().tolist())
exp_full_options = [experience_level_map.get(opt, opt) for opt in exp_all_options]
employment_all_options = sorted(df['employment_type'].unique().tolist())
employment_full_options = [employment_type_map.get(opt, opt) for opt in employment_all_options]
loc_all_options = sorted(df['company_location'].unique().tolist())
size_all_options = sorted(df['company_size'].unique().tolist())
size_full_options = [company_size_map.get(opt, opt) for opt in size_all_options]
company_all_options = sorted(df['company_name'].unique().tolist())

all_skills = set()
if 'required_skills' in df.columns:
    for skills in df['required_skills'].dropna():
        all_skills.update([s.strip() for s in str(skills).split(',')])
all_skills_list = sorted(all_skills)

# Initialize filter session states with defaults if not present
if 'filter_work_type' not in st.session_state:
    st.session_state.filter_work_type = work_type_all
if 'filter_experience' not in st.session_state:
    st.session_state.filter_experience = exp_full_options
if 'filter_employment' not in st.session_state:
    st.session_state.filter_employment = employment_full_options
if 'filter_location' not in st.session_state:
    st.session_state.filter_location = loc_all_options
if 'filter_size' not in st.session_state:
    st.session_state.filter_size = size_full_options
if 'filter_company' not in st.session_state:
    st.session_state.filter_company = company_all_options
if 'filter_min_salary' not in st.session_state:
    st.session_state.filter_min_salary = 0
if 'filter_skills' not in st.session_state:
    st.session_state.filter_skills = []

# FILTERS IN EXPANDER - More compact
with st.expander("Filters", expanded=True):
    # Row 1
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        work_type_options = st.multiselect(
            "Work Type",
            options=work_type_all,
            default=st.session_state.filter_work_type,
            key='work_type_filter'
        )

    with col2:
        experience_selection = st.multiselect(
            "Career Level",
            options=exp_full_options,
            default=st.session_state.filter_experience,
            key='exp_filter'
        )

    with col3:
        employment_selection = st.multiselect(
            "Job Type",
            options=employment_full_options,
            default=st.session_state.filter_employment,
            key='employment_filter'
        )

    with col4:
        location_options = st.multiselect(
            "Company Location",
            options=loc_all_options,
            default=st.session_state.filter_location,
            key='loc_filter',
            help="Country where the company is headquartered"
        )

    # Row 2
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        company_size_selection = st.multiselect(
            "Organization Size",
            options=size_full_options,
            default=st.session_state.filter_size,
            key='size_filter'
        )

    with col2:
        company_options = st.multiselect(
            "Company",
            options=company_all_options,
            default=st.session_state.filter_company,
            key='company_filter'
        )

    with col3:
        min_salary = st.number_input(
            f"Min Salary ({target_currency})",
            min_value=0,
            value=st.session_state.filter_min_salary,
            step=10000,
            format="%d",
            key='salary_filter'
        )

    with col4:
        skills_options = st.multiselect(
            "Required Skills",
            options=all_skills_list,
            default=st.session_state.filter_skills,
            key='skills_filter'
        )

# Update session state from widget values
st.session_state.filter_work_type = work_type_options if work_type_options else work_type_all
st.session_state.filter_experience = experience_selection if experience_selection else exp_full_options
st.session_state.filter_employment = employment_selection if employment_selection else employment_full_options
st.session_state.filter_location = location_options if location_options else loc_all_options
st.session_state.filter_size = company_size_selection if company_size_selection else size_full_options
st.session_state.filter_company = company_options if company_options else company_all_options
st.session_state.filter_min_salary = min_salary
st.session_state.filter_skills = skills_options

# Convert selections back to raw values for filtering
experience_options = [k for k, v in experience_level_map.items() if v in (experience_selection if experience_selection else exp_full_options)]
if not experience_options:
    experience_options = exp_all_options

employment_options = [k for k, v in employment_type_map.items() if v in (employment_selection if employment_selection else employment_full_options)]
if not employment_options:
    employment_options = employment_all_options

company_size_options = [k for k, v in company_size_map.items() if v in (company_size_selection if company_size_selection else size_full_options)]
if not company_size_options:
    company_size_options = size_all_options

# Apply filters
work_type_filter = work_type_options if work_type_options else work_type_all
location_filter = location_options if location_options else loc_all_options
company_filter = company_options if company_options else company_all_options

# Filter data
with st.spinner("Filtering jobs..."):
    filtered_df = df.copy()

    filtered_df = filtered_df[filtered_df['work_type'].isin(work_type_filter)]
    filtered_df = filtered_df[filtered_df['experience_level'].isin(experience_options)]
    filtered_df = filtered_df[filtered_df['employment_type'].isin(employment_options)]
    filtered_df = filtered_df[filtered_df['company_location'].isin(location_filter)]
    filtered_df = filtered_df[filtered_df['company_size'].isin(company_size_options)]
    filtered_df = filtered_df[filtered_df['company_name'].isin(company_filter)]
    filtered_df = filtered_df[filtered_df['salary_target'] >= min_salary]

    if skills_options:
        filtered_df = filtered_df[filtered_df['required_skills'].apply(
            lambda x: any(skill in str(x) for skill in skills_options) if pd.notna(x) else False
        )]

# Display results count
st.markdown(f"**Found {len(filtered_df):,} jobs** matching your criteria")
if target_currency != 'USD':
    st.caption(f"Salaries converted from USD to {target_currency} using ExchangeRate-API")

# Display table
if len(filtered_df) > 0:
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
        'work_type': 'Work Type',
        'company_location': 'Company Location',
        'company_size': 'Organization Size',
        'salary_display': f'Salary ({target_currency})',
        'remote_ratio': 'Remote %'
    }

    available_cols = [col for col in display_columns.keys() if col in display_df.columns]
    display_columns_filtered = {col: display_columns[col] for col in available_cols}

    st.dataframe(
        display_df[available_cols].rename(columns=display_columns_filtered),
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

    # Prepare full raw data for download
    download_df = filtered_df.copy()
    download_df['salary_converted'] = download_df['salary_target']
    download_df['converted_currency'] = target_currency

    csv = download_df.to_csv(index=False).encode('utf-8')

    st.markdown("---")
    st.markdown("**Download Complete Dataset**")
    st.caption("The CSV includes ALL data fields for filtered jobs: required_skills, posting_date, salary_usd (original), salary_converted, and more fields not shown in the table above.")

    st.download_button(
        label="Download Filtered Data as CSV (All Fields)",
        data=csv,
        file_name="aiml_jobs_filtered_complete.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.warning("No jobs match your criteria. Try adjusting the filters.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8rem;'>
    <p>2025 Mohammadreza Hendiani</p>
</div>
""", unsafe_allow_html=True)
