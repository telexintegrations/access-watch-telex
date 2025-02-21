import concurrent.futures
import requests

from access_watch.middlewares import AccessMonitoringMiddleware

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_task(payload):
    # Initialize settings with default values
    monitor_anonymous = "Yes"
    include_timestamp = "Yes"
    threshold = 5

    # Loop through settings to retrieve necessary data
    for setting in payload['settings']:
        label_lower = setting['label'].lower()

        if "anonymous" in label_lower:
            monitor_anonymous = setting.get('default', "Yes")
        elif "timestamp" in label_lower:
            include_timestamp = setting.get('default', "Yes")
        elif "threshold" in label_lower:
            threshold = int(setting.get('default', 5))

    # Get all cached data
    cached_data = AccessMonitoringMiddleware.get_all_cached_data()

    logger.info(cached_data)

    # Filter cached data based on access count and the threshold
    filtered_data = []
    for key, value in cached_data.items():
        access_count = value.get('count', 0)
        timestamp = value.get('timestamp')

        # Filter by access count
        if access_count >= threshold:
            # Filter out anonymous users
            if "anon_access" in key and monitor_anonymous != "Yes":
                continue

            # Construct the entry to add to the final message
            data_entry = {
                "key": key,
                "access_count": access_count
            }

            # Include timestamp
            if include_timestamp == "Yes" and timestamp:
                data_entry["timestamp"] = timestamp

            filtered_data.append(data_entry)

    logger.info("This line is running")

    if len(filtered_data) > 0:
        logger.info("There is a message to be sent")

        # Prepare the message with the filtered data
        message = "\n".join([
            f"User: {entry['key']} - Attempts: {entry['access_count']}" + 
            (f" - Last Access: {entry['timestamp']}" if 'timestamp' in entry else "")
            for entry in filtered_data
        ])


        # Data follows telex webhook format, calling the return_url
        data = {
            "message": message,
            "username": "LMO",
            "event_name": "Security Check",
            "status": "error" if filtered_data else "success"
        }

        # clear cache
        AccessMonitoringMiddleware.clear_all_cache(threshold)

        # Send the request to the return_url
        return_url = f"{payload['return_url']}"

        requests.post(return_url, json=data)

    # Test with webhook url
    # url = "https://ping.telex.im/v1/webhooks/01951715-27aa-7f6e-999e-1f31cf6371d7"

    # requests.post(
    #     url,
    #     json=data,
    #     headers={
    #         "Accept": "application/json",
    #         "Content-Type": "application/json"
    #     }
    # )

def run_background_task(payload):
    # Create a process pool and submit a task to run in another process
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(monitor_task, payload)
