import azure.functions as func
import logging
from .secops_tuning import (
    get_threat_investigations, 
    send_high_priority_investigations, 
    send_review_queue_investigations, 
    post_high_confidence_feedback
)

def main(mytimer: func.TimerRequest) -> None:
    logging.info('SecOps Tuning script started.')
    
    threats_data = get_threat_investigations()
    
    if threats_data and 'investigations' in threats_data:
        threats = threats_data['investigations']
        if threats:
            logging.info(f"Retrieved {len(threats)} threats.")
            # Execute steps
            send_high_priority_investigations(threats)
            send_review_queue_investigations(threats)
            post_high_confidence_feedback(threats)
        else:
            logging.info("No threats found.")
    else:
        logging.error("Failed to fetch data.")
