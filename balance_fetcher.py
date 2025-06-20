"""
Balance fetching from Solana blockchain and price APIs
"""

import aiohttp
import asyncio
import logging
from typing import Tuple

from config import SOLSCAN_API_BASE, SOLSCAN_API_KEY, PRICE_API_URL

logger = logging.getLogger(__name__)

class BalanceFetcher:
    def __init__(self):
        self.session = None
        self._session_timeout = aiohttp.ClientTimeout(total=3)  # Faster timeout
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self._session_timeout)
        return self.session
    
    async def get_balance(self, address: str) -> Tuple[float, float]:
        """Get SOL balance and USD value for address"""
        try:
            # Get SOL balance and USD price concurrently
            sol_balance_task = self._get_sol_balance(address)
            sol_price_task = self._get_sol_price()
            
            sol_balance, sol_price = await asyncio.gather(
                sol_balance_task,
                sol_price_task,
                return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(sol_balance, Exception):
                logger.error(f"Error getting SOL balance: {sol_balance}")
                sol_balance = 0.0
            
            if isinstance(sol_price, Exception):
                logger.error(f"Error getting SOL price: {sol_price}")
                sol_price = 0.0
            
            # Calculate USD value
            usd_value = sol_balance * sol_price
            
            return sol_balance, usd_value
            
        except Exception as e:
            logger.error(f"Error in get_balance: {e}")
            return 0.0, 0.0
    
    async def _get_sol_balance(self, address: str) -> float:
        """Get SOL balance from SolScan API"""
        try:
            session = await self._get_session()
            
            # SolScan API endpoint
            url = f"{SOLSCAN_API_BASE}/account"
            params = {"address": address}
            
            headers = {}
            if SOLSCAN_API_KEY:
                headers["Authorization"] = f"Bearer {SOLSCAN_API_KEY}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract SOL balance (lamports to SOL conversion)
                    lamports = data.get("lamports", 0)
                    sol_balance = lamports / 1_000_000_000  # Convert lamports to SOL
                    
                    return sol_balance
                else:
                    logger.warning(f"SolScan API returned status {response.status}")
                    return 0.0
                    
        except asyncio.TimeoutError:
            logger.warning("Timeout getting SOL balance")
            return 0.0
        except Exception as e:
            logger.error(f"Error getting SOL balance: {e}")
            return 0.0
    
    async def _get_sol_price(self) -> float:
        """Get current SOL price in USD"""
        try:
            session = await self._get_session()
            
            async with session.get(PRICE_API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    price = data.get("solana", {}).get("usd", 0.0)
                    return float(price)
                else:
                    logger.warning(f"Price API returned status {response.status}")
                    return 0.0
                    
        except asyncio.TimeoutError:
            logger.warning("Timeout getting SOL price")
            return 0.0
        except Exception as e:
            logger.error(f"Error getting SOL price: {e}")
            return 0.0
    
    async def close(self):
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
