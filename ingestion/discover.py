"""
discover.py

Purpose:
--------
Connect to Drupal JSON:API and discover all available resources.
"""

import requests
from config import JSON_API_URL


def discover_resources():
    print("=" * 60)
    print("Drupal AI Agent - Discovery Module")
    print("=" * 60)

    print(f"\nConnecting to: {JSON_API_URL}")

    try:
        response = requests.get(JSON_API_URL, timeout=10)
        response.raise_for_status()

        data = response.json()

        print("\n✅ Connection Successful")
        print("\nAvailable Resources:\n")

        if "links" in data:
            for resource in data["links"]:
                print(f"✓ {resource}")
        else:
            print("No resources found.")

        print("\nDiscovery completed successfully.")

    except requests.exceptions.RequestException as e:
        print("\n❌ Failed to connect to Drupal")
        print(e)


if __name__ == "__main__":
    discover_resources()