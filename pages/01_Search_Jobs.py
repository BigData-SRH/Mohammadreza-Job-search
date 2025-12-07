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

# Theme application
def apply_theme():
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #fafafa; }
        .main { background-color: #0e1117; }
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown { color: #fafafa !important; }
        .stTextInput label, .stSelectbox label, .stMultiSelect label, .stNumberInput label { color: #fafafa !important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background-color: #ffffff; color: #31333F; }
        .main { background-color: #ffffff; }
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown { color: #31333F !important; }
        .stTextInput label, .stSelectbox label, .stMultiSelect label, .stNumberInput label { color: #31333F !important; }
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

        # Add work_type based on remote_ratio (hybrid = between 0% and 100% exclusive)
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

# Sidebar settings (Display Settings only)
with st.sidebar:
    st.markdown("### Display Settings")

    # Theme toggle
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

    # Currency settings
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

    # Reset button
    if st.button("Reset All Settings", use_container_width=True, key="reset_btn"):
        st.session_state.theme = 'light'
        st.session_state.default_currency = 'USD'
        st.cache_data.clear()
        st.rerun()

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

st.divider()

# FILTERS AT TOP OF PAGE
st.subheader("Filters")

# Row 1: Work Type, Career Level, Job Type
filter_row1_col1, filter_row1_col2, filter_row1_col3 = st.columns(3)

with filter_row1_col1:
    work_type_all = sorted(df['work_type'].unique())
    work_type_options = st.multiselect(
        "Work Type (Remote/Hybrid/On-site)",
        options=work_type_all,
        default=work_type_all,
        key='work_type_filter'
    )
    if not work_type_options:
        work_type_options = work_type_all
        st.warning("At least one option must be selected")

with filter_row1_col2:
    exp_all_options = sorted(df['experience_level'].unique())
    exp_full_options = [experience_level_map.get(opt, opt) for opt in exp_all_options]
    experience_selection = st.multiselect(
        "Career Level",
        options=exp_full_options,
        default=exp_full_options,
        key='exp_filter'
    )
    experience_options = [k for k, v in experience_level_map.items() if v in experience_selection]
    if not experience_options:
        experience_options = exp_all_options

with filter_row1_col3:
    employment_all_options = sorted(df['employment_type'].unique())
    employment_full_options = [employment_type_map.get(opt, opt) for opt in employment_all_options]
    employment_selection = st.multiselect(
        "Job Type",
        options=employment_full_options,
        default=employment_full_options,
        key='employment_filter'
    )
    employment_options = [k for k, v in employment_type_map.items() if v in employment_selection]
    if not employment_options:
        employment_options = employment_all_options

# Row 2: Company Location, Organization Size, Company
filter_row2_col1, filter_row2_col2, filter_row2_col3 = st.columns(3)

with filter_row2_col1:
    loc_all_options = sorted(df['company_location'].unique())
    location_options = st.multiselect(
        "Company Location",
        options=loc_all_options,
        default=loc_all_options,
        key='loc_filter',
        help="Filter by the country where the company is located"
    )
    if not location_options:
        location_options = loc_all_options

with filter_row2_col2:
    size_all_options = sorted(df['company_size'].unique())
    size_full_options = [company_size_map.get(opt, opt) for opt in size_all_options]
    company_size_selection = st.multiselect(
        "Organization Size",
        options=size_full_options,
        default=size_full_options,
        key='size_filter'
    )
    company_size_options = [k for k, v in company_size_map.items() if v in company_size_selection]
    if not company_size_options:
        company_size_options = size_all_options

with filter_row2_col3:
    company_all_options = sorted(df['company_name'].unique())
    company_options = st.multiselect(
        "Company",
        options=company_all_options,
        default=company_all_options,
        key='company_filter'
    )
    if not company_options:
        company_options = company_all_options

# Row 3: Minimum Salary, Required Skills
filter_row3_col1, filter_row3_col2 = st.columns(2)

with filter_row3_col1:
    min_salary = st.number_input(
        f"Minimum Salary ({target_currency})",
        min_value=0,
        value=0,
        step=10000,
        format="%d",
        help=f"Salaries are displayed in {target_currency}. Original salaries in USD are converted using real-time exchange rates."
    )

with filter_row3_col2:
    all_skills = set()
    if 'required_skills' in df.columns:
        for skills in df['required_skills'].dropna():
            all_skills.update([s.strip() for s in str(skills).split(',')])

    skills_options = st.multiselect(
        "Required Skills",
        options=sorted(all_skills),
        key='skills_filter'
    )

# Apply/Clear buttons
st.markdown("")
btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 4])
with btn_col1:
    apply_filters = st.button("Apply Filters", use_container_width=True, type="primary", key="apply_btn")
with btn_col2:
    if st.button("Clear Filters", use_container_width=True, key="clear_btn"):
        st.rerun()

st.divider()

# Filter data
with st.spinner("Filtering jobs..."):
    filtered_df = df.copy()

    filtered_df = filtered_df[filtered_df['work_type'].isin(work_type_options)]
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

    # Prepare full raw data for download (includes all columns like skills, dates, etc.)
    download_df = filtered_df.copy()
    # Include original columns plus the converted salary for convenience
    download_df['salary_converted'] = download_df['salary_target']
    download_df['converted_currency'] = target_currency

    csv = download_df.to_csv(index=False).encode('utf-8')

    st.markdown("---")
    st.markdown("**Download Complete Dataset**")
    st.caption("The CSV file includes all data fields for the filtered jobs, including fields not shown in the table above such as required_skills, posting_date, salary_usd (original), and salary_converted (in your selected currency).")

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
