from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import logging
from database import insert_rate, get_latest_rate, get_previous_rate, log_notification, get_notification_count
from gold_api import fetch_gold_rate
from email_service import send_gold_rate_notification
from config import INITIAL_DURATION_HOURS, EMAIL_RECIPIENTS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoldRateScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.start_time = datetime.now()
        self.initial_duration = timedelta(hours=INITIAL_DURATION_HOURS)
        self.switched_to_weekly = False
    
    def check_and_update_schedule(self):
        """Check if we should switch from hourly to weekly schedule."""
        elapsed_time = datetime.now() - self.start_time
        
        if not self.switched_to_weekly and elapsed_time >= self.initial_duration:
            logger.info(f"Switching schedule from hourly to weekly (after {INITIAL_DURATION_HOURS} hours)")
            self.switched_to_weekly = True
            
            # Remove hourly job
            self.scheduler.remove_job('fetch_gold_rate_hourly')
            
            # Add weekly job
            self.scheduler.add_job(
                self.fetch_and_notify,
                IntervalTrigger(weeks=1),
                id='fetch_gold_rate_weekly',
                name='Weekly Gold Rate Fetch'
            )
            logger.info("Weekly schedule activated")
    
    def fetch_and_notify(self):
        """Fetch gold rate, store in DB, and send email notification."""
        logger.info("Starting gold rate fetch and notification...")
        
        try:
            # Fetch current rate
            rate_data = fetch_gold_rate()
            if rate_data is None:
                logger.error("Failed to fetch gold rate")
                return
            
            # Extract USD price
            price_usd = rate_data['price_usd']
            
            # Get previous rate for comparison
            previous_rate = get_previous_rate()
            current_db_rate = get_latest_rate()
            
            # Calculate change percent based on USD
            change_percent = None
            if current_db_rate:
                change_percent = ((price_usd - current_db_rate['price_usd']) / current_db_rate['price_usd']) * 100
            
            # Insert into database
            insert_rate(price_usd, change_percent)
            
            # Prepare data for email (use USD only)
            current_rate = {
                'price_usd': price_usd
            }
            
            # Send email notification
            email_sent = send_gold_rate_notification(current_rate, previous_rate)
            
            if email_sent:
                log_notification(EMAIL_RECIPIENTS[0], f"Gold Rate: ${price_usd:.2f}/g")
                logger.info(f"✓ Notification sent successfully - ${price_usd:.2f} USD")
            else:
                logger.warning("Failed to send notification")
            
            # Check if we need to switch schedules
            self.check_and_update_schedule()
            
        except Exception as e:
            logger.error(f"Error in fetch_and_notify: {e}", exc_info=True)
    
    def start(self):
        """Start the scheduler with initial hourly schedule."""
        try:
            logger.info("Starting Gold Rate Scheduler...")
            
            # Add initial hourly job
            self.scheduler.add_job(
                self.fetch_and_notify,
                IntervalTrigger(hours=1),
                id='fetch_gold_rate_hourly',
                name='Hourly Gold Rate Fetch'
            )
            
            # Execute immediately on start
            self.fetch_and_notify()
            
            self.scheduler.start()
            logger.info("✓ Scheduler started. Running hourly for the first 24 hours, then switches to weekly.")
            
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}", exc_info=True)
            raise
    
    def stop(self):
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def get_status(self):
        """Get scheduler status."""
        return {
            'running': self.scheduler.running,
            'jobs': len(self.scheduler.get_jobs()),
            'start_time': self.start_time,
            'elapsed_time': datetime.now() - self.start_time,
            'switched_to_weekly': self.switched_to_weekly
        }
