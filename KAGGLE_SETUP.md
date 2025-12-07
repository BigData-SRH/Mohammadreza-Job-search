# Quick Setup Guide: Connecting Kaggle Dataset

This is a **quick reference guide** for securely connecting your Kaggle dataset without exposing credentials.

## 🚀 Quick Start (3 Steps)

### 1. Get Kaggle Credentials

```bash
# Download your Kaggle API token from:
https://www.kaggle.com/settings
# Click "Create New API Token" in the API section
```

### 2. Run Setup Script

```bash
# Automatic setup (recommended)
python setup_secrets.py

# Or manual setup
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### 3. Run Streamlit App

```bash
streamlit run Dashboard.py
```

The app will automatically download the dataset from Kaggle on first run!

---

## 📋 Deployment to Streamlit Cloud

### Step 1: Push to GitHub (Without Credentials!)

```bash
# Verify sensitive files are NOT being committed
git status

# You should NOT see:
# - kaggle.json
# - .streamlit/secrets.toml
# - data/*.csv

# If you see them, they're already in .gitignore - good!

# Commit and push
git add .
git commit -m "Deploy app"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click "New app"
3. Select your repository: `BigData-SRH/Mohammadreza-Job-search`
4. Main file: `Dashboard.py`
5. Click "Deploy"

### Step 3: Add Secrets on Streamlit Cloud

**This is the critical step!**

1. In your deployed app, click **Settings** ⚙️
2. Click **Secrets**
3. Paste your Kaggle credentials in TOML format:

```toml
[kaggle]
username = "your_kaggle_username"
key = "your_kaggle_api_key_here"
```

4. Click **Save**
5. App will restart automatically

**Where to find these values?**
- Open the `kaggle.json` file you downloaded
- Copy the `username` and `key` values

---

## 🔒 Security Checklist

✅ **Already Protected** (files in `.gitignore`):
- ✅ `kaggle.json` - Kaggle API credentials
- ✅ `.streamlit/secrets.toml` - Local secrets
- ✅ `data/*.csv` - Dataset files

✅ **Safe to commit**:
- ✅ `setup_secrets.py` - Setup helper script
- ✅ `.streamlit/secrets.toml.example` - Template only
- ✅ `utils/data_loader.py` - Data loading logic
- ✅ All Python app files

---

## 🎯 How It Works

### Local Development
```
You → setup_secrets.py → .streamlit/secrets.toml → Streamlit App → Kaggle API → Dataset
```

### Streamlit Cloud Deployment
```
You → Streamlit Cloud Secrets UI → Streamlit App → Kaggle API → Dataset
```

### Key Features
- **No credentials in code** - Uses Streamlit secrets
- **No dataset in repo** - Downloaded automatically from Kaggle
- **Fallback support** - Works with local files if API unavailable
- **Caching** - Dataset cached for 1 hour for performance

---

## 🛠️ Troubleshooting

### Error: "Dataset file not found"

**Solution:**
```bash
# Option 1: Download manually and place in data/ folder
mkdir -p data
# Download from Kaggle and save as data/ai_job_dataset.csv

# Option 2: Configure Kaggle API
python setup_secrets.py
```

### Error: "Kaggle credentials not found"

**Local Development:**
```bash
python setup_secrets.py
```

**Streamlit Cloud:**
1. Go to app Settings → Secrets
2. Add your Kaggle credentials in TOML format
3. Save and wait for app to restart

### Error: "Permission denied" from Kaggle

**Solutions:**
1. Check that the Kaggle dataset is public
2. Visit the dataset page and accept terms if required:
   https://www.kaggle.com/datasets/pratyushpuri/global-ai-job-market-trend-2025
3. Verify your API token is valid (regenerate if needed)

---

## 📊 Alternative: Manual Dataset Upload

If you prefer not to use Kaggle API:

1. Download dataset from Kaggle manually
2. Place in `data/ai_job_dataset.csv`
3. The app will use the local file automatically

**Note:** Local files take precedence over API downloads.

---

## 🔄 Updating the Dataset

### Automatic (Recommended)
The app re-downloads the dataset every hour automatically.

### Manual
```bash
# Delete cached data
rm -rf data/ai_job_dataset.csv

# Restart app - will download fresh copy
streamlit run Dashboard.py
```

---

## 📚 Additional Resources

- [Detailed Deployment Guide](./DEPLOYMENT.md)
- [Streamlit Secrets Documentation](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- [Kaggle API Documentation](https://www.kaggle.com/docs/api)

---

## ❓ FAQ

**Q: Will my Kaggle credentials be exposed?**
A: No! They're stored securely in Streamlit secrets and never committed to Git.

**Q: Do I need to commit the dataset?**
A: No! The app downloads it automatically using Kaggle API.

**Q: What if I want to include the dataset in the repo?**
A: Remove `data/` and `*.csv` from `.gitignore`, add the file, and commit.

**Q: Is this free?**
A: Yes! Streamlit Cloud, Kaggle API, and GitHub are all free for public projects.

**Q: Can I use a different Kaggle dataset?**
A: Yes! Modify the dataset ID in [utils/data_loader.py:12](./utils/data_loader.py#L12)

---

**Need help?** Check [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive guide.
