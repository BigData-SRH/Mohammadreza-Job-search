# Architecture: Secure Kaggle Integration

This document visualizes how the secure Kaggle integration works.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         YOUR GITHUB REPOSITORY                      │
│                     (Public - No Secrets Here!)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📄 Dashboard.py                                                    │
│  📄 pages/01_Search_Jobs.py                                        │
│  📁 utils/                                                         │
│     └── 📄 data_loader.py  ← Core integration logic                │
│  📄 requirements.txt (includes: kaggle>=1.5.16)                    │
│  📄 .gitignore (protects: kaggle.json, secrets.toml, data/)       │
│  📄 setup_secrets.py                                               │
│  📄 verify_setup.py                                                │
│  📄 .streamlit/secrets.toml.example (template only)                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ git push
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      STREAMLIT CLOUD DEPLOYMENT                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🚀 Running App (Dashboard.py)                                     │
│      │                                                              │
│      ├─→ Imports utils/data_loader.py                              │
│      └─→ Calls load_dataset()                                      │
│                    │                                                │
│                    ↓                                                │
│  🔐 Streamlit Secrets (Settings → Secrets)                         │
│      [kaggle]                                                       │
│      username = "your_username"                                     │
│      key = "your_api_key"                                           │
│                    │                                                │
│                    ↓                                                │
│  📊 Data Loader Logic                                              │
│      1. Check if data/ai_job_dataset.csv exists                    │
│      2. If not, authenticate with Kaggle API                       │
│      3. Download dataset                                           │
│      4. Cache for 1 hour                                           │
│                    │                                                │
└────────────────────┼────────────────────────────────────────────────┘
                     │
                     │ HTTPS API Call
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│                           KAGGLE API                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📦 Dataset: pratyushpuri/global-ai-job-market-trend-2025          │
│                                                                     │
│  Returns: ai_job_dataset.csv                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

### Local Development Flow

```
Developer                  Local Machine                    Kaggle
    │                           │                              │
    │  1. Download kaggle.json  │                              │
    │◄──────────────────────────┼──────────────────────────────┤
    │                           │                              │
    │  2. Run setup_secrets.py  │                              │
    ├──────────────────────────►│                              │
    │                           │                              │
    │                    Creates ~/.kaggle/kaggle.json         │
    │                           │ OR                           │
    │                    .streamlit/secrets.toml               │
    │                           │                              │
    │  3. Run streamlit app     │                              │
    ├──────────────────────────►│                              │
    │                           │                              │
    │                    Reads secrets.toml                    │
    │                           │                              │
    │                           │  4. API request              │
    │                           ├─────────────────────────────►│
    │                           │                              │
    │                           │  5. Returns dataset          │
    │                           │◄─────────────────────────────┤
    │                           │                              │
    │                    Saves to data/                        │
    │                    Caches in memory                      │
    │                           │                              │
    │  6. App displays data     │                              │
    │◄──────────────────────────┤                              │
```

### Streamlit Cloud Deployment Flow

```
Developer              Streamlit Cloud              Kaggle
    │                        │                         │
    │  1. Push to GitHub     │                         │
    ├───────────────────────►│                         │
    │                        │                         │
    │  2. Deploy app         │                         │
    ├───────────────────────►│                         │
    │                        │                         │
    │  3. Add secrets (UI)   │                         │
    ├───────────────────────►│                         │
    │                        │                         │
    │              App starts & reads secrets          │
    │                        │                         │
    │              On first user visit:                │
    │                        │                         │
    │                        │  4. API request         │
    │                        ├────────────────────────►│
    │                        │                         │
    │                        │  5. Returns dataset     │
    │                        │◄────────────────────────┤
    │                        │                         │
    │              Caches in Streamlit cache           │
    │                        │                         │
    │  6. User sees app      │                         │
    │◄───────────────────────┤                         │
    │                        │                         │
    │              Subsequent users: uses cache        │
    │              (no Kaggle API call needed)         │
```

---

## 🔐 Security Layers

```
┌───────────────────────────────────────────────────────┐
│  Layer 1: Git Security (.gitignore)                   │
├───────────────────────────────────────────────────────┤
│  Prevents committing:                                 │
│  • kaggle.json                                        │
│  • .streamlit/secrets.toml                            │
│  • data/*.csv                                         │
└───────────────────────────────────────────────────────┘
                      │
                      ↓
┌───────────────────────────────────────────────────────┐
│  Layer 2: Streamlit Secrets Management                │
├───────────────────────────────────────────────────────┤
│  Secure storage:                                      │
│  • Encrypted at rest                                  │
│  • Not visible in logs                                │
│  • Isolated per app                                   │
│  • Accessed via st.secrets API only                   │
└───────────────────────────────────────────────────────┘
                      │
                      ↓
┌───────────────────────────────────────────────────────┐
│  Layer 3: Environment Variables                       │
├───────────────────────────────────────────────────────┤
│  Runtime only:                                        │
│  • KAGGLE_USERNAME (from secrets)                     │
│  • KAGGLE_KEY (from secrets)                          │
│  • Cleared after download                             │
└───────────────────────────────────────────────────────┘
                      │
                      ↓
┌───────────────────────────────────────────────────────┐
│  Layer 4: HTTPS Transport                             │
├───────────────────────────────────────────────────────┤
│  Secure communication:                                │
│  • TLS 1.2+ encryption                                │
│  • Certificate validation                             │
│  • No credential logging                              │
└───────────────────────────────────────────────────────┘
                      │
                      ↓
┌───────────────────────────────────────────────────────┐
│  Layer 5: Kaggle API Authentication                   │
├───────────────────────────────────────────────────────┤
│  Server-side validation:                              │
│  • API key verification                               │
│  • Rate limiting                                      │
│  • Access control                                     │
└───────────────────────────────────────────────────────┘
```

---

## 📦 Component Responsibilities

### 1. Dashboard.py / Pages
**Role:** User interface
**Security:** No credentials, no sensitive data

```python
# Clean code - no secrets!
from utils.data_loader import load_dataset
df = load_dataset()
```

### 2. utils/data_loader.py
**Role:** Data fetching and loading
**Security:** Uses st.secrets, no hardcoded credentials

```python
# Secure credential access
if 'kaggle' in st.secrets:
    os.environ['KAGGLE_USERNAME'] = st.secrets['kaggle']['username']
    os.environ['KAGGLE_KEY'] = st.secrets['kaggle']['key']
```

### 3. .gitignore
**Role:** Prevent credential leaks
**Security:** Blocks sensitive files from Git

```
kaggle.json
.streamlit/secrets.toml
data/
```

### 4. setup_secrets.py
**Role:** Local development helper
**Security:** Creates local secrets file (not committed)

```python
# Reads kaggle.json → Creates secrets.toml
```

### 5. verify_setup.py
**Role:** Pre-deployment validation
**Security:** Checks no secrets will be committed

```python
# Verifies .gitignore, checks git status
```

---

## 🔄 State Management

### App Startup Sequence

```
1. Streamlit starts
   │
   ├─→ Loads st.secrets from Streamlit Cloud
   │
2. User visits page
   │
   ├─→ Dashboard.py imports data_loader
   │
3. load_dataset() called
   │
   ├─→ Check: Does data/ai_job_dataset.csv exist?
   │   │
   │   NO ─→ Continue
   │   YES ─→ Load file, skip download
   │
4. download_kaggle_dataset() called
   │
   ├─→ Check: Are kaggle credentials available?
   │   │
   │   NO ─→ Error, show instructions
   │   YES ─→ Continue
   │
5. Authenticate with Kaggle API
   │
   ├─→ Set environment variables from secrets
   │
6. Download dataset
   │
   ├─→ api.dataset_download_files()
   │
7. Extract to data/
   │
8. Load into DataFrame
   │
   ├─→ pd.read_csv()
   │   Clean data
   │   Process columns
   │
9. Cache result (@st.cache_data)
   │
10. Return DataFrame to app
    │
11. App renders visualizations
```

---

## 🎯 Comparison: Different Approaches

### Approach 1: Current (Streamlit Secrets + Kaggle API) ⭐

```
GitHub Repo          Streamlit Cloud         Kaggle
    │                      │                    │
    │                      │                    │
    ├─ Code only ─────────►│                    │
    │  (no secrets)        │                    │
    │                      │                    │
    │                  Reads secrets            │
    │                      │                    │
    │                      ├─ API request ─────►│
    │                      │                    │
    │                      │◄─── Dataset ───────┤
    │                      │                    │
```

**Pros:** ✅ Secure, ✅ No large files in repo, ✅ Auto-updates
**Cons:** ⏱️ Initial download time

### Approach 2: Commit Dataset to Repo

```
GitHub Repo          Streamlit Cloud
    │                      │
    ├─ Code + Data ───────►│
    │  (large repo)        │
    │                      │
    │                  Reads local file
    │                      │
```

**Pros:** ⚡ Fast load
**Cons:** 📦 Large repo, 🔄 Manual updates, ⚠️ Size limits

### Approach 3: External Hosting (S3, etc.)

```
GitHub Repo      Streamlit Cloud      S3/CDN
    │                  │                 │
    ├─ Code ──────────►│                 │
    │  (no data)       │                 │
    │                  ├─ HTTP GET ─────►│
    │                  │                 │
    │                  │◄─── Dataset ────┤
```

**Pros:** ⚡ Fast, 📦 Small repo
**Cons:** 💰 Costs, 🔧 More setup

---

## 📊 Performance Characteristics

| Scenario | Time | Network | Storage |
|----------|------|---------|---------|
| First load (no cache) | 5-15s | ~10-50MB download | Temp cache |
| Cached load | <1s | 0 | In-memory |
| Cache expired (1hr) | 5-15s | ~10-50MB | Refresh cache |
| Local file exists | <1s | 0 | Local disk |

---

## 🔧 Configuration Points

### 1. Dataset ID
**Location:** [utils/data_loader.py:12](./utils/data_loader.py#L12)
```python
dataset_id='pratyushpuri/global-ai-job-market-trend-2025'
```

### 2. Cache Duration
**Location:** [utils/data_loader.py:87](./utils/data_loader.py#L87)
```python
@st.cache_data(ttl=3600)  # 1 hour
```

### 3. Data Path
**Location:** [utils/data_loader.py:23](./utils/data_loader.py#L23)
```python
dataset_path = 'data/ai_job_dataset.csv'
```

---

## 🚦 Error Handling Flow

```
load_dataset() called
    │
    ├─→ Try: download_kaggle_dataset()
    │       │
    │       ├─→ Try: Read st.secrets
    │       │       │
    │       │       ├─→ Success → Download
    │       │       │
    │       │       └─→ Error → Try ~/.kaggle/kaggle.json
    │       │                   │
    │       │                   ├─→ Success → Download
    │       │                   │
    │       │                   └─→ Error → Show instructions
    │       │
    │       └─→ Catch: Show error + help text
    │
    └─→ Return: DataFrame or None
```

---

## 🎓 Learning Resources

### For Understanding This Architecture

1. **Streamlit Secrets Management**
   - https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

2. **Kaggle API**
   - https://www.kaggle.com/docs/api

3. **Git Security Best Practices**
   - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure

4. **Environment Variables**
   - https://12factor.net/config

---

## 📝 Summary

This architecture provides:

✅ **Security:** Multiple layers protect credentials
✅ **Simplicity:** Automated download and caching
✅ **Flexibility:** Works locally and in cloud
✅ **Performance:** Intelligent caching reduces API calls
✅ **Maintainability:** Clear separation of concerns

**Key Innovation:** Using Streamlit's built-in secrets management eliminates the need for complex credential handling while maintaining security.

---

*Architecture designed for secure, efficient Kaggle dataset integration*
*Last updated: 2025-12-07*
