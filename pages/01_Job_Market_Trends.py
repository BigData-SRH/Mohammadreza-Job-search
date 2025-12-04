# pages/2_📈_Market_Trends.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Market Trends", page_icon="📈", layout="wide")

st.title("📈 Market Trends & Analysis")
st.markdown("Analyze AI/ML job market trends and insights")

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
        'posted_date': pd.date_range(start='2024-10-01', periods=n_samples, freq='3H')
    })
    
    return data

df = load_data()

# Monthly trends
st.subheader("📊 Job Postings Trend (Oct 2024 - Jul 2025)")
df['month'] = df['posted_date'].dt.to_period('M').astype(str)
monthly_counts = df.groupby('month').size().reset_index(name='count')

# Add trend line
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
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

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

# Work type trends over time
st.subheader("🏢 Work Type Evolution")
df_work_time = df.groupby(['month', 'work_type']).size().reset_index(name='count')

fig = px.area(df_work_time, 
              x='month', 
              y='count', 
              color='work_type',
              labels={'count': 'Number of Jobs', 'month': 'Month', 'work_type': 'Work Type'},
              color_discrete_map={'Remote': '#10B981', 'Hybrid': '#F59E0B', 'On-site': '#3B82F6'})
fig.update_layout(height=400)
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

# Horizontal bar chart for skills
fig = px.bar(skills_count.head(10), 
             y='skill', 
             x='percentage',
             orientation='h',
             text='percentage',
             labels={'percentage': 'Percentage of Jobs (%)', 'skill': 'Skill'},
             color='percentage',
             color_continuous_scale='Viridis')
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(height=400, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Skills combinations heatmap
st.subheader("🔗 Skills Co-occurrence Analysis")

# Get top 8 skills
top_skills = skills_count.head(8)['skill'].tolist()

# Create co-occurrence matrix
cooccurrence = pd.DataFrame(0, index=top_skills, columns=top_skills)

for skills_str in df['skills']:
    skills_list = [s.strip() for s in skills_str.split(',')]
    for skill1 in top_skills:
        if skill1 in skills_list:
            for skill2 in top_skills:
                if skill2 in skills_list:
                    cooccurrence.loc[skill1, skill2] += 1

# Heatmap
fig = px.imshow(cooccurrence,
                labels=dict(x="Skill", y="Skill", color="Co-occurrences"),
                x=top_skills,
                y=top_skills,
                color_continuous_scale='Blues',
                text_auto=True)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Salary trends by role over time
st.subheader("💰 Salary Trends by Experience Level")

salary_trends = df.groupby(['month', 'experience_level'])['salary_usd'].mean().reset_index()

fig = px.line(salary_trends,
              x='month',
              y='salary_usd',
              color='experience_level',
              markers=True,
              labels={'salary_usd': 'Average Salary (USD)', 'month': 'Month', 'experience_level': 'Experience Level'},
              color_discrete_map={'Junior': '#3B82F6', 'Mid-Level': '#10B981', 'Senior': '#F59E0B', 'Lead': '#EF4444'})
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Remote work analysis
st.subheader("🌐 Remote Work Ratio Distribution")

# Histogram of remote ratios
fig = px.histogram(df,
                   x='remote_ratio',
                   nbins=20,
                   labels={'remote_ratio': 'Remote Work Percentage', 'count': 'Number of Jobs'},
                   color_discrete_sequence=['#3B82F6'])
fig.add_vline(x=50, line_dash="dash", line_color="red", 
              annotation_text="50% (Hybrid threshold)", 
              annotation_position="top right")
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# Remote ratio by country
st.subheader("🗺️ Average Remote Ratio by Country")
remote_by_country = df.groupby('location')['remote_ratio'].mean().reset_index()
remote_by_country = remote_by_country.sort_values('remote_ratio', ascending=True)

fig = px.bar(remote_by_country,
             y='location',
             x='remote_ratio',
             orientation='h',
             labels={'remote_ratio': 'Average Remote Ratio (%)', 'location': 'Country'},
             color='remote_ratio',
             color_continuous_scale='RdYlGn')
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)