#!/usr/bin/env python
"""
RabbitMQ Message Consumer Startup Script
"""
import logging
import argparse
import time
import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.messaging.order_events import OrderEventConsumer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def start_order_created_consumer():
    """Start order creation event consumer"""
    logger.info("Starting order creation event consumer...")
    consumer = OrderEventConsumer()
    try:
        consumer.start_order_created_consumer()
    except KeyboardInterrupt:
        logger.info("Interrupt signal received, shutting down consumer...")
    finally:
        consumer.close()
        logger.info("Order creation event consumer has been closed")


def start_payment_processed_consumer():
    """Start payment processing event consumer"""
    logger.info("Starting payment processing event consumer...")
    consumer = OrderEventConsumer()
    try:
        consumer.start_payment_processed_consumer()
    except KeyboardInterrupt:
        logger.info("Interrupt signal received, shutting down consumer...")
    finally:
        consumer.close()
        logger.info("Payment processing event consumer has been closed")


def declare_queues():
    """Declare required queues"""
    logger.info("Declaring required queues...")
    consumer = OrderEventConsumer()
    try:
        consumer.declare_queues()
        logger.info("Queues declared successfully")
    finally:
        consumer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Order message queue consumer")
    parser.add_argument(
        "--queue",
        type=str,
        choices=["order_created", "payment_processed", "all", "setup"],
        default="all",
        help="Queue name to consume, or use 'setup' to just create queues",
    )

    args = parser.parse_args()

    if args.queue == "setup":
        declare_queues()
    elif args.queue == "order_created":
        # Declare queues before starting consumer
        declare_queues()
        start_order_created_consumer()
    elif args.queue == "payment_processed":
        start_payment_processed_consumer()
    elif args.queue == "all":
        logger.info("Starting all consumers...")
        import threading

        # Create threads to run multiple consumers in parallel
        order_thread = threading.Thread(target=start_order_created_consumer)
        payment_thread = threading.Thread(target=start_payment_processed_consumer)

        # Start threads
        order_thread.start()
        payment_thread.start()

        try:
            # Wait for threads to complete
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Interrupt signal received, please wait for all consumers to close...")

        logger.info("All consumers have been closed")

# To start this consumer, run:
# python scripts/consumer.py --queue all