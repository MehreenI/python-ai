import csv
import json
import logging
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# --- Settings ---
API_URL = os.getenv("API_ENDPOINT", "https://api.github.com/users/")
TOKEN = os.getenv("GITHUB_TOKEN")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 2))
TIMEOUT = int(os.getenv("TIMEOUT", 10))

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
CSV_FILE = OUTPUT_DIR / os.getenv("CSV_FILE", "summary.csv")
LOG_FILE = os.getenv("LOG_FILE", "errors.log")
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)

HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

FIELDS = ["login", "name", "public_repos", "followers"]


def get_usernames():
    user_name = input("Enter GitHub usernames (Comma Separated Values): ")
    return user_name.split(",")


def fetch_user(username, attempt=1):
    try:
        response = requests.get(f"{API_URL}{username}", headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        user = response.json()
        return {field: user.get(field) for field in FIELDS}
    except requests.Timeout:
        error = "Request timed out"
    except requests.ConnectionError:
        error = "No internet connection"
    except requests.HTTPError as e:
        status = e.response.status_code
        if status < 500:
            logging.error(f"HTTP error for '{username}': {status}")
            return None
        error = f"HTTP error {status}"
    except requests.RequestException as error:
        # Any other requests error (bad URL, invalid JSON, etc.) - retrying won't help
        logging.error(f"Request failed for '{username}': {error}")
        return None

    logging.error(f"{error} for '{username}' (attempt {attempt}/{MAX_RETRIES}).")

    if attempt < MAX_RETRIES:
        time.sleep(RETRY_DELAY)
        return fetch_user(username, attempt + 1) 

    return None


def save_json(username, user_data):
    file_path = OUTPUT_DIR / f"{username}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=2)
    print(f"JSON saved: {file_path}")


def save_csv(users):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(users)
    print(f"CSV saved: {CSV_FILE}")


def main():
    users = []

    for username in get_usernames():
        user_data = fetch_user(username)
        if user_data:
            save_json(username, user_data)
            users.append(user_data)

    if users:
        save_csv(users)
    else:
        print("No successful users. CSV was not created.")


if __name__ == "__main__":
    main()
