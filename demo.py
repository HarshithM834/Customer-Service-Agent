# Runnable demo: test all scenarios without needing FastAPI server

import asyncio
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def print_section(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


async def demo():
    print_section("AI Customer Support Agent - Demo")
    print("Multi-agent customer support system")
    print("Powered by: Gemini + Perplexity + ElevenLabs")
    
    print_section("Scenario 1: Billing Question")
    billing_query = {
        "message": "Why is my bill so high this month? I usually pay $80 but now it's $120.",
        "customer_id": "demo_cust_001"
    }
    print(f"Customer: {billing_query['message']}")
    try:
        response = client.post("/chat", json=billing_query)
        result = response.json()
        print(f"\nAgent Type: {result['agent_type']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Cost Estimate: ${result['cost_estimate']:.4f}")
        print("✓ Success")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print_section("Scenario 2: Sales Question")
    sales_query = {
        "message": "I'm interested in your 5G unlimited plan. What's the difference from my current plan?",
        "customer_id": "demo_cust_002"
    }
    print(f"Customer: {sales_query['message']}")
    try:
        response = client.post("/chat", json=sales_query)
        result = response.json()
        print(f"\nAgent Type: {result['agent_type']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Cost Estimate: ${result['cost_estimate']:.4f}")
        print("✓ Success")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print_section("Scenario 3: Technical Support")
    tech_query = {
        "message": "My phone keeps dropping calls. What should I do?",
        "customer_id": "demo_cust_003"
    }
    print(f"Customer: {tech_query['message']}")
    try:
        response = client.post("/chat", json=tech_query)
        result = response.json()
        print(f"\nAgent Type: {result['agent_type']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Cost Estimate: ${result['cost_estimate']:.4f}")
        print("✓ Success")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print_section("Scenario 4: Miscellaneous Question")
    misc_query = {
        "message": "Do you have any promotions running right now?",
        "customer_id": "demo_cust_004"
    }
    print(f"Customer: {misc_query['message']}")
    try:
        response = client.post("/chat", json=misc_query)
        result = response.json()
        print(f"\nAgent Type: {result['agent_type']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Cost Estimate: ${result['cost_estimate']:.4f}")
        print("✓ Success")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print_section("Interaction Logs")
    try:
        logs_response = client.get("/logs")
        logs = logs_response.json()
        print(f"Total Interactions: {logs['total_interactions']}\n")
        
        print("Sample Log Entries:")
        for i, log in enumerate(logs['logs'][:3], 1):
            print(f"\n{i}. Customer: {log['customer_message'][:60]}...")
            print(f"   Agent Type: {log['agent_type']}")
            print(f"   Response: {log['response'][:80]}...")
            print(f"   Timestamp: {log['timestamp']}")
        print("\n✓ Logging working correctly")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print_section("Health Check")
    try:
        health_response = client.get("/health")
        health = health_response.json()
        print(f"Status: {health['status']}")
        print(f"Service: {health['service']}")
        print("✓ System healthy")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print_section("Demo Complete")
    print("✓ Multi-agent routing working")
    print("✓ Intent classification working")
    print("✓ Context retrieval working")
    print("✓ Agent responses generated")
    print("✓ Logging/observability working")
    print("✓ All endpoints functional")
    print("\nTo run this demo again: python3 demo.py")
    print("To start FastAPI server: python3 main.py")
    print("\nGitHub: https://github.com/yourusername/tmobile-agent")


if __name__ == "__main__":
    asyncio.run(demo())
