# Gold 22K Rate Tracker 🏆

A Python application that tracks live Gold 22K prices and sends email notifications via Gmail.

## Features

✨ **Live Price Tracking**
- Fetches real-time Gold 22K prices from Metals API
- Stores historical data in SQLite database
- Tracks price changes and trends

📧 **Smart Email Notifications**
- Sends hourly updates for the first 24 hours
- Automatically switches to weekly updates
- Beautiful HTML formatted emails
- Includes price comparisons and change percentages

💾 **Database Storage**
- SQLite database for persistent storage
- Maintains historical rate data
- Logs all notifications sent

## Prerequisites

- Python 3.8 or higher
- Gmail account with App Password enabled
- Internet connection for API calls

## Installation

1. **Clone or download the project**
   ```bash
   cd gold-rate-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gmail App Password**
   - Go to your Gmail account settings
   - Enable 2-Factor Authentication if not already enabled
   - Visit https://myaccount.google.com/apppasswords
   - Create an "App password" for Mail/Windows
   - Copy the 16-character password

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add:
   ```
   GMAIL_EMAIL=yatenderyadav489@gmail.com
   GMAIL_PASSWORD=your_16_char_app_password_here
   EMAIL_RECIPIENTS=yatenderyadav489@gmail.com
   ```

## Usage

**Start the application:**
```bash
python main.py
```

The application will:
1. ✓ Fetch the current gold price immediately
2. ✓ Send the first email notification
3. ✓ Continue fetching every hour for 24 hours
4. ✓ Automatically switch to weekly updates after 24 hours
5. ✓ Store all data in `gold_rates.db`

**Stop the application:**
Press `Ctrl+C` to gracefully shutdown

## Project Structure

```
gold-rate-tracker/
├── main.py              # Application entry point
├── config.py            # Configuration & settings
├── database.py          # SQLite database operations
├── gold_api.py          # API integration for fetching rates
├── email_service.py     # Gmail SMTP email sending
├── scheduler.py         # Job scheduling and automation
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .env                 # Your actual credentials (keep secret!)
├── gold_rates.db        # SQLite database (auto-created)
├── gold_tracker.log     # Application logs
└── README.md            # This file
```

## Configuration

Edit `.env` to customize:

```env
# Gmail credentials
GMAIL_EMAIL=yatenderyadav489@gmail.com
GMAIL_PASSWORD=your_app_password

# Email recipients (comma-separated)
EMAIL_RECIPIENTS=yatenderyadav489@gmail.com

# Scheduling
INITIAL_SCHEDULE=hourly           # Send every hour
INITIAL_DURATION_HOURS=24         # For this many hours
RECURRING_SCHEDULE=weekly         # Then send weekly
```

## Email Template

The application sends beautifully formatted HTML emails with:
- 💰 Current gold price (USD and INR)
- 📊 Previous price for comparison
- 📈/📉 Percentage change indicator
- ⏰ Timestamp of the update

## Database Schema

### gold_rates table
```sql
- id: Auto-increment primary key
- timestamp: When the rate was fetched
- price_usd: Price per gram in USD
- price_inr: Price per gram in INR
- change_percent: Percentage change from previous rate
- source: Data source (e.g., 'metals_api')
```

### notifications table
```sql
- id: Auto-increment primary key
- timestamp: When email was sent
- email_to: Recipient email address
- subject: Email subject line
- status: Delivery status
```

## Logs

Application logs are saved to `gold_tracker.log` and displayed in the console:
- INFO: Regular operations and milestones
- WARNING: Non-critical issues
- ERROR: Failures and errors

## Troubleshooting

**Gmail Authentication Failed**
- Verify you're using an App Password, not your Gmail password
- Ensure 2-Factor Authentication is enabled on your Gmail
- Check that the password in `.env` is correct

**API Connection Error**
- Verify you have an active internet connection
- Check that the Metals API is accessible
- Review logs in `gold_tracker.log`

**Email Not Sending**
- Check that GMAIL_PASSWORD is set correctly
- Verify your email address is correct
- Check internet connection
- Review Gmail security settings

## Data API

- **Source**: Metals API (https://metals.live)
- **Rate**: Gold prices per troy ounce
- **Conversion**: Automatically converted to per gram for Indian context
- **Update Frequency**: On demand (controlled by scheduler)

## Future Enhancements

- [ ] Web dashboard for rate visualization
- [ ] Multiple currency support
- [ ] Price alerts/thresholds
- [ ] SMS notifications
- [ ] Mobile app
- [ ] Historical charts
- [ ] Export functionality (CSV/PDF)

## Support

For issues or questions:
1. Check the logs: `gold_tracker.log`
2. Verify `.env` configuration
3. Ensure all dependencies are installed

## License

MIT License - Feel free to use and modify

## Disclaimer

This tool is provided for informational purposes. Gold prices can be volatile. Always verify prices from official sources before making financial decisions.

---

Made with ❤️ by Your Assistant
