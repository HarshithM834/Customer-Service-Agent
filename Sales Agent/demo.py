# Demo script for Sales Agent

from services import classify_sales_intent
from agents import SalesRouter
import time

def run_demo():
    router = SalesRouter()
    
    test_messages = [
        "I'm looking to switch to your service, do you have any deals?",
        "I want to upgrade my iPhone 14 to the new model.",
        "What are the specs for the Samsung Galaxy S24?",
        "Are there any holiday promotions right now?",
        "I am just browsing, curious about what you sell.", 
        "Where can I find a store near me?" # might be other
    ]
    
    print("--- Starting Sales Agent Demo ---")
    
    for msg in test_messages:
        print(f"\nCustomer: {msg}")
        
        intent = classify_sales_intent(msg)
        print(f"Classified Intent: {intent}")
        
        agent_name, response = router.route(intent, msg)
        print(f"Agent: {agent_name}")
        print(f"Response: {response[:150]}...") # Truncate for display
        
        time.sleep(1)

if __name__ == "__main__":
    run_demo()
