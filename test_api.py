import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/api/health")
    print("Health Check:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_ask_jiji(query="Explain RAG"):
    payload = {"query_text": query}
    response = requests.post(
        f"{BASE_URL}/api/ask-jiji",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Ask Jiji - Query: '{query}'")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Answer: {data['answer']}")
        print(f"Resources found: {len(data['resources'])}")
        for i, resource in enumerate(data['resources'], 1):
            print(f"  {i}. {resource['title']} ({resource['type']})")
            print(f"     URL: {resource['file_url']}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Learn with Jiji API")
    print("=" * 50)
    print()
    
    # Test health endpoint
    test_health()
    
    # Test with different queries
    test_ask_jiji("Explain RAG")
    test_ask_jiji("Machine Learning")
    test_ask_jiji("Neural Networks")
    
    # Test with empty query (should fail validation)
    response = requests.post(
        f"{BASE_URL}/api/ask-jiji",
        json={"query_text": ""}
    )
    print("Test empty query:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")