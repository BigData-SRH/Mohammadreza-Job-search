# Deployment Guide for Streamlit Cloud

This guide explains how to deploy the AI Job Market Explorer to Streamlit Cloud with secure Kaggle dataset access.

## Prerequisites

1. GitHub account
2. Kaggle account
3. Streamlit Cloud account (free at https://streamlit.io/cloud)

## Setup Steps

### 1. Get Kaggle API Credentials

1. Log in to your Kaggle account
2. Go to **Account Settings**: https://www.kaggle.com/settings
3. Scroll to **API** section
4. Click **"Create New API Token"**
5. Save the downloaded `kaggle.json` file (contains username and key)

**IMPORTANT:** Never commit `kaggle.json` to Git! It's already in `.gitignore`.

### 2. Set Up Local Secrets (Optional - for local testing)

Create `.streamlit/secrets.toml` in your project root:

```toml
[kaggle]
username = "your_kaggle_username"
key = "your_kaggle_api_key_from_kaggle_json"
```

Replace with your actual credentials from `kaggle.json`.

**IMPORTANT:** This file is in `.gitignore` and will NOT be committed.

### 3. Push Code to GitHub

```bash
# Ensure sensitive files are ignored
git status  # Should NOT show kaggle.json or secrets.toml

# Add and commit your changes
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 4. Deploy to Streamlit Cloud

#### Option A: Deploy from Streamlit Cloud Dashboard

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository
5. Set **Main file path** to: `Dashboard.py`
6. Click **"Deploy"**

#### Option B: Deploy with URL

Visit: `https://share.streamlit.io/deploy?repository=BigData-SRH/Mohammadreza-Job-search&branch=main&mainModule=Dashboard.py`

### 5. Add Secrets to Streamlit Cloud (CRITICAL STEP)

After deploying, you MUST add your Kaggle credentials as secrets:

1. Go to your app dashboard on Streamlit Cloud
2. Click **"Settings"** (⚙️ icon)
3. Click **"Secrets"**
4. Add your Kaggle credentials in TOML format:

```toml
[kaggle]
username = "your_kaggle_username"
key = "your_kaggle_api_key"
```

5. Click **"Save"**
6. Your app will automatically restart with the new secrets

### 6. Verify Deployment

Your app will:
1. Try to load dataset from `data/ai_job_dataset.csv` (if exists)
2. If not found, download from Kaggle using API credentials
3. Cache the data for 1 hour for better performance

## Architecture Options

### Option 1: Auto-Download from Kaggle (Implemented)

**Pros:**
- No manual data upload needed
- Always uses latest dataset from Kaggle
- Secure (credentials in Streamlit secrets)

**Cons:**
- First load might be slower (downloads dataset)
- Requires Kaggle API access

**How it works:**
- Uses `utils/data_loader.py` helper
- Downloads dataset on first run
- Caches for subsequent requests

### Option 2: Include Dataset in Repo (Alternative)

If you prefer to include the dataset in your repository:

1. Remove `data/` and `*.csv` from `.gitignore`
2. Add the dataset file to `data/ai_job_dataset.csv`
3. Commit and push to GitHub
4. Dataset will be included in deployment

**Pros:**
- Faster initial load
- No Kaggle API needed

**Cons:**
- Larger repository size
- Must manually update dataset
- Not ideal for large files (GitHub has 100MB file limit)

### Option 3: Use GitHub Releases for Large Files

For datasets > 25MB:

1. Create a GitHub Release
2. Attach dataset as release asset
3. Download from release URL in code

## Using the Data Loader

The new `utils/data_loader.py` module handles dataset loading automatically:

```python
from utils.data_loader import load_dataset

# This will automatically download from Kaggle if needed
df = load_dataset()
```

## Troubleshooting

### "Dataset file not found" Error

**Solution:** Ensure you've added Kaggle secrets in Streamlit Cloud settings.

### "Kaggle credentials not found" Error

**Solution:**
1. Check that secrets are properly formatted in TOML
2. Restart the app from Streamlit Cloud dashboard

### "Permission denied" from Kaggle API

**Solution:**
1. Verify your Kaggle API token is valid
2. Ensure the dataset is public on Kaggle
3. Check your Kaggle account has API access enabled

### Dataset Not Downloading

**Solution:**
1. Check the dataset identifier is correct: `pratyushpuri/global-ai-job-market-trend-2025`
2. Ensure you have accepted the dataset terms on Kaggle
3. Check Streamlit Cloud logs for specific error messages

## Security Best Practices

✅ **DO:**
- Store credentials in Streamlit secrets
- Keep `kaggle.json` out of version control
- Use `.gitignore` for sensitive files

❌ **DON'T:**
- Commit `kaggle.json` to Git
- Hardcode credentials in code
- Share your API key publicly

## Monitoring

Once deployed, you can:
- View app logs in Streamlit Cloud dashboard
- Monitor resource usage
- See visitor analytics
- Check for errors in real-time

## Updating the App

To update your deployed app:

```bash
# Make changes locally
git add .
git commit -m "Your update message"
git push origin main
```

Streamlit Cloud will automatically detect changes and redeploy!

## Alternative: Local Dataset

If you want to avoid Kaggle API entirely:

1. Download dataset manually from Kaggle
2. Place in `data/ai_job_dataset.csv`
3. Remove `kaggle>=1.5.16` from `requirements.txt`
4. The app will use the local file

## Cost

- Streamlit Cloud: **FREE** (for public apps)
- Kaggle API: **FREE**
- GitHub: **FREE** (for public repos)

**Total Cost: $0** 🎉

## Support

- Streamlit Docs: https://docs.streamlit.io/
- Kaggle API Docs: https://www.kaggle.com/docs/api
- GitHub Issues: Report problems in your repo's Issues tab
