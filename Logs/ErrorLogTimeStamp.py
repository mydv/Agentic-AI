import logging
from logging.handlers import TimedRotatingFileHandler
import time
from datetime import datetime, timedelta

# Logger setup
logger = logging.getLogger("PaymentLogger")
logger.setLevel(logging.ERROR)

handler = TimedRotatingFileHandler(
    filename="logs/payment_error_timestamp.log",
    when="H",
    interval=1,
    backupCount=24,
    encoding="utf-8"
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Track last log time
last_log_time = datetime.min

def process_payment(user_id, amount):
    global last_log_time
    now = datetime.now()
    if now - last_log_time >= timedelta(minutes=5):
        try:
            if amount <= 0:
                raise ValueError("Invalid payment amount.")
            raise ConnectionError("Payment gateway timeout.")
        except Exception as e:
            logger.error(f"Payment failed for user {user_id}: {str(e)}")
        last_log_time = now  # Update timestamp
    else:
        try:
            if amount <= 0:
                raise ValueError("Invalid payment amount.")
            raise ConnectionError("Unable to process payment.")
        except Exception as e:
            logger.error(f"Payment failed for user {user_id}: {str(e)}")

if __name__ == "__main__":
    while True:
        process_payment("user_123", 0)
        process_payment("user_456", 100.00)
        time.sleep(120)  # Sleep for 2 minutes
