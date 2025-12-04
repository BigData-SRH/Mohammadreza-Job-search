# pages/1_🔍_Search_Jobs.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Search Jobs", page_icon="🔍", layout="wide")

st.title("🔍 Search & Filter Jobs")
st.markdown("Find AI/ML jobs that match your criteria")

# Currency conversion rates (to USD)
CURRENCY_RATES = {
    'USD': 1.0,
    'EUR': 1.09,
    'GBP': 1.27,
    'CAD': 0.72,
    'AUD': 0.65,
    'INR': 0.012,
    'JPY': 0.0067
}

# Load data
@st.cache_data
def load_data():
    np.random.seed(42)
    
    countries_currencies = {
        'USA': 'USD',
        'UK': 'GBP', 
        'Germany': 'EUR',
        'Canada': 'CAD',
        'Australia': 'AUD',
        'India': 'INR',
        'Japan': 'JPY'
    }
    
    locations = list(countries_currencies.keys())
    n_samples = 2000
    
    # Generate experience levels
    experience_levels = np.random.choice(['Junior', 'Mid-Level', 'Senior', 'Lead'], n_samples, p=[0.25, 0.35, 0.30, 0.10])
    
    location_list = np.random.choice(locations, n_samples)
    currencies = [countries_currencies[loc] for loc in location_list]
    
    # Salary multipliers by experience
    exp_multipliers = {
        'Junior': (0.6, 0.8),
        'Mid-Level': (0.8, 1.1),
        'Senior': (1.2, 1.6),
        'Lead': (1.7, 2.2)
    }
    
    base_salary_ranges = {
        'USD': (80000, 130000),
        'GBP': (55000, 90000),
        'EUR': (60000, 100000),
        'CAD': (90000, 140000),
        'AUD': (100000, 160000),
        'INR': (1200000, 2500000),
        'JPY': (8000000, 13000000)
    }
    
    salaries_local = []
    salaries_usd = []
    for loc, curr, exp in zip(location_list, currencies, experience_levels):
        min_base, max_base = base_salary_ranges[curr]
        mult_min, mult_max = exp_multipliers[exp]
        
        min_sal = int(min_base * mult_min)
        max_sal = int(max_base * mult_max)
        
        local_salary = np.random.randint(min_sal, max_sal)
        salaries_local.append(local_salary)
        salaries_usd.append(local_salary * CURRENCY_RATES[curr])
    
    # Generate remote ratio with more realistic distribution
    remote_ratios = []
    for _ in range(n_samples):
        rand = np.random.random()
        if rand < 0.3:  # 30% fully on-site
            remote_ratios.append(0)
        elif rand < 0.5:  # 20% fully remote
            remote_ratios.append(100)
        elif rand < 0.7:  # 20% at 50% (hybrid)
            remote_ratios.append(50)
        else:  # 30% other hybrid values
            remote_ratios.append(np.random.randint(20, 80))
    
    # Determine work type: only 50% is hybrid
    work_types = []
    for ratio in remote_ratios:
        if ratio == 0:
            work_types.append('On-site')
        elif ratio == 100:
            work_types.append('Remote')
        elif ratio == 50:
            work_types.append('Hybrid')
        else:
            if ratio < 50:
                work_types.append('On-site')
            else:
                work_types.append('Remote')
    
    data = pd.DataFrame({
        'job_title': np.random.choice(['Data Scientist', 'ML Engineer', 'AI Researcher', 'Data Analyst',
                                       'Deep Learning Engineer', 'NLP Engineer', 'Computer Vision Engineer'], n_samples),
        'experience_level': experience_levels,
        'location': location_list,
        'currency': currencies,
        'salary_local': salaries_local,
        'salary_usd': salaries_usd,
        'remote_ratio': remote_ratios,
        'work_type': work_types,
        'skills': [', '.join(np.random.choice(['Python', 'TensorFlow', 'PyTorch', 'SQL', 'AWS', 
                    'Docker', 'Kubernetes', 'Scikit-learn', 'R', 'Spark'], 
                    size=np.random.randint(2, 6), replace=False)) for _ in range(n_samples)],
        'posted_date': pd.date_range(start='2024-10-01', periods=n_samples, freq='3H'),
        'company': np.random.choice(['Google', 'Amazon', 'Microsoft', 'Meta', 'Apple', 'IBM', 
                                     'NVIDIA', 'Tesla', 'OpenAI', 'DeepMind'], n_samples)
    })
    
    return data

df = load_data()

# Sidebar filters
st.sidebar.header("🔧 Filters")

# Experience Level
experience_options = st.sidebar.multiselect(
    "⭐ Experience Level",
    options=sorted(df['experience_level'].unique()),
    default=df['experience_level'].unique()
)

# Work Type
work_type_options = st.sidebar.multiselect(
    "🏢 Work Type",
    options=sorted(df['work_type'].unique()),
    default=df['work_type'].unique()
)

# Location
location_options = st.sidebar.multiselect(
    "📍 Location",
    options=sorted(df['location'].unique()),
    default=df['location'].unique()
)

# Minimum Salary in USD (no maximum)
min_salary_usd = st.sidebar.number_input(
    "💵 Minimum Salary (USD)",
    min_value=0,
    max_value=int(df['salary_usd'].max()),
    value=0,
    step=10000,
    help="Enter minimum salary in USD equivalent"
)

# Skills
all_skills = set()
for skills in df['skills']:
    all_skills.update([s.strip() for s in skills.split(',')])

skills_options = st.sidebar.multiselect(
    "💻 Required Skills",
    options=sorted(all_skills)
)

# Apply filters button
st.sidebar.divider()
col1, col2 = st.sidebar.columns(2)
with col1:
    apply_filters = st.button("🔍 Apply", use_container_width=True)
with col2:
    clear_filters = st.button("🔄 Clear", use_container_width=True)

if clear_filters:
    st.rerun()

# Filter data
filtered_df = df.copy()

if experience_options:
    filtered_df = filtered_df[filtered_df['experience_level'].isin(experience_options)]

if work_type_options:
    filtered_df = filtered_df[filtered_df['work_type'].isin(work_type_options)]

if location_options:
    filtered_df = filtered_df[filtered_df['location'].isin(location_options)]

filtered_df = filtered_df[filtered_df['salary_usd'] >= min_salary_usd]

if skills_options:
    filtered_df = filtered_df[filtered_df['skills'].apply(
        lambda x: any(skill in x for skill in skills_options)
    )]

# Display results count and stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📋 Jobs Found", f"{len(filtered_df):,}")
with col2:
    if len(filtered_df) > 0:
        avg_sal = filtered_df['salary_usd'].mean()
        st.metric("💰 Avg Salary", f"${avg_sal/1000:.0f}K")
    else:
        st.metric("💰 Avg Salary", "N/A")
with col3:
    if len(filtered_df) > 0:
        remote_count = (filtered_df['work_type'] == 'Remote').sum()
        st.metric("🏠 Remote", f"{remote_count}")
    else:
        st.metric("🏠 Remote", "0")
with col4:
    if len(filtered_df) > 0:
        hybrid_count = (filtered_df['work_type'] == 'Hybrid').sum()
        st.metric("🔀 Hybrid", f"{hybrid_count}")
    else:
        st.metric("🔀 Hybrid", "0")

st.divider()

# Display table
if len(filtered_df) > 0:
    # Format salary display
    display_df = filtered_df.copy()
    display_df['salary_display'] = display_df.apply(
        lambda row: f"{row['salary_local']:,.0f} {row['currency']} (${row['salary_usd']:,.0f})", 
        axis=1
    )
    
    # Select and rename columns for display
    display_columns = {
        'job_title': 'Job Title',
        'experience_level': 'Experience',
        'work_type': 'Work Type',
        'location': 'Location',
        'salary_display': 'Salary',
        'remote_ratio': 'Remote %',
        'skills': 'Skills',
        'company': 'Company'
    }
    
    st.dataframe(
        display_df[list(display_columns.keys())].rename(columns=display_columns),
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
    
    # Download button
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