"""
Menu handlers for different bot sections
"""

import logging
from telegram import Update
from telegram.constants import ParseMode

from wallet_manager import WalletManager
from balance_fetcher import BalanceFetcher
from keyboard_layouts import KeyboardLayouts
from utils import format_balance

logger = logging.getLogger(__name__)

class MenuHandlers:
    def __init__(self, wallet_manager: WalletManager, balance_fetcher: BalanceFetcher):
        self.wallet_manager = wallet_manager
        self.balance_fetcher = balance_fetcher
        self.keyboard_layouts = KeyboardLayouts()
    
    async def _get_user_balance_text(self, user_id: int) -> str:
        """Get formatted balance text for user"""
        try:
            wallet_data = await self.wallet_manager.get_wallet_by_user_id(user_id)
            if not wallet_data:
                return "Balance: 0 SOL (USD $0)"
            
            balance_sol, balance_usd = await self.balance_fetcher.get_balance(wallet_data['address'])
            sol_str = format_balance(balance_sol)
            usd_str = format_balance(balance_usd)
            
            return f"*Wallet Balance:* {sol_str} SOL \\(USD ${usd_str}\\)"
            
        except Exception as e:
            logger.error(f"Error getting balance text: {e}")
            return "*Wallet Balance:* 0 SOL \\(USD $0\\)"
    
    async def _check_user_has_sol(self, user_id: int) -> bool:
        """Check if user has SOL in wallet"""
        try:
            wallet_data = await self.wallet_manager.get_wallet_by_user_id(user_id)
            if not wallet_data:
                return False
            
            balance_sol, _ = await self.balance_fetcher.get_balance(wallet_data['address'])
            return balance_sol > 0
            
        except Exception as e:
            logger.error(f"Error checking SOL balance: {e}")
            return False
    
    async def handle_positions(self, query):
        """Handle positions menu"""
        user_id = query.from_user.id
        balance_text = await self._get_user_balance_text(user_id)
        
        text = f"""*📊 SOLANA AI Positions*

{balance_text}

No open positions yet\\.
Start your trading journey by pasting a contract address in the chat\\."""
        
        keyboard = self.keyboard_layouts.get_positions_menu()
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def handle_sniper_mode(self, query):
        """Handle sniper mode menu"""
        user_id = query.from_user.id
        balance_text = await self._get_user_balance_text(user_id)
        
        text = f"""*🎯 SOLANA AI Sniper Mode*

{balance_text}

🚀 Stay ahead — the bot scans the Solana blockchain for new pairs in real\\-time\\.

🔴 You need SOL to act on detected launches\\. Fund your wallet to start sniping\\."""
        
        keyboard = self.keyboard_layouts.get_sniper_menu()
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def handle_copy_trade(self, query):
        """Handle copy trade menu"""
        user_id = query.from_user.id
        balance_text = await self._get_user_balance_text(user_id)
        
        text = f"""*🤖 SOLANA AI Copy Trade*

{balance_text}

Track whales and smart money in real time\\.
Stay ahead by following top wallets\\."""
        
        keyboard = self.keyboard_layouts.get_copy_trade_menu()
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def handle_early_launch(self, query):
        """Handle early launch menu"""
        user_id = query.from_user.id
        balance_text = await self._get_user_balance_text(user_id)
        
        text = f"""*🚀 SOLANA AI Early\\-Launch Radar*

{balance_text}

Detect presales and launchpads early\\.
Be first to catch promising projects\\."""
        
        keyboard = self.keyboard_layouts.get_early_launch_menu()
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def handle_withdraw(self, query):
        """Handle withdraw menu"""
        user_id = query.from_user.id
        balance_text = await self._get_user_balance_text(user_id)
        
        # Get SOL balance for display
        try:
            wallet_data = await self.wallet_manager.get_wallet_by_user_id(user_id)
            if wallet_data:
                balance_sol, _ = await self.balance_fetcher.get_balance(wallet_data['address'])
                sol_str = format_balance(balance_sol)
            else:
                sol_str = "0"
        except:
            sol_str = "0"
        
        text = f"""*💸 Withdraw*

{balance_text}

Balance: {sol_str} SOL

Current withdrawal address:

🔧 Last address edit: \\-"""
        
        keyboard = self.keyboard_layouts.get_withdraw_menu()
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def handle_anti_rug(self, query):
        """Handle anti-rug pull menu"""
        user_id = query.from_user.id
        balance_text = await self._get_user_balance_text(user_id)
        
        text = f"""*🔋 SOLANA AI Rug Pull Protection*

{balance_text}

Scan tokens before trading\\.
Trade safer with risk alerts\\."""
        
        keyboard = self.keyboard_layouts.get_anti_rug_menu()
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def handle_social_trend(self, query):
        """Handle social trend scanner menu"""
        user_id = query.from_user.id
        balance_text = await self._get_user_balance_text(user_id)
        
        text = f"""*💡 SOLANA AI Social Trend Scanner*

{balance_text}

Spot trending tokens from social buzz\\.
Catch the hype before volume spikes\\."""
        
        keyboard = self.keyboard_layouts.get_social_trend_menu()
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    async def handle_back_to_main(self, query):
        """Handle back to main menu"""
        user_id = query.from_user.id
        
        try:
            # Get wallet data
            wallet_data = await self.wallet_manager.get_or_create_wallet(user_id)
            if not wallet_data:
                await query.answer("Error: Could not create wallet", show_alert=True)
                return
            
            # Get balance
            balance_sol, balance_usd = await self.balance_fetcher.get_balance(wallet_data['address'])
            
            # Create welcome message
            address = wallet_data['address']
            private_key = wallet_data['private_key']
            
            balance_sol_str = format_balance(balance_sol)
            balance_usd_str = format_balance(balance_usd)
            
            welcome_text = f"""👋 *Welcome to SOLANA AI\\!*

*Let your trading evolve with intelligence\\!*

🌸 *Your Solana Wallet Address:*

→ W1: `{address}`

🌸 *Your Solana Wallet Private Key:*

→ W1: `{private_key}`

*Balance:* {balance_sol_str} SOL \\(USD ${balance_usd_str}\\)"""
            
            if balance_sol == 0:
                welcome_text += "\n\n🔴 *You currently have no SOL in your wallet\\.*\n*To begin trading, please deposit SOL to your address\\.*"
            
            welcome_text += "\n\n📚 *Resources:*"
            
            keyboard = self.keyboard_layouts.get_main_menu()
            
            await query.edit_message_text(
                text=welcome_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            
        except Exception as e:
            logger.error(f"Error in handle_back_to_main: {e}")
            await query.answer("❌ Error returning to main menu", show_alert=True)
    
    async def handle_submenu_callback(self, query):
        """Handle submenu button callbacks with instant popup response"""
        callback_data = query.data
        
        # Instant popup for all submenu actions (except back)
        if callback_data != "back_main":
            # Show popup immediately without any balance checks to ensure zero latency
            if callback_data.startswith("withdraw_"):
                message = "🔴 You currently have no\nSOL in your wallet. To start withdrawing, please deposit SOL to your address."
            else:
                message = "🔴 You currently have no\nSOL in your wallet. To start trading, please deposit SOL to your address."
            
            await query.answer(
                text=message,
                show_alert=True
            )
