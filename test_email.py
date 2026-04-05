#!/usr/bin/env python3
"""
Simple test script to send a test email
"""

from email_service import send_email
from config import GMAIL_EMAIL, EMAIL_RECIPIENTS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_test_email():
    """Send a simple test email to verify Gmail setup."""
    
    subject = "🧪 Gold Rate Tracker - Test Email (USD)"
    
    from_email = GMAIL_EMAIL
    to_emails = ', '.join(EMAIL_RECIPIENTS)
    
    body_html = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 8px; }}
                h2 {{ color: #d4af37; text-align: center; }}
                .status {{ background-color: #e8f5e9; padding: 15px; border-radius: 5px; }}
                .price-box {{ background-color: #fff9e6; padding: 15px; border-radius: 5px; margin: 10px 0; text-align: center; }}
                .price-box strong {{ font-size: 18px; color: #d4af37; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>✅ Test Email Successful!</h2>
                
                <div class="status">
                    <p><strong>Gold Rate Tracker</strong> is now configured and working correctly.</p>
                    <p>Email notifications will show prices in <strong>USD ($)</strong></p>
                    <p>You will receive gold price updates every hour for the first 24 hours, then weekly.</p>
                </div>
                
                <div class="price-box">
                    <p>📊 Sample Gold 22K Price</p>
                    <strong>$65.50 per gram</strong>
                </div>
                
                <p style="margin-top: 20px; color: #666;">
                    <strong>From:</strong> {from_email}<br>
                    <strong>To:</strong> {to_emails}<br>
                </p>
                
                <p style="text-align: center; color: #999; font-size: 12px; margin-top: 30px;">
                    This is a test notification from Gold Rate Tracker - Prices in USD
                </p>
            </div>
        </body>
    </html>
    """
    
    logger.info("📧 Sending test email...")
    logger.info(f"From: {GMAIL_EMAIL}")
    logger.info(f"To: {', '.join(EMAIL_RECIPIENTS)}")
    
    success = send_email(subject, body_html)
    
    if success:
        logger.info("✅ Test email sent successfully!")
        return True
    else:
        logger.error("❌ Failed to send test email")
        return False

if __name__ == "__main__":
    send_test_email()
