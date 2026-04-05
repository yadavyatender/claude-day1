import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import GMAIL_EMAIL, GMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, EMAIL_RECIPIENTS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(subject, body_html, recipients=None):
    """Send email via Gmail SMTP."""
    if recipients is None:
        recipients = EMAIL_RECIPIENTS
    
    if not GMAIL_PASSWORD:
        logger.error("GMAIL_PASSWORD not configured. Please set it in .env file")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = GMAIL_EMAIL
        msg['To'] = ', '.join(recipients)
        
        msg.attach(MIMEText(body_html, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent to {recipients}: {subject}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error("Gmail authentication failed. Check email/password in .env")
        return False
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def create_gold_rate_email(current_rate, previous_rate=None):
    """Create formatted HTML email for gold rate update."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    price_usd = current_rate['price_usd']
    
    change_html = ""
    if previous_rate:
        prev_price_usd = previous_rate['price_usd']
        change_percent = ((price_usd - prev_price_usd) / prev_price_usd) * 100
        change_indicator = "📈" if change_percent > 0 else "📉"
        change_html = f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">Previous Price (USD):</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; font-weight: bold;">${prev_price_usd:.2f}</td>
        </tr>
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #ddd;">Change:</td>
            <td style="padding: 10px; border-bottom: 1px solid #ddd; font-weight: bold; color: {'green' if change_percent > 0 else 'red'};">
                {change_indicator} {change_percent:+.2f}%
            </td>
        </tr>
        """
    
    html_body = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                h2 {{ color: #d4af37; text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .highlight {{ background-color: #fff9e6; }}
                .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🏆 Gold 22K Live Price Update</h2>
                
                <table>
                    <tr class="highlight">
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">Current Price (USD):</td>
                        <td style="padding: 10px; border-bottom: 1px solid #ddd; font-weight: bold; color: #d4af37; font-size: 18px;">
                            ${price_usd:.2f} per gram
                        </td>
                    </tr>
                    {change_html}
                    <tr>
                        <td style="padding: 10px;">Updated At:</td>
                        <td style="padding: 10px;">{timestamp}</td>
                    </tr>
                </table>
                
                <div class="footer">
                    <p>This is an automated notification from Gold Rate Tracker.</p>
                    <p>Live Price in USD | Data source: GoldAPI & Metals.live</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return html_body

def send_gold_rate_notification(current_rate, previous_rate=None):
    """Send gold rate update email."""
    subject = f"🏆 Gold 22K Price Update: ${current_rate['price_usd']:.2f} USD/g"
    body = create_gold_rate_email(current_rate, previous_rate)
    return send_email(subject, body)
