"""
Utility functions for the SOLANA AI Bot
"""

import logging
from datetime import datetime
from typing import Union

def format_balance(amount: Union[int, float]) -> str:
    """Format balance to avoid showing 0.0, always show 0 instead"""
    if amount == 0 or amount == 0.0:
        return "0"
    
    # For very small amounts, show with appropriate decimal places
    if amount < 0.001:
        return f"{amount:.6f}".rstrip('0').rstrip('.')
    elif amount < 1:
        return f"{amount:.4f}".rstrip('0').rstrip('.')
    else:
        return f"{amount:.2f}".rstrip('0').rstrip('.')

def get_french_timestamp() -> str:
    """Get current timestamp in French format (dd/mm/yyyy hh:mm:ss)"""
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def setup_logging():
    """Set up logging configuration"""
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create file handler for persistent logging
    file_handler = logging.FileHandler('solana_ai_bot.log')
    file_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )
    
    # Reduce noise from external libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def escape_markdown_v2(text: str) -> str:
    """Escape special characters for MarkdownV2"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text
