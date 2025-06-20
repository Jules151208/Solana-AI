"""
Keyboard layouts for different bot menus
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class KeyboardLayouts:
    def get_main_menu(self) -> InlineKeyboardMarkup:
        """Get main menu keyboard layout"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Positions", callback_data="positions"),
                InlineKeyboardButton("🎯 Sniper Mode", callback_data="sniper_mode")
            ],
            [
                InlineKeyboardButton("🤖 Copy Trade", callback_data="copy_trade"),
                InlineKeyboardButton("🚀 Early-Launch", callback_data="early_launch")
            ],
            [
                InlineKeyboardButton("💸 Withdraw", callback_data="withdraw"),
                InlineKeyboardButton("🔋 Anti-Rug Pull", callback_data="anti_rug")
            ],
            [
                InlineKeyboardButton("💡 Social Trend Scanner", callback_data="social_trend")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_positions_menu(self) -> InlineKeyboardMarkup:
        """Get positions submenu keyboard layout (2x2 grid)"""
        keyboard = [
            [
                InlineKeyboardButton("📝 Min Value: N/A SOL", callback_data="pos_min_value"),
                InlineKeyboardButton("📝 Sell Position: 100%", callback_data="pos_sell_position")
            ],
            [
                InlineKeyboardButton("🔴 USD", callback_data="pos_usd"),
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_sniper_menu(self) -> InlineKeyboardMarkup:
        """Get sniper mode submenu keyboard layout"""
        keyboard = [
            [
                InlineKeyboardButton("🎯 Pro Account", callback_data="sniper_pro"),
                InlineKeyboardButton("🎯 Create Task", callback_data="sniper_create")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_copy_trade_menu(self) -> InlineKeyboardMarkup:
        """Get copy trade submenu keyboard layout (3-column layout)"""
        keyboard = [
            [
                InlineKeyboardButton("🆕 Add new config", callback_data="copy_add_config"),
                InlineKeyboardButton("🚛 Mass Create", callback_data="copy_mass_create")
            ],
            [
                InlineKeyboardButton("⏹️ Pause All", callback_data="copy_pause_all"),
                InlineKeyboardButton("▶️ Start All", callback_data="copy_start_all"),
                InlineKeyboardButton("🗑️ Delete All", callback_data="copy_delete_all")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_early_launch_menu(self) -> InlineKeyboardMarkup:
        """Get early launch submenu keyboard layout"""
        keyboard = [
            [
                InlineKeyboardButton("🚀 Detect Presale", callback_data="early_presale"),
                InlineKeyboardButton("🚀 Detect Launchpad", callback_data="early_launchpad")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_withdraw_menu(self) -> InlineKeyboardMarkup:
        """Get withdraw submenu keyboard layout"""
        keyboard = [
            [
                InlineKeyboardButton("50%", callback_data="withdraw_50"),
                InlineKeyboardButton("100%", callback_data="withdraw_100"),
                InlineKeyboardButton("X SOL", callback_data="withdraw_custom")
            ],
            [
                InlineKeyboardButton("💸 Set Address", callback_data="withdraw_set_address")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_anti_rug_menu(self) -> InlineKeyboardMarkup:
        """Get anti-rug pull submenu keyboard layout"""
        keyboard = [
            [
                InlineKeyboardButton("🔋 Scan Token", callback_data="rug_scan_token"),
                InlineKeyboardButton("🔋 Check Risk Score", callback_data="rug_risk_score")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_social_trend_menu(self) -> InlineKeyboardMarkup:
        """Get social trend scanner submenu keyboard layout"""
        keyboard = [
            [
                InlineKeyboardButton("💡 Trending Now", callback_data="social_trending"),
                InlineKeyboardButton("💡 Top Influencers", callback_data="social_influencers")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
