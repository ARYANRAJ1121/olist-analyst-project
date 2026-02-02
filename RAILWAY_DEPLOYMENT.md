# 🚂 Railway Deployment Guide

This guide will help you deploy your Olist Analytics Dashboard to Railway.

## 📋 Prerequisites

- A [Railway account](https://railway.app/) (free tier available)
- Your GitHub repository pushed with the latest changes
- Git installed on your machine

## 🚀 Deployment Steps

### 1. Push Your Code to GitHub

Make sure all the deployment files are committed:

```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Deploy on Railway

#### Option A: Deploy via Railway Dashboard (Recommended)

1. Go to [railway.app](https://railway.app/)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your `olist-analyst-project` repository
6. Railway will automatically detect the configuration

#### Option B: Deploy via Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. Configure Environment (if needed)

Railway should automatically detect your Streamlit app. If needed, you can set:

- **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- **Build Command:** `pip install -r requirements_dashboard.txt`

### 4. Access Your App

Once deployed, Railway will provide you with a public URL like:
`https://your-app-name.up.railway.app`

## 📁 Deployment Files Created

✅ **Procfile** - Tells Railway how to run your app
✅ **runtime.txt** - Specifies Python version (3.11.7)
✅ **.streamlit/config.toml** - Streamlit production configuration
✅ **requirements_dashboard.txt** - Updated with all dependencies

## 🔧 Configuration Details

### Procfile

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### runtime.txt

```
python-3.11.7
```

### .streamlit/config.toml

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## 🐛 Troubleshooting

### Issue: App won't start

**Solution:** Check Railway logs for missing dependencies. Add any missing packages to `requirements_dashboard.txt`

### Issue: Port binding error

**Solution:** Ensure the Procfile uses `$PORT` variable (already configured)

### Issue: Memory errors

**Solution:** Railway free tier has memory limits. Consider:

- Optimizing data loading in `app.py`
- Using Railway Pro plan for more resources

### Issue: Build timeout

**Solution:** Railway has build time limits. Your app should build quickly, but if not:

- Remove unused dependencies
- Use lighter package versions

## 💰 Pricing

- **Free Tier:** $5 credit/month (should be sufficient for this dashboard)
- **Pro Plan:** $20/month for unlimited usage

## 🔄 Continuous Deployment

Railway automatically redeploys when you push to your GitHub repository:

```bash
# Make changes to your code
git add .
git commit -m "Update dashboard features"
git push origin main
# Railway will automatically redeploy!
```

## 📊 Monitoring

Railway provides:

- Real-time logs
- Deployment history
- Resource usage metrics
- Custom domain support (Pro plan)

## 🌐 Custom Domain (Optional)

To add a custom domain:

1. Go to your Railway project settings
2. Click **"Domains"**
3. Add your custom domain
4. Update DNS records as instructed

## ✅ Post-Deployment Checklist

- [ ] App is accessible via Railway URL
- [ ] All visualizations load correctly
- [ ] Theme switching works
- [ ] Data explorer functions properly
- [ ] No console errors in browser
- [ ] Update README with new Railway URL

## 🔗 Useful Links

- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

---

**Need help?** Check Railway logs or reach out to Railway support!
