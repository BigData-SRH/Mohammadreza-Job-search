# pages/03_Settings.py
import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

# Initialize session state for settings
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'  # Default to light theme
if 'default_currency' not in st.session_state:
    st.session_state.default_currency = 'USD'
if 'hybrid_min' not in st.session_state:
    st.session_state.hybrid_min = 50
if 'hybrid_max' not in st.session_state:
    st.session_state.hybrid_max = 50

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

st.title("⚙️ Settings & Preferences")
st.markdown("Customize your dashboard experience")

st.divider()

# Theme Settings
st.subheader("🎨 Theme Settings")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("**Current Theme:**")
    theme_display = "🌙 Dark Mode" if st.session_state.theme == 'dark' else "☀️ Light Mode"
    st.info(theme_display)

with col2:
    st.markdown("**Change Theme:**")
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("🌙 Switch to Dark", use_container_width=True, 
                    disabled=(st.session_state.theme == 'dark')):
            st.session_state.theme = 'dark'
            st.success("Theme changed to Dark Mode")
            st.rerun()
    with theme_col2:
        if st.button("☀️ Switch to Light", use_container_width=True,
                    disabled=(st.session_state.theme == 'light')):
            st.session_state.theme = 'light'
            st.success("Theme changed to Light Mode")
            st.rerun()

st.divider()

# Currency Settings
st.subheader("💱 Currency Settings")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("**Current Default Currency:**")
    st.info(f"🪙 {st.session_state.default_currency}")

with col2:
    st.markdown("**Select Default Currency:**")
    st.markdown("All salaries will be converted to this currency across the dashboard.")
    
    currency_options = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'INR', 'JPY']
    currency_labels = {
        'USD': '🇺🇸 USD - US Dollar',
        'EUR': '🇪🇺 EUR - Euro',
        'GBP': '🇬🇧 GBP - British Pound',
        'CAD': '🇨🇦 CAD - Canadian Dollar',
        'AUD': '🇦🇺 AUD - Australian Dollar',
        'INR': '🇮🇳 INR - Indian Rupee',
        'JPY': '🇯🇵 JPY - Japanese Yen'
    }
    
    selected_currency = st.selectbox(
        "Choose currency",
        options=currency_options,
        format_func=lambda x: currency_labels[x],
        index=currency_options.index(st.session_state.default_currency),
        label_visibility="collapsed"
    )
    
    if st.button("💾 Save Currency Preference", use_container_width=True):
        st.session_state.default_currency = selected_currency
        st.success(f"✅ Default currency changed to {selected_currency}. Changes will apply after page refresh.")
        st.rerun()

st.divider()

# Hybrid Work Definition
st.subheader("🏢 Hybrid Work Definition")

st.markdown("""
Define what range of remote work percentage qualifies as "Hybrid" work. 
Jobs with remote ratios outside this range will be classified as either "On-site" or "Remote".
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Current Definition:**")
    if st.session_state.hybrid_min == st.session_state.hybrid_max:
        st.info(f"Exactly {st.session_state.hybrid_min}% remote = Hybrid")
    else:
        st.info(f"{st.session_state.hybrid_min}% - {st.session_state.hybrid_max}% remote = Hybrid")
    
    st.markdown("**Classification:**")
    st.markdown(f"- 0% remote → On-site")
    st.markdown(f"- {st.session_state.hybrid_min}%-{st.session_state.hybrid_max}% remote → Hybrid")
    st.markdown(f"- 100% remote → Remote")

with col2:
    st.markdown("**Customize Definition:**")
    
    # Preset options
    current_preset = 'Strict (50% only)' if (st.session_state.hybrid_min == 50 and st.session_state.hybrid_max == 50) else \
                     'Moderate (40-60%)' if (st.session_state.hybrid_min == 40 and st.session_state.hybrid_max == 60) else \
                     'Flexible (30-70%)' if (st.session_state.hybrid_min == 30 and st.session_state.hybrid_max == 70) else 'Custom'
    
    preset = st.radio(
        "Choose a preset or customize:",
        options=['Strict (50% only)', 'Moderate (40-60%)', 'Flexible (30-70%)', 'Custom'],
        index=['Strict (50% only)', 'Moderate (40-60%)', 'Flexible (30-70%)', 'Custom'].index(current_preset)
    )
    
    if preset == 'Strict (50% only)':
        hybrid_min = 50
        hybrid_max = 50
    elif preset == 'Moderate (40-60%)':
        hybrid_min = 40
        hybrid_max = 60
    elif preset == 'Flexible (30-70%)':
        hybrid_min = 30
        hybrid_max = 70
    else:  # Custom
        col_min, col_max = st.columns(2)
        with col_min:
            hybrid_min = st.number_input(
                "Min % Remote",
                min_value=1,
                max_value=99,
                value=min(max(st.session_state.hybrid_min, 1), 99),
                step=5,
                help="Minimum remote work percentage for hybrid classification (1-99%)"
            )
        with col_max:
            hybrid_max = st.number_input(
                "Max % Remote",
                min_value=1,
                max_value=99,
                value=min(max(st.session_state.hybrid_max, 1), 99),
                step=5,
                help="Maximum remote work percentage for hybrid classification (1-99%)"
            )
        
        if hybrid_min > hybrid_max:
            st.error("⚠️ Minimum cannot be greater than maximum!")
    
    if st.button("💾 Save Hybrid Definition", use_container_width=True):
        if hybrid_min <= hybrid_max:
            st.session_state.hybrid_min = hybrid_min
            st.session_state.hybrid_max = hybrid_max
            # Clear the data cache to force reload with new hybrid definition
            st.cache_data.clear()
            st.success(f"✅ Hybrid work definition updated: {hybrid_min}% - {hybrid_max}%. Navigate to other pages to see the updated plots.")
            st.rerun()
        else:
            st.error("Invalid range! Please adjust values.")

st.divider()

# Reset to Defaults
st.subheader("🔄 Reset Settings")

st.warning("This will reset all settings to their default values.")

if st.button("🔄 Reset All Settings to Default", use_container_width=True):
    st.session_state.theme = 'dark'
    st.session_state.default_currency = 'USD'
    st.session_state.hybrid_min = 50
    st.session_state.hybrid_max = 50
    st.success("✅ All settings have been reset to defaults!")
    st.rerun()

st.divider()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8rem;'>
    <p>Settings are stored in your session and will reset when you close the browser.</p>
    <p>© 2025 Mohammadreza Hendiani</p>
</div>
""", unsafe_allow_html=True)