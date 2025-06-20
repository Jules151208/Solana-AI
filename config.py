"""
Configuration settings for SOLANA AI Bot
"""

import os

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "7806926630:AAF_D_OcpkQtB9M5dH0iwk7QbwvTrdpglIA")

# Database configuration
DATABASE_FILE = "wallets.db"

# SolScan API configuration
SOLSCAN_API_BASE = "https://api.solscan.io"
SOLSCAN_API_KEY = os.getenv("SOLSCAN_API_KEY", "")

# Solana RPC configuration
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

# Price API configuration
PRICE_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
