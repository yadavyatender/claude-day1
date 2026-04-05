#!/usr/bin/env python3
"""
Gold 22K Rate Tracker with Email Notifications
Fetches live gold prices and sends email updates
"""

import sys
import time
import logging
from database import create_database
from scheduler import GoldRateScheduler
from config import GMAIL_PASSWORD

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gold_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_configuration():
    """Verify configuration before starting."""
    logger.info("Checking configuration...")
    
    if not GMAIL_PASSWORD:
        logger.error("❌ GMAIL_PASSWORD not set in .env file")
        logger.info("Please set up your Gmail App Password:")
        logger.info("1. Enable 2-Factor Authentication on your Gmail account")
        logger.info("2. Go to https://myaccount.google.com/apppasswords")
        logger.info("3. Create an app password and copy it")
        logger.info("4. Add GMAIL_PASSWORD to .env file")
        return False
    
    logger.info("✓ Configuration looks good")
    return True

def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("Gold 22K Rate Tracker - Starting")
    logger.info("=" * 60)
    
    # Check configuration
    if not check_configuration():
        sys.exit(1)
    
    # Initialize database
    try:
        create_database()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)
    
    # Start scheduler
    scheduler = GoldRateScheduler()
    try:
        scheduler.start()
        logger.info("✓ Gold Rate Scheduler is running!")
        logger.info("Press Ctrl+C to stop the application")
        
        # Keep the application running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("\nShutdown signal received...")
        scheduler.stop()
        logger.info("✓ Application stopped gracefully")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        scheduler.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
