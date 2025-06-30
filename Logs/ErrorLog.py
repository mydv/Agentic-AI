import logging

# Configure logging
logging.basicConfig(
    filename='logs/payment_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_payment(user_id, amount):
    try:
        # Simulate payment logic
        if amount <= 0:
            raise ValueError("Invalid payment amount.")
        # Simulate external payment gateway failure
        raise ConnectionError("Payment gateway timeout.")
    except Exception as e:
        logging.error(f"Payment failed for user {user_id}: {str(e)}")

# Example usage
process_payment("user_123", 0)       # Invalid amount
process_payment("user_456", 100.00)  # Simulated gateway failure
