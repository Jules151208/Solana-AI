"""
Wallet management for Solana addresses
"""

import sqlite3
import asyncio
from solders.keypair import Keypair
import logging

from config import DATABASE_FILE

logger = logging.getLogger(__name__)

class WalletManager:
    def __init__(self):
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database"""
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wallets (
                    user_id INTEGER PRIMARY KEY,
                    address TEXT NOT NULL,
                    private_key TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    async def get_or_create_wallet(self, user_id: int) -> dict:
        """Get existing wallet or create new one for user"""
        try:
            # Check if wallet exists
            existing_wallet = await self._get_existing_wallet(user_id)
            if existing_wallet:
                return existing_wallet
            
            # Create new wallet
            return await self._create_new_wallet(user_id)
            
        except Exception as e:
            logger.error(f"Error in get_or_create_wallet for user {user_id}: {e}")
            raise
    
    async def _get_existing_wallet(self, user_id: int) -> dict | None:
        """Get existing wallet from database"""
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT address, private_key FROM wallets WHERE user_id = ?',
                (user_id,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'address': result[0],
                    'private_key': result[1]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting existing wallet: {e}")
            return None
    
    async def _create_new_wallet(self, user_id: int) -> dict:
        """Create new Solana wallet"""
        try:
            # Generate new keypair
            keypair = Keypair()
            
            # Get address and private key
            address = str(keypair.pubkey())
            private_key = str(keypair)
            
            # Save to database
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO wallets (user_id, address, private_key) VALUES (?, ?, ?)',
                (user_id, address, private_key)
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created new wallet for user {user_id}: {address}")
            
            return {
                'address': address,
                'private_key': private_key
            }
            
        except Exception as e:
            logger.error(f"Error creating new wallet: {e}")
            raise
    
    async def get_wallet_by_user_id(self, user_id: int) -> dict | None:
        """Get wallet data by user ID"""
        return await self._get_existing_wallet(user_id)
