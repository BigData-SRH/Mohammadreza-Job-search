# pages/01_Job_Market_Trends.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Market Trends", page_icon="📈", layout="wide")

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'  # Default to light theme
if 'default_currency' not in st.session_state:
    st.session_state.default_currency = 'USD'
if 'hybrid_min' not in st.session_state:
    st.session_state.hybrid_min = 50
if 'hybrid_max' not in st.session_state:
    st.session_state.hybrid_max = 50
if 'currency_rates' not in st.session_state:
    st.session_state.currency_rates = {}
if 'last_rate_update' not in st.session_state:
    st.session_state.last_rate_update = None

# Unified theme application function
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

# Theme colors
def get_theme_colors():
    if st.session_state.theme == 'dark':
        return {
            'bg': '#0e1117',
            'paper_bg': '#262730',
            'text': '#fafafa',
            'grid': '#3b3b3b'
        }
    else:
        return {
            'bg': '#ffffff',
            'paper_bg': '#f0f2f6',
            'text': '#31333F',
            'grid': '#e1e4e8'
        }

theme_colors = get_theme_colors()

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

st.title("📈 Market Trends & Analysis")
st.markdown("Analyze AI/ML job market trends and insights")

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
    
    company_sizes = ['Startup (1-50)', 'Small (51-200)', 'Medium (201-1000)', 
                     'Large (1001-5000)', 'Enterprise (5000+)']
    
    locations = list(countries_currencies.keys())
    n_samples = 2000
    
    experience_levels = np.random.choice(['Junior', 'Mid-Level', 'Senior', 'Lead'], 
                                        n_samples, p=[0.25, 0.35, 0.30, 0.10])
    
    location_list = np.random.choice(locations, n_samples)
    currencies = [countries_currencies[loc] for loc in location_list]
    
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
    
    def categorize_work_type(ratio, hybrid_min, hybrid_max):
        if ratio == 0:
            return 'On-site'
        elif ratio == 100:
            return 'Remote'
        elif hybrid_min <= ratio <= hybrid_max:
            return 'Hybrid'
        else:
            return 'On-site' if ratio < hybrid_min else 'Remote'
    
    work_types = [categorize_work_type(r, st.session_state.hybrid_min, st.session_state.hybrid_max) 
                  for r in remote_ratios]
    
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
        'skills': [', '.join(np.random.choice(['Python', 'TensorFlow', 'PyTorch', 'SQL', 'AWS', 
                    'Docker', 'Kubernetes', 'Scikit-learn', 'R', 'Spark'], 
                    size=np.random.randint(2, 6), replace=False)) for _ in range(n_samples)],
        'posted_date': pd.date_range(start='2024-10-01', periods=n_samples, freq='3H')
    })
    
    return data

df = load_data()

target_currency = st.session_state.default_currency
df['salary_target'] = df['salary_usd'].apply(lambda x: convert_to_target_currency(x, target_currency))

# Monthly trends
st.subheader("📊 Job Postings Trend (Oct 2024 - Jul 2025)")
df['month'] = df['posted_date'].dt.to_period('M').astype(str)
monthly_counts = df.groupby('month').size().reset_index(name='count')

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly_counts['month'],
    y=monthly_counts['count'],
    mode='lines+markers',
    name='Job Postings',
    line=dict(color='#3B82F6', width=3),
    marker=dict(size=8)
))

fig.update_layout(
    xaxis_title='Month',
    yaxis_title='Number of Postings',
    height=400,
    hovermode='x unified',
    plot_bgcolor=theme_colors['paper_bg'],
    paper_bgcolor=theme_colors['bg'],
    font=dict(color=theme_colors['text']),
    xaxis=dict(gridcolor=theme_colors['grid']),
    yaxis=dict(gridcolor=theme_colors['grid'])
)
st.plotly_chart(fig, use_container_width=True)

# Theme colors for borders
def get_border_color():
    return '#4B5563' if st.session_state.theme == 'dark' else '#D1D5DB'

def get_paper_bg():
    return '#262730' if st.session_state.theme == 'dark' else '#f0f2f6'

# Custom CSS for metric cards with borders
st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: bold;
}
[data-testid="stMetric"] {
    background-color: """ + get_paper_bg() + """;
    border: 2px solid """ + get_border_color() + """;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Key insights
col1, col2, col3 = st.columns(3)
with col1:
    growth_rate = ((monthly_counts['count'].iloc[-1] - monthly_counts['count'].iloc[0]) / monthly_counts['count'].iloc[0] * 100)
    st.metric("Total Growth", f"{growth_rate:.1f}%", f"{monthly_counts['count'].iloc[-1] - monthly_counts['count'].iloc[0]} jobs")
with col2:
    peak_month = monthly_counts.loc[monthly_counts['count'].idxmax(), 'month']
    peak_count = monthly_counts['count'].max()
    st.metric("Peak Month", peak_month, f"{peak_count} postings")
with col3:
    avg_monthly = monthly_counts['count'].mean()
    st.metric("Avg Monthly", f"{avg_monthly:.0f}", "postings")

st.divider()

# Work type trends
st.subheader("🏢 Work Type Evolution")
df_work_time = df.groupby(['month', 'work_type']).size().reset_index(name='count')

fig = px.area(df_work_time, 
              x='month', 
              y='count', 
              color='work_type',
              labels={'count': 'Number of Jobs', 'month': 'Month', 'work_type': 'Work Type'},
              color_discrete_map={'Remote': '#10B981', 'Hybrid': '#F59E0B', 'On-site': '#3B82F6'})
fig.update_layout(
    height=400,
    plot_bgcolor=theme_colors['paper_bg'],
    paper_bgcolor=theme_colors['bg'],
    font=dict(color=theme_colors['text']),
    xaxis=dict(gridcolor=theme_colors['grid']),
    yaxis=dict(gridcolor=theme_colors['grid'])
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Skills demand
st.subheader("💻 Most In-Demand Skills")
all_skills = []
for skills in df['skills']:
    all_skills.extend([s.strip() for s in skills.split(',')])

skills_count = pd.Series(all_skills).value_counts().reset_index()
skills_count.columns = ['skill', 'count']
skills_count['percentage'] = (skills_count['count'] / len(df) * 100).round(1)

fig = px.bar(skills_count.head(10), 
             y='skill', 
             x='percentage',
             orientation='h',
             text='percentage',
             labels={'percentage': 'Percentage of Jobs (%)', 'skill': 'Skill'},
             color='percentage',
             color_continuous_scale='Viridis')
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color=theme_colors['text']))
fig.update_layout(
    height=400,
    showlegend=False,
    plot_bgcolor=theme_colors['paper_bg'],
    paper_bgcolor=theme_colors['bg'],
    font=dict(color=theme_colors['text']),
    xaxis=dict(gridcolor=theme_colors['grid']),
    yaxis=dict(gridcolor=theme_colors['grid'])
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Skills co-occurrence
st.subheader("🔗 Skills Co-occurrence Analysis")

top_skills = skills_count.head(8)['skill'].tolist()
cooccurrence = pd.DataFrame(0, index=top_skills, columns=top_skills)

for skills_str in df['skills']:
    skills_list = [s.strip() for s in skills_str.split(',')]
    for skill1 in top_skills:
        if skill1 in skills_list:
            for skill2 in top_skills:
                if skill2 in skills_list:
                    cooccurrence.loc[skill1, skill2] += 1

fig = px.imshow(cooccurrence,
                labels=dict(x="Skill", y="Skill", color="Co-occurrences"),
                x=top_skills,
                y=top_skills,
                color_continuous_scale='YlOrRd',
                text_auto=True)
fig.update_layout(
    height=500,
    plot_bgcolor=theme_colors['paper_bg'],
    paper_bgcolor=theme_colors['bg'],
    font=dict(color=theme_colors['text'])
)
# Make text black for visibility on yellow-orange-red scale
fig.update_traces(textfont=dict(color='black', size=12))
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Salary trends
st.subheader(f"💰 Salary Trends by Experience Level ({target_currency})")

salary_trends = df.groupby(['month', 'experience_level'])['salary_target'].mean().reset_index()

fig = px.line(salary_trends,
              x='month',
              y='salary_target',
              color='experience_level',
              markers=True,
              labels={'salary_target': f'Average Salary ({target_currency})', 'month': 'Month', 'experience_level': 'Experience Level'},
              color_discrete_map={'Junior': '#3B82F6', 'Mid-Level': '#10B981', 'Senior': '#F59E0B', 'Lead': '#EF4444'})
fig.update_layout(
    height=400,
    plot_bgcolor=theme_colors['paper_bg'],
    paper_bgcolor=theme_colors['bg'],
    font=dict(color=theme_colors['text']),
    xaxis=dict(gridcolor=theme_colors['grid']),
    yaxis=dict(gridcolor=theme_colors['grid'])
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Remote work analysis
st.subheader("🌐 Remote Work Ratio Distribution")

fig = px.histogram(df,
                   x='remote_ratio',
                   nbins=20,
                   labels={'remote_ratio': 'Remote Work Percentage', 'count': 'Number of Jobs'},
                   color_discrete_sequence=['#3B82F6'])
fig.add_vline(x=st.session_state.hybrid_min, line_dash="dash", line_color="orange", 
              annotation_text=f"Hybrid min: {st.session_state.hybrid_min}%")
if st.session_state.hybrid_max != st.session_state.hybrid_min:
    fig.add_vline(x=st.session_state.hybrid_max, line_dash="dash", line_color="orange", 
                  annotation_text=f"Hybrid max: {st.session_state.hybrid_max}%")
fig.update_layout(
    height=400,
    plot_bgcolor=theme_colors['paper_bg'],
    paper_bgcolor=theme_colors['bg'],
    font=dict(color=theme_colors['text']),
    xaxis=dict(gridcolor=theme_colors['grid']),
    yaxis=dict(gridcolor=theme_colors['grid'])
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8rem;'>
    <p>© 2025 Mohammadreza Hendiani</p>
</div>
""", unsafe_allow_html=True)