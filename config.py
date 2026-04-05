import os
from dotenv import load_dotenv

load_dotenv()

# Gmail Configuration
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', 'yatenderyadav489@gmail.com')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', '')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', 'yatenderyadav489@gmail.com').split(',')

# API Configuration
METALS_API_KEY = os.getenv('METALS_API_KEY', '')
# Using metals.live API - free, no authentication required
GOLD_API_URL = 'https://api.metals.live/v1/spot/gold'

# Currency Exchange Rates (USD to INR/AED)
USD_TO_INR = float(os.getenv('USD_TO_INR', '83.12'))
USD_TO_AED = float(os.getenv('USD_TO_AED', '3.67'))

# Database
DATABASE_FILE = 'gold_rates.db'

# Scheduling
INITIAL_SCHEDULE = os.getenv('INITIAL_SCHEDULE', 'hourly')
INITIAL_DURATION_HOURS = int(os.getenv('INITIAL_DURATION_HOURS', '24'))
RECURRING_SCHEDULE = os.getenv('RECURRING_SCHEDULE', 'weekly')

# Email
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
