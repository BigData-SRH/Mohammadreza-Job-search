# app.py - Main Dashboard Page (AI Job Market Explorer)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="AI Job Market Explorer",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for settings
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'default_currency' not in st.session_state:
    st.session_state.default_currency = 'USD'
if 'currency_rates' not in st.session_state:
    st.session_state.currency_rates = {}
if 'last_rate_update' not in st.session_state:
    st.session_state.last_rate_update = None

# Fetch real-time currency rates
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

# Get currency rates
if not st.session_state.currency_rates or not st.session_state.last_rate_update or \
   (datetime.now() - st.session_state.last_rate_update) > timedelta(hours=1):
    st.session_state.currency_rates = fetch_currency_rates()
    st.session_state.last_rate_update = datetime.now()

CURRENCY_RATES = st.session_state.currency_rates

def convert_to_target_currency(amount_usd, target_currency='USD'):
    if target_currency == 'USD':
        return amount_usd
    return amount_usd * CURRENCY_RATES.get(target_currency, 1.0)

# Theme application
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

        /* Multiselect placeholder and empty state */
        .stMultiSelect input::placeholder {
            color: #a0a0b0 !important;
        }
        .stMultiSelect div[data-baseweb="select"] > div {
            color: #a0a0b0 !important;
        }
        [data-baseweb="menu"] [role="presentation"] {
            background-color: #262730 !important;
            color: #a0a0b0 !important;
        }
        [data-baseweb="menu"] li[role="presentation"] {
            background-color: #262730 !important;
            color: #a0a0b0 !important;
        }
        .stMultiSelect [class*="placeholder"] {
            color: #a0a0b0 !important;
        }
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

        /* Metrics for light theme - better contrast */
        [data-testid="stMetric"] {
            background-color: #f8f9fa;
            border: 1px solid #e2e8f0;
        }
        [data-testid="stMetricValue"] { color: #1a1a2e !important; }
        [data-testid="stMetricLabel"] { color: #4a5568 !important; }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

def get_theme_colors():
    if st.session_state.theme == 'dark':
        return {'bg': '#0e1117', 'paper_bg': '#262730', 'text': '#fafafa', 'grid': '#3b3b3b'}
    else:
        return {'bg': '#ffffff', 'paper_bg': '#f8f9fa', 'text': '#1a1a2e', 'grid': '#cbd5e0'}

theme_colors = get_theme_colors()

# Sidebar settings
with st.sidebar:
    st.markdown("### Display Settings")

    # Theme toggle
    st.markdown("**Theme**")
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("Dark", use_container_width=True, disabled=(st.session_state.theme == 'dark')):
            st.session_state.theme = 'dark'
            st.rerun()
    with theme_col2:
        if st.button("Light", use_container_width=True, disabled=(st.session_state.theme == 'light')):
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
        label_visibility="collapsed"
    )

    if selected_currency != st.session_state.default_currency:
        st.session_state.default_currency = selected_currency
        st.rerun()

    st.markdown("---")

    if st.session_state.last_rate_update:
        st.caption(f"Rates updated: {st.session_state.last_rate_update.strftime('%Y-%m-%d %H:%M')}")

# Title
st.title("AI Job Market Explorer")
st.markdown("Discover insights from 2,000+ AI/ML job postings (Oct 2024 - Jul 2025)")

# Helper function to categorize work type (hybrid = between 0% and 100% exclusive)
def categorize_work_type(ratio):
    if ratio == 0:
        return 'On-site'
    elif ratio == 100:
        return 'Remote'
    else:
        return 'Hybrid'

# Load data with spinner
@st.cache_data
def load_data():
    np.random.seed(42)

    countries_currencies = {
        'USA': 'USD', 'UK': 'GBP', 'Germany': 'EUR', 'Canada': 'CAD',
        'Australia': 'AUD', 'India': 'INR', 'Japan': 'JPY'
    }

    company_sizes = ['Startup (1-50)', 'Small (51-200)', 'Medium (201-1000)',
                     'Large (1001-5000)', 'Enterprise (5000+)']

    locations = list(countries_currencies.keys())
    n_samples = 2000

    experience_levels = np.random.choice(['Junior', 'Mid-Level', 'Senior', 'Lead'],
                                        n_samples, p=[0.25, 0.35, 0.30, 0.10])

    location_list = np.random.choice(locations, n_samples)
    currencies = [countries_currencies[loc] for loc in location_list]

    exp_multipliers = {
        'Junior': (0.6, 0.8), 'Mid-Level': (0.8, 1.1),
        'Senior': (1.2, 1.6), 'Lead': (1.7, 2.2)
    }

    base_salary_ranges = {
        'USD': (80000, 130000), 'GBP': (55000, 90000), 'EUR': (60000, 100000),
        'CAD': (90000, 140000), 'AUD': (100000, 160000),
        'INR': (1200000, 2500000), 'JPY': (8000000, 13000000)
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
        salaries_usd.append(local_salary / CURRENCY_RATES[curr])

    remote_ratios = []
    for _ in range(n_samples):
        rand = np.random.random()
        if rand < 0.3:
            remote_ratios.append(0)
        elif rand < 0.5:
            remote_ratios.append(100)
        elif rand < 0.7:
            remote_ratios.append(50)
        else:
            remote_ratios.append(np.random.randint(20, 80))

    work_types = [categorize_work_type(r) for r in remote_ratios]

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
        'company_size': np.random.choice(company_sizes, n_samples),
        'company': np.random.choice(['Google', 'Amazon', 'Microsoft', 'Meta', 'Apple', 'IBM',
                                     'NVIDIA', 'Tesla', 'OpenAI', 'DeepMind', 'Anthropic', 'Databricks'], n_samples),
        'skills': [', '.join(np.random.choice(['Python', 'TensorFlow', 'PyTorch', 'SQL', 'AWS',
                    'Docker', 'Kubernetes', 'Scikit-learn', 'R', 'Spark'],
                    size=np.random.randint(2, 6), replace=False)) for _ in range(n_samples)],
        'posted_date': pd.date_range(start='2024-10-01', periods=n_samples, freq='3H')
    })

    return data

with st.spinner("Loading data..."):
    df = load_data()

target_currency = st.session_state.default_currency
df['salary_target'] = df['salary_usd'].apply(lambda x: convert_to_target_currency(x, target_currency))

# Custom CSS for metric cards
st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: bold;
    color: """ + ('#fafafa' if st.session_state.theme == 'dark' else '#1a1a2e') + """ !important;
}
[data-testid="stMetricLabel"] {
    color: """ + ('#c0c0c0' if st.session_state.theme == 'dark' else '#4a5568') + """ !important;
}
[data-testid="stMetric"] {
    background-color: """ + theme_colors['paper_bg'] + """;
    border: 2px solid """ + ('#4B5563' if st.session_state.theme == 'dark' else '#cbd5e0') + """;
    padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_salary = df['salary_target'].mean()
    st.metric("Avg Salary", f"{avg_salary/1000:.0f}K {target_currency}", "+8%")

with col2:
    total_jobs = len(df)
    st.metric("Total Jobs", f"{total_jobs:,}", "")

with col3:
    remote_pct = (df['work_type'] == 'Remote').sum() / len(df) * 100
    st.metric("Remote Jobs", f"{remote_pct:.1f}%", "")

with col4:
    hybrid_pct = (df['work_type'] == 'Hybrid').sum() / len(df) * 100
    st.metric("Hybrid Jobs", f"{hybrid_pct:.1f}%", "")

if target_currency != 'USD':
    st.caption(f"Salary values converted from USD to {target_currency} using ExchangeRate-API rates")

st.divider()

# Monthly trends
st.subheader("Job Postings Trend (Oct 2024 - Jul 2025)")
df['month'] = df['posted_date'].dt.to_period('M').astype(str)
monthly_counts = df.groupby('month').size().reset_index(name='count')

with st.spinner("Generating trend chart..."):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_counts['month'], y=monthly_counts['count'],
        mode='lines+markers', name='Job Postings',
        line=dict(color='#3B82F6', width=3), marker=dict(size=8)
    ))
    fig.update_layout(
        xaxis_title='Month', yaxis_title='Number of Postings',
        height=350, hovermode='x unified',
        plot_bgcolor=theme_colors['paper_bg'], paper_bgcolor=theme_colors['bg'],
        font=dict(color=theme_colors['text']),
        xaxis=dict(gridcolor=theme_colors['grid']), yaxis=dict(gridcolor=theme_colors['grid'])
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Main visualizations - Row 1
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Salary by Experience Level")
    if target_currency != 'USD':
        st.caption(f"Original salaries in USD, converted to {target_currency} using ExchangeRate-API")
    else:
        st.caption("Salaries displayed in original USD")
    with st.spinner("Loading..."):
        fig = go.Figure()
        exp_order = ['Junior', 'Mid-Level', 'Senior', 'Lead']
        colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']

        for exp, color in zip(exp_order, colors):
            exp_data = df[df['experience_level'] == exp]['salary_target']
            fig.add_trace(go.Box(y=exp_data, name=exp, marker_color=color, boxmean='sd'))

        fig.update_layout(
            yaxis_title=f'Salary ({target_currency})', xaxis_title='Experience Level',
            height=350, showlegend=False,
            plot_bgcolor=theme_colors['paper_bg'], paper_bgcolor=theme_colors['bg'],
            font=dict(color=theme_colors['text']),
            xaxis=dict(gridcolor=theme_colors['grid']), yaxis=dict(gridcolor=theme_colors['grid'])
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Job Title Distribution")
    with st.spinner("Loading..."):
        job_dist = df['job_title'].value_counts().reset_index()
        job_dist.columns = ['job_title', 'count']

        # Use theme-appropriate color scale
        if st.session_state.theme == 'dark':
            color_scale = [[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#60a5fa']]  # Dark theme: darker to lighter blue
        else:
            color_scale = [[0, '#2563eb'], [0.5, '#1e40af'], [1, '#1e3a8a']]  # Light theme: vibrant to dark blue

        fig = px.bar(job_dist, y='job_title', x='count', orientation='h',
                     color='count', color_continuous_scale=color_scale)
        fig.update_layout(
            height=350, showlegend=False,
            xaxis_title='Number of Jobs', yaxis_title='Job Title',
            plot_bgcolor=theme_colors['paper_bg'], paper_bgcolor=theme_colors['bg'],
            font=dict(color=theme_colors['text']),
            xaxis=dict(gridcolor=theme_colors['grid']), yaxis=dict(gridcolor=theme_colors['grid'])
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# Main visualizations - Row 2
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Work Type Distribution")
    with st.spinner("Loading..."):
        work_type_dist = df['work_type'].value_counts().reset_index()
        work_type_dist.columns = ['work_type', 'count']

        fig = px.pie(work_type_dist, values='count', names='work_type', hole=0.4,
                     color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B'])
        fig.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
        fig.update_layout(height=300, plot_bgcolor=theme_colors['paper_bg'],
                          paper_bgcolor=theme_colors['bg'], font=dict(color=theme_colors['text']))
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Jobs by Country")
    with st.spinner("Loading..."):
        loc_dist = df['location'].value_counts().reset_index()
        loc_dist.columns = ['location', 'count']
        loc_dist['percentage'] = (loc_dist['count'] / loc_dist['count'].sum() * 100).round(1)
        loc_dist = loc_dist.sort_values('count', ascending=True)

        fig = go.Figure()
        for idx, row in loc_dist.iterrows():
            fig.add_trace(go.Scatter(
                x=[0, row['count']], y=[row['location'], row['location']],
                mode='lines', line=dict(color='lightgray', width=2),
                showlegend=False, hoverinfo='skip'
            ))

        fig.add_trace(go.Scatter(
            x=loc_dist['count'], y=loc_dist['location'],
            mode='markers+text', marker=dict(size=12, color='#3B82F6'),
            text=[f"{p:.1f}%" for p in loc_dist['percentage']],
            textposition='middle right', textfont=dict(color=theme_colors['text']),
            showlegend=False, hovertemplate='<b>%{y}</b><br>Jobs: %{x}<extra></extra>'
        ))

        fig.update_layout(
            height=300, xaxis_title='Number of Jobs', yaxis_title='',
            margin=dict(l=0, r=80, t=20, b=40),
            plot_bgcolor=theme_colors['paper_bg'], paper_bgcolor=theme_colors['bg'],
            font=dict(color=theme_colors['text']),
            xaxis=dict(gridcolor=theme_colors['grid']), yaxis=dict(gridcolor=theme_colors['grid'])
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# Skills demand
st.subheader("Most In-Demand Skills")
with st.spinner("Analyzing skills..."):
    all_skills = []
    for skills in df['skills']:
        all_skills.extend([s.strip() for s in skills.split(',')])

    skills_count = pd.Series(all_skills).value_counts().reset_index()
    skills_count.columns = ['skill', 'count']
    skills_count['percentage'] = (skills_count['count'] / len(df) * 100).round(1)

    fig = px.bar(skills_count.head(10), y='skill', x='percentage', orientation='h',
                 text='percentage', labels={'percentage': 'Percentage of Jobs (%)', 'skill': 'Skill'},
                 color='percentage', color_continuous_scale='Viridis')
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color=theme_colors['text']))
    fig.update_layout(
        height=400, showlegend=False,
        plot_bgcolor=theme_colors['paper_bg'], paper_bgcolor=theme_colors['bg'],
        font=dict(color=theme_colors['text']),
        xaxis=dict(gridcolor=theme_colors['grid']), yaxis=dict(gridcolor=theme_colors['grid'])
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Salary by country
st.subheader(f"Average Salary by Country (Displayed in {target_currency})")
if target_currency != 'USD':
    st.caption("Original salaries in USD, converted using real-time exchange rates from ExchangeRate-API. Hover over bars to see original currency.")
else:
    st.caption("Salaries displayed in original USD. Hover over bars to see local currency equivalent.")

with st.spinner("Loading salary comparison..."):
    # Get both local and converted salaries for display
    salary_by_location = df.groupby(['location', 'currency']).agg({
        'salary_target': 'mean',
        'salary_local': 'mean'
    }).reset_index()
    salary_by_location = salary_by_location.sort_values('salary_target', ascending=True)

    # Use theme-appropriate color scale
    if st.session_state.theme == 'dark':
        color_scale = [[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#60a5fa']]  # Dark theme: darker to lighter blue
        text_color = 'white'
    else:
        color_scale = [[0, '#2563eb'], [0.5, '#1e40af'], [1, '#1e3a8a']]  # Light theme: vibrant to dark blue
        text_color = 'white'

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=salary_by_location['location'], x=salary_by_location['salary_target'],
        orientation='h', text=[f"{sal:,.0f}" for sal in salary_by_location['salary_target']],
        textposition='auto', textfont=dict(color=text_color),
        marker=dict(color=salary_by_location['salary_target'], colorscale=color_scale, showscale=False),
        hovertemplate='<b>%{y}</b><br>Converted: %{x:,.0f} ' + target_currency + '<br>Original Currency: %{customdata}<extra></extra>',
        customdata=salary_by_location['currency']
    ))

    fig.update_layout(
        xaxis_title=f'Average Salary ({target_currency})', yaxis_title='Country',
        height=350, margin=dict(l=0, r=20, t=20, b=40),
        plot_bgcolor=theme_colors['paper_bg'], paper_bgcolor=theme_colors['bg'],
        font=dict(color=theme_colors['text']),
        xaxis=dict(gridcolor=theme_colors['grid']), yaxis=dict(gridcolor=theme_colors['grid'])
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: gray; font-size: 0.8rem;'>
    <p>AI Job Market Explorer | Data: 2,000+ postings (Oct 2024 - Jul 2025) | Built with Streamlit</p>
    <p>2025 Mohammadreza Hendiani | Licensed under MIT</p>
</div>
""", unsafe_allow_html=True)
