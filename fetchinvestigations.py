import logging
import requests
import azure.functions as func

# Define the Azure Functions application instance
app = func.FunctionApp()

# NCRONTAB expression "0 */15 * * * *" schedules execution every 15 minutes
@app.timer_trigger(schedule="0 */15 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def fetch_threat_investigations(myTimer: func.TimerRequest) -> None:
    """
    Timer-triggered Azure function that fetches investigations every 15 minutes
    and logs items with a verdict of 'Threat'.
    """
    # Check if the execution is running later than scheduled
    if myTimer.past_due:
        logging.warning("The timer trigger is running late.")

    url = "https://qevlar-tam-case-api-production.up.railway.app/investigations"
    logging.info(f"Initiating HTTP GET request to: {url}")

    try:
        # Fetch data from the API
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        investigations = response.json()

        # Handle both a direct list response or an enveloped dictionary list
        if isinstance(investigations, dict):
            # Fallback to common enveloped keys if API wraps the list
            investigations_list = investigations.get("investigations", investigations.get("data", []))
        elif isinstance(investigations, list):
            investigations_list = investigations
        else:
            logging.error("Unexpected API response format. Expected a list or dictionary.")
            return

        # Filter items where the verdict matches 'Threat'
        threat_cases = [item for item in investigations_list if item.get("verdict") == "Threat"]
        
        logging.info(f"Successfully processed {len(investigations_list)} total cases.")
        logging.info(f"Found {len(threat_cases)} cases matching verdict='Threat'.")

        # Actionable processing placeholder for filtered threat records
        for case in threat_cases:
            case_id = case.get("id", "Unknown ID")
            logging.info(f"Processing Threat Case ID: {case_id}")
            # Add downstream automation logic here (e.g., Azure Sentinel, database storage, email alert)

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
    except ValueError:
        logging.error("Failed to decode JSON from the API response.")
