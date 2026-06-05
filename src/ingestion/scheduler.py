import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.ingestion import run_ingestion

logger = logging.getLogger(__name__)

# Create a global scheduler instance
scheduler = BackgroundScheduler()

def init_scheduler():
    """Initializes and starts the background scheduler for daily ingestion."""
    logger.info("Setting up daily ingestion scheduler...")
    
    try:
        # Schedule job for 10:00 AM IST daily
        scheduler.add_job(
            run_ingestion,
            trigger=CronTrigger(hour=10, minute=0, timezone="Asia/Kolkata"),
            id="daily_ingestion",
            name="Daily corpus re-ingestion",
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("Scheduler started successfully. Next run scheduled for 10:00 AM IST.")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")

def shutdown_scheduler():
    """Gracefully shuts down the background scheduler."""
    if scheduler.running:
        logger.info("Shutting down ingestion scheduler...")
        scheduler.shutdown(wait=False)
        logger.info("Scheduler shut down.")
