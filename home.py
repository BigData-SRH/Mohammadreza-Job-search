# Home.py - Main Dashboard Page
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(
    page_title="AI/ML Job Market Explorer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for theming
def load_css():
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: var(--secondary-background-color);
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Title
st.title("🤖 AI/ML Job Market Explorer")
st.markdown("Discover insights from 2,000+ AI/ML job postings (Oct 2024 - Jul 2025)")

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

# Load or create sample data
@st.cache_data
def load_data():
    np.random.seed(42)
    
    # Create sample data with currencies
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
    
    # Generate base salaries in local currencies with realistic ranges per experience
    location_list = np.random.choice(locations, n_samples)
    currencies = [countries_currencies[loc] for loc in location_list]
    
    # Salary multipliers by experience
    exp_multipliers = {
        'Junior': (0.6, 0.8),
        'Mid-Level': (0.8, 1.1),
        'Senior': (1.2, 1.6),
        'Lead': (1.7, 2.2)
    }
    
    # Base salary ranges per currency (mid-level baseline)
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
        
        # Apply experience multiplier
        min_sal = int(min_base * mult_min)
        max_sal = int(max_base * mult_max)
        
        local_salary = np.random.randint(min_sal, max_sal)
        salaries_local.append(local_salary)
        salaries_usd.append(local_salary * CURRENCY_RATES[curr])
    
    # Generate remote ratio with more realistic distribution
    # More jobs at extremes (0%, 50%, 100%)
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
    
    # Determine work type: only 50% is hybrid, 0 is on-site, 100 is remote
    work_types = []
    for ratio in remote_ratios:
        if ratio == 0:
            work_types.append('On-site')
        elif ratio == 100:
            work_types.append('Remote')
        elif ratio == 50:
            work_types.append('Hybrid')
        else:
            # For other values between 1-99 (excluding 50), categorize based on proximity
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
        'posted_date': pd.date_range(start='2024-10-01', periods=n_samples, freq='3H')
    })
    
    return data

df = load_data()

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_salary = df['salary_usd'].mean()
    st.metric("Avg Salary (USD)", f"${avg_salary/1000:.0f}K", "+8%")

with col2:
    total_jobs = len(df)
    st.metric("Total Jobs", f"{total_jobs:,}", "")

with col3:
    remote_pct = (df['work_type'] == 'Remote').sum() / len(df) * 100
    st.metric("Remote Jobs", f"{remote_pct:.1f}%", "")

with col4:
    hybrid_pct = (df['work_type'] == 'Hybrid').sum() / len(df) * 100
    st.metric("Hybrid Jobs", f"{hybrid_pct:.1f}%", "")

st.divider()

# Main visualizations
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💰 Salary Distribution by Experience Level")
    
    # Box plot for salary distribution
    fig = go.Figure()
    
    exp_order = ['Junior', 'Mid-Level', 'Senior', 'Lead']
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
    
    for exp, color in zip(exp_order, colors):
        exp_data = df[df['experience_level'] == exp]['salary_usd']
        fig.add_trace(go.Box(
            y=exp_data,
            name=exp,
            marker_color=color,
            boxmean='sd'
        ))
    
    fig.update_layout(
        yaxis_title='Salary (USD)',
        xaxis_title='Experience Level',
        height=350,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Job Title Distribution")
    
    job_dist = df['job_title'].value_counts().reset_index()
    job_dist.columns = ['job_title', 'count']
    
    # Horizontal bar chart instead of pie for better readability
    fig = px.bar(job_dist, 
                 y='job_title', 
                 x='count',
                 orientation='h',
                 color='count',
                 color_continuous_scale='Blues')
    fig.update_layout(
        height=350,
        showlegend=False,
        xaxis_title='Number of Jobs',
        yaxis_title='Job Title'
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🏢 Work Type Distribution")
    
    work_type_dist = df['work_type'].value_counts().reset_index()
    work_type_dist.columns = ['work_type', 'count']
    work_type_dist['percentage'] = (work_type_dist['count'] / work_type_dist['count'].sum() * 100).round(1)
    
    # Donut chart for work type
    fig = px.pie(work_type_dist, 
                 values='count', 
                 names='work_type',
                 hole=0.4,
                 color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🌍 Jobs by Country")
    
    loc_dist = df['location'].value_counts().reset_index()
    loc_dist.columns = ['location', 'count']
    loc_dist['percentage'] = (loc_dist['count'] / loc_dist['count'].sum() * 100).round(1)
    
    # Lollipop chart - clean and data science appropriate
    fig = go.Figure()
    
    # Sort by count
    loc_dist = loc_dist.sort_values('count', ascending=True)
    
    # Add stems
    for idx, row in loc_dist.iterrows():
        fig.add_trace(go.Scatter(
            x=[0, row['count']],
            y=[row['location'], row['location']],
            mode='lines',
            line=dict(color='lightgray', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add circles
    fig.add_trace(go.Scatter(
        x=loc_dist['count'],
        y=loc_dist['location'],
        mode='markers+text',
        marker=dict(size=12, color='#3B82F6'),
        text=[f"{p:.1f}%" for p in loc_dist['percentage']],
        textposition='middle right',
        showlegend=False,
        hovertemplate='<b>%{y}</b><br>Jobs: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        height=300,
        xaxis_title='Number of Jobs',
        yaxis_title='',
        margin=dict(l=0, r=80, t=20, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Salary comparison across currencies
st.subheader("💱 Average Salary by Country (USD Equivalent)")

salary_by_location = df.groupby(['location', 'currency']).agg({
    'salary_usd': 'mean'
}).reset_index()

salary_by_location = salary_by_location.sort_values('salary_usd', ascending=True)

# Simple horizontal bar chart showing USD equivalent only
fig = go.Figure()

fig.add_trace(go.Bar(
    y=salary_by_location['location'],
    x=salary_by_location['salary_usd'],
    orientation='h',
    text=[f"${sal:,.0f}" for sal in salary_by_location['salary_usd']],
    textposition='auto',
    marker=dict(
        color=salary_by_location['salary_usd'],
        colorscale='Blues',
        showscale=False
    ),
    hovertemplate='<b>%{y}</b><br>Avg Salary: $%{x:,.0f}<extra></extra>'
))

fig.update_layout(
    xaxis_title='Average Salary (USD)',
    yaxis_title='Country',
    height=350,
    margin=dict(l=0, r=20, t=20, b=40)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8rem;'>
    <p>AI/ML Job Market Dashboard | Data: 2,000+ postings (Oct 2024 - Jul 2025) | Built with Streamlit</p>
    <p>© 2025 Mohammadreza Hendiani | Licensed under CC BY-SA 4.0</p>
</div>
""", unsafe_allow_html=True)