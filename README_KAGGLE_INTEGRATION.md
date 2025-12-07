# Kaggle Dataset Integration - Complete Solution

This document explains how your Streamlit app securely connects to Kaggle without exposing credentials or committing the database to your repository.

## 🎯 Solution Overview

Your setup uses **Streamlit Secrets Management** to securely store Kaggle API credentials:

```
Local Development: kaggle.json → setup_secrets.py → .streamlit/secrets.toml → App
Streamlit Cloud:   Manual entry in Secrets UI → App
```

**Key Benefits:**
✅ No credentials in code or Git
✅ No dataset in repository
✅ Automatic dataset download from Kaggle
✅ Secure deployment to Streamlit Cloud

---

## 📁 Project Structure

```
Mohammadreza-Job-search/
├── Dashboard.py                    # Main app
├── pages/
│   └── 01_Search_Jobs.py          # Search page
├── utils/
│   └── data_loader.py             # 🔑 Kaggle dataset loader
├── .streamlit/
│   ├── secrets.toml               # 🔒 LOCAL ONLY (in .gitignore)
│   └── secrets.toml.example       # Template (safe to commit)
├── data/                          # 🔒 Ignored (in .gitignore)
│   └── ai_job_dataset.csv         # Downloaded automatically
├── setup_secrets.py               # Setup helper
├── verify_setup.py                # Verification tool
├── KAGGLE_SETUP.md                # Quick reference
├── DEPLOYMENT.md                  # Full deployment guide
├── .gitignore                     # Security configuration
└── requirements.txt
```

### Security Files (🔒 = Never committed to Git)
- `kaggle.json` - Your Kaggle API credentials
- `.streamlit/secrets.toml` - Local secrets file
- `data/*.csv` - Dataset files

---

## 🚀 Quick Setup (3 Commands)

### For Local Development

```bash
# 1. Get Kaggle credentials and run setup
python setup_secrets.py

# 2. Verify setup is correct
python verify_setup.py

# 3. Run the app
streamlit run Dashboard.py
```

That's it! The app will automatically download the dataset from Kaggle.

---

## 🌐 Deploying to Streamlit Cloud

### Step 1: Verify Security Before Push

```bash
# Check what will be committed
python verify_setup.py

# Verify git status
git status

# These files should NOT appear:
# ❌ kaggle.json
# ❌ .streamlit/secrets.toml
# ❌ data/ai_job_dataset.csv
```

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click "New app"
3. Select repository: `BigData-SRH/Mohammadreza-Job-search`
4. Main file: `Dashboard.py`
5. Click "Deploy"

### Step 4: Add Secrets (CRITICAL!)

**In Streamlit Cloud app dashboard:**

1. Click **Settings** ⚙️
2. Click **Secrets**
3. Add your Kaggle credentials:

```toml
[kaggle]
username = "your_kaggle_username"
key = "your_kaggle_api_key"
```

4. Click **Save**

**Where to get these values?**
- Open your downloaded `kaggle.json` file
- Copy the `username` and `key` values

---

## 🔧 How It Works

### Data Loading Flow

```python
# In your Streamlit app
from utils.data_loader import load_dataset

df = load_dataset()  # That's it!
```

**Behind the scenes:**

1. **Check for local file** (`data/ai_job_dataset.csv`)
   - If exists → Use it
   - If not → Continue to step 2

2. **Check for Streamlit secrets**
   - If found → Use credentials to download from Kaggle
   - If not → Try local `~/.kaggle/kaggle.json`

3. **Download from Kaggle**
   - Authenticate with API
   - Download dataset: `pratyushpuri/global-ai-job-market-trend-2025`
   - Extract to `data/` directory
   - Cache for 1 hour

4. **Load and process**
   - Clean data
   - Add calculated fields
   - Return DataFrame

### Security Architecture

```
┌─────────────────────────────────────────────────────┐
│  Your Code (committed to Git)                      │
│  ✅ Dashboard.py                                    │
│  ✅ utils/data_loader.py                           │
│  ✅ .streamlit/secrets.toml.example                │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  Secrets (NOT in Git, .gitignore)                  │
│  🔒 .streamlit/secrets.toml (local)                │
│  🔒 Streamlit Cloud Secrets (cloud)                │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│  External Services                                  │
│  📊 Kaggle API → Dataset                           │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Utilities Provided

### 1. setup_secrets.py

Automatically creates `.streamlit/secrets.toml` from your `kaggle.json`:

```bash
python setup_secrets.py
```

**What it does:**
- Finds your `kaggle.json` file
- Creates `.streamlit/secrets.toml`
- Configures proper format for Streamlit

### 2. verify_setup.py

Verifies your setup is secure and complete:

```bash
python verify_setup.py
```

**Checks performed:**
- ✅ `.gitignore` configured correctly
- ✅ Kaggle credentials available
- ✅ Required packages in `requirements.txt`
- ✅ Data loader utility exists
- ✅ No sensitive files staged for commit

### 3. utils/data_loader.py

Core data loading module with automatic Kaggle download:

```python
from utils.data_loader import download_kaggle_dataset, load_dataset

# Just download
path = download_kaggle_dataset()

# Download + load + process
df = load_dataset()  # Cached for 1 hour
```

---

## 📋 Troubleshooting

### Problem: "Dataset file not found"

**Solution:**
```bash
# Option 1: Use Kaggle API (recommended)
python setup_secrets.py
streamlit run Dashboard.py

# Option 2: Manual download
# Download CSV from Kaggle
mkdir -p data
mv ~/Downloads/ai_job_dataset.csv data/
streamlit run Dashboard.py
```

### Problem: "Kaggle credentials not found"

**Local Development:**
```bash
# Check if kaggle.json exists
ls ~/.kaggle/kaggle.json

# If not, download from Kaggle:
# https://www.kaggle.com/settings → API → Create New API Token

# Then run setup
python setup_secrets.py
```

**Streamlit Cloud:**
1. Go to your app dashboard
2. Settings → Secrets
3. Add credentials in TOML format
4. Save and wait for restart

### Problem: "Permission denied" from Kaggle API

**Solutions:**

1. **Accept dataset terms:**
   - Visit: https://www.kaggle.com/datasets/pratyushpuri/global-ai-job-market-trend-2025
   - Click "Download" to accept terms

2. **Verify API token:**
   - Go to https://www.kaggle.com/settings
   - Revoke old token
   - Create new API token
   - Re-run `python setup_secrets.py`

3. **Check dataset is public:**
   - Ensure the dataset hasn't been made private

### Problem: Data not updating

**Solution:**
```bash
# Clear cached data
rm -rf data/ai_job_dataset.csv

# Restart app - will download fresh copy
streamlit run Dashboard.py
```

---

## 🔄 Updating to a Different Kaggle Dataset

To use a different dataset:

1. **Edit [utils/data_loader.py:12](./utils/data_loader.py#L12)**:

```python
def download_kaggle_dataset(dataset_id='your-username/your-dataset-name'):
```

2. **Update the expected filename if different**:

```python
dataset_path = 'data/your_dataset_name.csv'
```

3. **Update load_dataset() function** if data structure differs

---

## 🔐 Security Best Practices

### ✅ DO:
- Use Streamlit secrets for credentials
- Keep `.gitignore` updated
- Verify setup before pushing: `python verify_setup.py`
- Use the provided utility scripts
- Store `kaggle.json` in `~/.kaggle/` directory

### ❌ DON'T:
- Commit `kaggle.json` to Git
- Hardcode credentials in Python files
- Remove files from `.gitignore`
- Share your API key publicly
- Commit the dataset to the repository

---

## 📊 Alternative Approaches

### Option 1: Auto-Download (Current Implementation) ⭐ Recommended

**Pros:**
- ✅ No dataset in repo (smaller repo size)
- ✅ Always latest data from Kaggle
- ✅ Secure credential management

**Cons:**
- ⏱️ First load is slower (downloads dataset)
- 🔑 Requires Kaggle API setup

### Option 2: Commit Dataset to Repo

```bash
# Remove from .gitignore
sed -i '/data\//d' .gitignore
sed -i '/\*.csv/d' .gitignore

# Add dataset
git add data/ai_job_dataset.csv
git commit -m "Add dataset"
git push
```

**Pros:**
- ⚡ Faster initial load
- 🔓 No API credentials needed

**Cons:**
- 📦 Larger repository size
- 🔄 Must manually update data
- ⚠️ GitHub has 100MB file limit

### Option 3: GitHub Releases (For Large Files)

For datasets > 25MB:

```bash
# Create a release with dataset attached
gh release create v1.0.0 data/ai_job_dataset.csv

# Download in code from release URL
wget https://github.com/user/repo/releases/download/v1.0.0/ai_job_dataset.csv
```

---

## 📈 Performance Notes

- **First load:** 5-15 seconds (downloads from Kaggle)
- **Subsequent loads:** < 1 second (uses cached data)
- **Cache duration:** 1 hour (configurable in `@st.cache_data(ttl=3600)`)

To adjust cache duration, edit [utils/data_loader.py:87](./utils/data_loader.py#L87):

```python
@st.cache_data(ttl=7200)  # 2 hours instead of 1
```

---

## 📚 Documentation Reference

- **[KAGGLE_SETUP.md](./KAGGLE_SETUP.md)** - Quick reference guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Full deployment guide
- **[.streamlit/secrets.toml.example](./.streamlit/secrets.toml.example)** - Secrets template

---

## ✅ Final Checklist

Before deploying:

- [ ] Run `python verify_setup.py` - all checks pass
- [ ] Test locally: `streamlit run Dashboard.py`
- [ ] Verify no sensitive files in git: `git status`
- [ ] Push to GitHub: `git push origin main`
- [ ] Deploy on Streamlit Cloud
- [ ] Add secrets in Streamlit Cloud dashboard
- [ ] Test deployed app

---

## 💰 Cost

**Total Cost: $0** (Free!)

- Streamlit Cloud: FREE for public apps
- Kaggle API: FREE
- GitHub: FREE for public repos

---

## 🆘 Getting Help

If you encounter issues:

1. Run verification: `python verify_setup.py`
2. Check logs in Streamlit Cloud dashboard
3. Review [DEPLOYMENT.md](./DEPLOYMENT.md)
4. Check Streamlit docs: https://docs.streamlit.io/
5. Check Kaggle API docs: https://www.kaggle.com/docs/api

---

## 📝 Summary

Your app is now configured to:

✅ **Securely** connect to Kaggle API
✅ **Automatically** download datasets
✅ **Never** expose credentials
✅ **Not** commit large files to Git
✅ **Deploy** safely to Streamlit Cloud

**You can now safely push to GitHub and deploy to Streamlit Cloud!**

---

*Last updated: 2025-12-07*
