SOLANA AI Bot - Render.com Deployment Guide
Files Created for Deployment
render_requirements.txt - Python dependencies (rename to requirements.txt when uploading)
Procfile - Tells Render how to start your bot
main.py - Your bot application (already exists)
Step-by-Step Render.com Deployment
1. Prepare Your Files
Rename render_requirements.txt to requirements.txt
Ensure all your bot files are in the root directory
Your main application file is main.py
2. Create Render Account
Go to https://render.com
Sign up or log in
Connect your GitHub account
3. Upload to GitHub
Create a new repository on GitHub
Upload all your bot files including:
main.py
requirements.txt (renamed from render_requirements.txt)
Procfile
config.py
wallet_manager.py
balance_fetcher.py
menu_handlers.py
keyboard_layouts.py
utils.py
wallets.db
4. Deploy on Render
In Render dashboard, click "New +"
Select "Web Service"
Connect your GitHub repository
Configure deployment settings:
Name: solana-ai-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python main.py
Instance Type: Free (or paid for better performance)
5. Set Environment Variables
In Render dashboard under "Environment":

BOT_TOKEN: 7806926630:AAF_D_OcpkQtB9M5dH0iwk7QbwvTrdpglIA
SOLSCAN_API_KEY: (optional, leave empty if you don't have one)
SOLANA_RPC_URL: https://api.mainnet-beta.solana.com
6. Deploy
Click "Create Web Service"
Render will automatically build and deploy your bot
Monitor the build logs for any errors
Important Notes
Database: Your SQLite database (wallets.db) will be reset on each deployment
Logs: Check Render logs if the bot doesn't start
Free Tier: Bot may sleep after 15 minutes of inactivity on free tier
Paid Tier: Recommended for production use to avoid sleeping
Troubleshooting
If deployment fails:

Check build logs in Render dashboard
Verify all dependencies are in requirements.txt
Ensure main.py runs without errors locally
Check that BOT_TOKEN environment variable is set correctly
Cost
Free tier: $0/month (with limitations)
Starter tier: $7/month (recommended for production)
