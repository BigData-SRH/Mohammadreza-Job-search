# AI Job Market Explorer

An interactive Streamlit dashboard for exploring AI/ML job market trends and insights.

## Overview

The AI Job Market Explorer analyzes 2,000+ AI/ML job postings from October 2024 to July 2025, providing valuable insights into:

- Salary trends across experience levels and locations
- Most in-demand technical skills
- Work type distributions (Remote, Hybrid, On-site)
- Geographic distribution of opportunities
- Monthly posting trends

## Features

- **Interactive Visualizations**: Explore data through dynamic Plotly charts
- **Job Search**: Filter jobs by work type, experience level, company location, skills, and more
- **Currency Conversion**: View salaries in 7 different currencies with real-time exchange rates
- **Complete Data Export**: Download filtered job data with ALL fields (including skills, dates, etc.) for further analysis
- **Theme Support**: Switch between light and dark themes

## Screenshots

The dashboard includes:
- Market overview with KPI metrics
- Salary distribution by experience level
- Job title and work type distributions
- Skills demand analysis
- Country-wise salary comparisons

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for cloning)

Check your versions:

```bash
python --version
pip --version
```

## Installation

### Option A: Clone the Repository

```bash
git clone https://github.com/BigData-SRH/Mohammadreza-Job-search.git
cd Mohammadreza-Job-search
```

### Option B: Download ZIP

1. Click "Code" then "Download ZIP"
2. Extract the ZIP file
3. Open the folder in your terminal

### Set Up Virtual Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Dataset

Download the dataset from Kaggle:

**Source:** [Global AI Job Market Trend 2025](https://www.kaggle.com/datasets/pratyushpuri/global-ai-job-market-trend-2025)

**License:** CC0 1.0 Universal (Public Domain)

1. Download the dataset from the link above
2. Extract the CSV file
3. Place it in the `data/` folder as `ai_job_dataset.csv`

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Navigation

- **Dashboard (Home)**: Market overview with trends and statistics
- **Search Jobs**: Filter and search job listings
- **About**: Documentation and project information

### Settings (Sidebar)

Available on all pages:
- **Theme**: Toggle between Light and Dark modes
- **Currency**: Select display currency (USD, EUR, GBP, CAD, AUD, INR, JPY)
- **Reset**: Reset all settings to defaults

### Downloading Data

The "Download Filtered Data as CSV" button on the Search Jobs page exports the **complete raw data** for all filtered jobs, including:

- All fields shown in the table (job title, company, location, etc.)
- Fields NOT shown in the table: `required_skills`, `posting_date`, and more
- Original salary in USD (`salary_usd` column)
- Converted salary in your selected currency (`salary_converted` column)
- The currency used for conversion (`converted_currency` column)

This allows you to perform your own analysis on the complete dataset.

## Currency Conversion

### API Provider

This dashboard uses [ExchangeRate-API](https://www.exchangerate-api.com/) to fetch real-time currency exchange rates.

### How It Works

1. **API Endpoint**: The dashboard calls `https://api.exchangerate-api.com/v4/latest/USD` to fetch current exchange rates with USD as the base currency.

2. **Rate Caching**: Exchange rates are cached for 1 hour to minimize API calls and ensure fast page loads. After 1 hour, fresh rates are automatically fetched.

3. **Conversion Formula**: All salaries in the dataset are stored in USD. When you select a different display currency:
   ```
   salary_display = salary_usd * exchange_rate
   ```

4. **Fallback Rates**: If the API is unavailable, the dashboard uses fallback rates to ensure functionality.

### Supported Currencies

| Currency | Code | Description |
|----------|------|-------------|
| US Dollar | USD | Base currency (no conversion needed) |
| Euro | EUR | European Union |
| British Pound | GBP | United Kingdom |
| Canadian Dollar | CAD | Canada |
| Australian Dollar | AUD | Australia |
| Indian Rupee | INR | India |
| Japanese Yen | JPY | Japan |

### Currency Display in Charts

- All salary visualizations clearly indicate when currency conversion has been applied
- Captions below charts show the conversion source (e.g., "Converted to EUR from original local currencies")
- Hover over data points to see additional currency information
- The "Average Salary by Country" chart shows the original currency for each country

## Project Structure

```
ai-job-explorer/
├── app.py                    # Main dashboard page
├── pages/
│   ├── 01_Search_Jobs.py    # Job search and filter page
│   └── 02_About.py          # Documentation and about page
├── data/
│   └── ai_job_dataset.csv   # Dataset (download separately)
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Work Type Classification

The dashboard categorizes jobs based on remote work percentage:
- **On-site**: 0% remote work
- **Hybrid**: Any percentage between 0% and 100%
- **Remote**: 100% remote work

## Data Fields

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

## Technical Stack

| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Core programming language |
| Streamlit | Web application framework |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computing |
| Plotly | Interactive visualizations |
| Requests | HTTP library for API calls |

### External APIs

| API | URL | Purpose |
|-----|-----|---------|
| ExchangeRate-API | https://api.exchangerate-api.com/v4/latest/USD | Real-time currency exchange rates |

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/YourFeature`)
6. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate documentation.

## Bug Reports

Found a bug or have a suggestion?

1. Go to [GitHub Issues](https://github.com/BigData-SRH/Mohammadreza-Job-search/issues)
2. Click "New Issue"
3. Provide a clear description
4. Include steps to reproduce (if applicable)
5. Add screenshots if helpful

## License

**Project Code:** MIT License

```
MIT License

Copyright (c) 2025 Mohammadreza Hendiani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Dataset:** CC0 1.0 Universal (Public Domain Dedication)

## Acknowledgments

- Dataset by [Pratyush Puri](https://www.kaggle.com/pratyushpuri) on Kaggle
- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/)
- Currency rates from [ExchangeRate-API](https://www.exchangerate-api.com/)

## Contact

**Mohammadreza Hendiani**

- Website: [hendiani.me](https://hendiani.me)
- LinkedIn: [mohammadreza-hendiani](https://linkedin.com/in/mohammadreza-hendiani)
- GitHub: [Man2Dev](https://github.com/Man2Dev)
