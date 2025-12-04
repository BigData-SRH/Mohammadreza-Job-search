# pages/3_👤_About.py
import streamlit as st

st.set_page_config(page_title="About", page_icon="👤", layout="wide")

st.title("👤 About")

# Profile section
col1, col2 = st.columns([1, 3])

with col1:
    st.image("https://via.placeholder.com/200", caption="Profile Picture")

with col2:
    st.markdown("## MOHAMMADREZA HENDIANI")
    st.markdown("**Bachelor in Computer Engineering | Master-Student in Informatik**")
    st.markdown("📍 Leipzig, Germany (Ich bin berechtigt, in Deutschland zu arbeiten)")

st.divider()

# Contact information
st.subheader("📬 Contact Information")

contact_col1, contact_col2 = st.columns(2)

with contact_col1:
    st.markdown("**📧 Email**")
    st.markdown("[mohammad.r.hendiani@gmail.com](mailto:mohammad.r.hendiani@gmail.com)")
    
    st.markdown("**🌐 Website**")
    st.markdown("[hendiani.me](https://hendiani.me)")

with contact_col2:
    st.markdown("**💼 LinkedIn**")
    st.markdown("[mohammadreza-hendiani](https://linkedin.com/in/mohammadreza-hendiani)")
    
    st.markdown("**💻 GitHub**")
    st.markdown("[Man2Dev](https://github.com/Man2Dev)")

st.divider()

# About the dashboard
st.subheader("📊 About This Dashboard")
st.markdown("""
This AI/ML Job Market Explorer analyzes 2,000+ job postings from October 2024 to July 2025, 
providing insights into salary trends, skill demands, and market dynamics in the AI/ML field.

The dashboard is built using Streamlit and designed to help job seekers make informed decisions 
about their career path in the rapidly evolving AI/ML industry.
""")

st.divider()

# Data & Licensing
st.subheader("📜 Data & Licensing")
st.info("""
**Dataset:** Kaggle AI Jobs 2025 (~2K postings, Oct 2024–Jul 2025)  
**License:** CC BY-SA 4.0  
**Source:** Kaggle Dataset Repository
""")

st.divider()

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>© 2025 Mohammadreza Hendiani | Licensed under CC BY-SA 4.0</p>
</div>
""", unsafe_allow_html=True)