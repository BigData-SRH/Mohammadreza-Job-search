# pages/02_About.py
import streamlit as st

st.set_page_config(page_title="About", page_icon="information", layout="wide")

# Theme state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'default_currency' not in st.session_state:
    st.session_state.default_currency = 'USD'

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
        p, span, label { color: #e0e0e0 !important; }
        .stMarkdown { color: #e0e0e0 !important; }
        .stMarkdown p { color: #e0e0e0 !important; }
        .stMarkdown li { color: #e0e0e0 !important; }
        .stMarkdown strong { color: #fafafa !important; }

        /* Table in markdown */
        .stMarkdown table { background-color: #1a1a2a; border-collapse: collapse; }
        .stMarkdown th { background-color: #262730; color: #fafafa !important; border: 1px solid #3a3a4a; padding: 8px; }
        .stMarkdown td { background-color: #1a1a2a; color: #e0e0e0 !important; border: 1px solid #3a3a4a; padding: 8px; }
        .stMarkdown tr:nth-child(even) td { background-color: #202030; }

        /* Code blocks */
        .stMarkdown code {
            background-color: #1a1a2a !important;
            color: #7dd3fc !important;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .stMarkdown pre {
            background-color: #1a1a2a !important;
            border: 1px solid #3a3a4a;
            border-radius: 4px;
        }
        .stMarkdown pre code {
            background-color: transparent !important;
            color: #7dd3fc !important;
        }
        .stCodeBlock { background-color: #1a1a2a !important; }
        [data-testid="stCodeBlock"] { background-color: #1a1a2a !important; }
        [data-testid="stCodeBlock"] pre { background-color: #1a1a2a !important; }
        [data-testid="stCodeBlock"] code { color: #7dd3fc !important; }
        pre { background-color: #1a1a2a !important; color: #7dd3fc !important; }
        code { background-color: #1a1a2a !important; color: #7dd3fc !important; }

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

        /* Info box */
        .stAlert, [data-testid="stAlert"] {
            background-color: #1e3a5f !important;
            color: #e0e0e0 !important;
        }
        .stAlert p { color: #e0e0e0 !important; }
        [data-baseweb="notification"] { background-color: #1e3a5f !important; }

        /* Divider */
        hr { border-color: #3a3a4a !important; }
        [data-testid="stDivider"] { background-color: #3a3a4a; }

        /* Caption */
        .stCaption, [data-testid="stCaptionContainer"] { color: #a0a0b0 !important; }

        /* Links */
        a { color: #60a5fa !important; }
        a:hover { color: #93c5fd !important; }

        /* Image caption */
        [data-testid="stImage"] figcaption { color: #a0a0b0 !important; }
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

        /* Tables for light theme */
        .stMarkdown table { border-collapse: collapse; }
        .stMarkdown th { background-color: #f8f9fa; color: #1a1a2e !important; border: 1px solid #e2e8f0; padding: 8px; }
        .stMarkdown td { color: #2d3748 !important; border: 1px solid #e2e8f0; padding: 8px; }

        /* Info box light theme */
        .stAlert, [data-testid="stAlert"] {
            background-color: #e8f4fd !important;
            color: #1a1a2e !important;
        }
        </style>
        """, unsafe_allow_html=True)

apply_theme()

# Sidebar settings
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

st.title("About")

# Profile section
col1, col2 = st.columns([1, 3])

with col1:
    st.image(
        "https://avatars.githubusercontent.com/u/84578249",
        caption="Profile Picture",
        use_container_width=True
    )

with col2:
    st.markdown("## MOHAMMADREZA HENDIANI")
    st.markdown("**Bachelor in Computer Engineering | Master-Student in Informatik**")

st.divider()

# Contact information
st.subheader("Contact Information")

contact_col1, contact_col2 = st.columns(2)

with contact_col1:
    st.markdown("**Email**")
    st.markdown("[mohammad.r.hendiani@gmail.com](mailto:mohammad.r.hendiani@gmail.com)")

    st.markdown("**Website**")
    st.markdown("[hendiani.me](https://hendiani.me)")

with contact_col2:
    st.markdown("**LinkedIn**")
    st.markdown("[mohammadreza-hendiani](https://linkedin.com/in/mohammadreza-hendiani)")

    st.markdown("**GitHub**")
    st.markdown("[Man2Dev](https://github.com/Man2Dev)")

st.divider()

# About the dashboard
st.subheader("About This Dashboard")
st.markdown("""
The AI Job Market Explorer is an interactive data visualization dashboard designed to help job seekers,
researchers, and industry professionals understand the current state of the AI/ML job market.

**Purpose:**
This tool analyzes job postings to provide insights into salary trends, skill demands, geographic
distribution, and work arrangement preferences across the AI and machine learning industry. Whether
you're a job seeker looking to understand market rates or a hiring manager benchmarking positions,
this dashboard provides data-driven insights.

**Key Features:**
- **Market Overview**: Get a high-level view of job postings, average salaries, and work type distributions
- **Salary Analysis**: Compare salaries across experience levels, locations, and job titles
- **Skills Insights**: Discover the most in-demand technical skills in the industry
- **Job Search**: Filter and search through job listings based on your preferences
- **Currency Conversion**: View salaries in your preferred currency with real-time exchange rates
- **Data Export**: Download complete filtered data including all fields for further analysis
- **Theme Support**: Choose between light and dark themes for comfortable viewing
""")

st.divider()

# How it works
st.subheader("How It Works")
st.markdown("""
**Data Processing Pipeline:**

1. **Data Ingestion**: The dashboard loads job posting data from a CSV dataset containing information
   about AI/ML positions globally.

2. **Data Transformation**: Raw data is processed to standardize formats, calculate derived metrics
   (like USD-equivalent salaries), and categorize work types.

3. **Visualization**: Interactive charts built with Plotly allow you to explore the data from
   multiple angles. All salary-related visualizations clearly indicate when currency conversion
   has been applied and show the original currency where relevant.

4. **Real-time Currency Conversion**: Exchange rates are fetched and used to convert salaries
   for display (see Currency Conversion section below for details).

**Work Type Classification:**
- **On-site**: 0% remote work
- **Hybrid**: Any percentage between 0% and 100% remote work
- **Remote**: 100% remote work
""")

st.divider()

# Currency Conversion Section
st.subheader("Currency Conversion")
st.markdown("""
**API Provider: ExchangeRate-API**

This dashboard uses [ExchangeRate-API](https://www.exchangerate-api.com/) to fetch real-time currency
exchange rates for converting salaries from USD to your selected display currency.

**How it works:**

1. **API Endpoint**: The dashboard calls `https://api.exchangerate-api.com/v4/latest/USD` to fetch
   current exchange rates with USD as the base currency.

2. **Rate Caching**: Exchange rates are cached for 1 hour to minimize API calls and ensure fast
   page loads. After 1 hour, fresh rates are automatically fetched.

3. **Conversion Formula**: All salaries in the dataset are stored in USD. When you select a
   different display currency, the conversion is: `salary_display = salary_usd * exchange_rate`

4. **Fallback Rates**: If the API is unavailable, the dashboard uses fallback rates to ensure
   functionality (these may not reflect current market rates).

**Supported Currencies:**
| Currency | Code | Description |
|----------|------|-------------|
| US Dollar | USD | Base currency (no conversion needed) |
| Euro | EUR | European Union |
| British Pound | GBP | United Kingdom |
| Canadian Dollar | CAD | Canada |
| Australian Dollar | AUD | Australia |
| Indian Rupee | INR | India |
| Japanese Yen | JPY | Japan |

**Important Notes:**
- Original salaries are stored in USD in the dataset
- Charts and tables clearly indicate when conversion has been applied
- Hover over data points in charts to see additional currency information
- Downloaded CSV files include both original USD values and converted values
""")

st.divider()

# How to use
st.subheader("How to Use")
st.markdown("""
**Dashboard Page (Home):**

Navigate to the main dashboard to see an overview of the job market. Use the sidebar to change
currency or theme settings. Hover over charts for detailed information.

- All salary visualizations show converted values in your selected currency
- Captions below charts indicate when conversion from original currency has been applied
- The "Average Salary by Country" chart shows data converted from various local currencies

**Search Jobs Page:**

Use the filters at the top of the page to narrow down job listings based on:
- Work type (Remote, Hybrid, On-site)
- Career level
- Job type (Full-time, Part-time, etc.)
- Company Location (the country where the company is headquartered)
- Company size
- Minimum salary (in your selected display currency)
- Required skills

Click "Apply Filters" to filter results or "Clear Filters" to reset.

**Downloading Data:**

The "Download Filtered Data as CSV" button exports the **complete raw data** for all filtered jobs.
This includes:
- All fields shown in the table (job title, company, location, etc.)
- Fields NOT shown in the table: required_skills, posting_date, and more
- Original salary in USD (salary_usd column)
- Converted salary in your selected currency (salary_converted column)
- The currency used for conversion (converted_currency column)

This allows you to perform your own analysis on the complete dataset.

**Settings (Sidebar):**

All settings are accessible from the sidebar on any page:
- Theme toggle (Light/Dark)
- Currency selection (affects all salary displays)
- Reset all settings to defaults
""")

st.divider()

# Dataset information
st.subheader("Dataset Information")

st.markdown("""
**Source:** Global AI Job Market Trend 2025

**Description:** This dataset contains approximately 2,000+ AI/ML job postings collected between
October 2024 and July 2025. It includes information about job titles, companies, locations,
salaries, required skills, and work arrangements.

**Data Fields:**
| Field | Description |
|-------|-------------|
| job_title | Position title (e.g., Data Scientist, ML Engineer) |
| company_name | Hiring company name |
| company_location | Country where the company is located |
| company_size | Organization size (S=Small, M=Medium, L=Large, E=Enterprise) |
| experience_level | Required experience (EN=Entry, MI=Mid, SE=Senior, EX=Executive) |
| employment_type | Full-time (FT), Part-time (PT), Contract (CT), Freelance (FL) |
| salary_usd | Annual salary in USD (base currency for all conversions) |
| remote_ratio | Percentage of remote work allowed (0-100) |
| required_skills | Technical skills required for the position |
| posting_date | When the job was posted |

**Dataset Link:** [Global AI Job Market Trend 2025 on Kaggle](https://www.kaggle.com/datasets/pratyushpuri/global-ai-job-market-trend-2025)
""")

st.divider()

# Licensing
st.subheader("Licensing")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Project License: MIT License**

    This project's source code is licensed under the MIT License, which permits:
    - Commercial use
    - Modification
    - Distribution
    - Private use

    [View Project on GitHub](https://github.com/BigData-SRH/Mohammadreza-Job-search)
    """)

with col2:
    st.markdown("""
    **Dataset License: CC0 1.0 Universal**

    The dataset is released under CC0 1.0 Universal (Public Domain Dedication):
    - No rights reserved
    - Free to use for any purpose
    - No attribution required

    [View Dataset on Kaggle](https://www.kaggle.com/datasets/pratyushpuri/global-ai-job-market-trend-2025)
    """)

st.divider()

# Contributing & Bug Reports
st.subheader("Contributing and Bug Reports")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Report Bugs**

    Found a bug or have a suggestion? Please report it:

    1. Go to the [GitHub Issues page](https://github.com/BigData-SRH/Mohammadreza-Job-search/issues)
    2. Click "New Issue"
    3. Provide a clear description of the bug or suggestion
    4. Include steps to reproduce (if applicable)
    5. Add screenshots if helpful

    We appreciate all feedback!
    """)

with col2:
    st.markdown("""
    **Contribute**

    Want to contribute to the project?

    1. Fork the [repository](https://github.com/BigData-SRH/Mohammadreza-Job-search)
    2. Create a feature branch (`git checkout -b feature/YourFeature`)
    3. Make your changes
    4. Commit your changes (`git commit -m 'Add some feature'`)
    5. Push to the branch (`git push origin feature/YourFeature`)
    6. Open a Pull Request

    Please ensure your code follows the existing style.
    """)

st.divider()

# Technical Stack
st.subheader("Technical Stack")

st.markdown("""
This dashboard is built using the following technologies:

| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Core programming language |
| Streamlit | Web application framework |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computing |
| Plotly | Interactive visualizations |
| Requests | HTTP library for API calls |

**External APIs:**

| API | URL | Purpose |
|-----|-----|---------|
| ExchangeRate-API | https://api.exchangerate-api.com/v4/latest/USD | Real-time currency exchange rates |

**API Details:**
- Free tier available (no API key required for basic usage)
- Returns exchange rates with USD as base currency
- Rates updated daily by the API provider
- Dashboard caches rates for 1 hour to optimize performance
""")

st.divider()

# Requirements
st.subheader("Requirements")

st.code("""
streamlit>=1.37.0
pandas>=2.0.0
numpy>=1.24.0
pyarrow>=22.0.0
plotly
requests>=2.31.0
""", language="text")

st.markdown("""
To install all dependencies:
```bash
pip install -r requirements.txt
```

To run the application:
```bash
streamlit run app.py
```
""")

st.divider()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>2025 Mohammadreza Hendiani</p>
    <p>Project: MIT License | Dataset: CC0 1.0 Universal</p>
</div>
""", unsafe_allow_html=True)
