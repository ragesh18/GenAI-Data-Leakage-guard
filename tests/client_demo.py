# client_demo.py

import requests

BASE_URL = "http://127.0.0.1:8000"


def send_prompt(prompt: str):
    resp = requests.post(f"{BASE_URL}/chat", json={"prompt": prompt})
    resp.raise_for_status()
    return resp.json()


def main():
    print("=== GenAI DLP Guard Client Demo ===")
    while True:
        prompt = input("\nEnter a prompt (or 'quit' to exit): ")
        if prompt.lower() in {"quit", "exit"}:
            break

        try:
            result = send_prompt(prompt)
        except Exception as e:
            print(f"Error: {e}")
            continue

        print("\n--- Proxy Decision ---")
        print(f"Action: {result['action']}")
        if result.get("masked_prompt"):
            print(f"Masked prompt: {result['masked_prompt']}")
        print("Message:", result["message"])

        if result["findings"]:
            print("\nFindings:")
            for f in result["findings"]:
                print(
                    f" - [{f['severity']}] {f['category']}: "
                    f"'{f['match']}' ({f['description']})"
                )

        if result.get("model_response"):
            print("\nSimulated LLM response:")
            print(result["model_response"])


if __name__ == "__main__":
    main()
