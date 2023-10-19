import requests
import json
import logging
import hashlib
import csv

# Configure the logging
logging.basicConfig(filename='api_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the API endpoint URLs

api_url_1 = 'https://petstore.swagger.io/v2/store/inventory'
api_url_2 = 'https://petstore.swagger.io/v2/store/inventory'


def make_api_call(api_url):
    try:
        # Make the API request
        response = requests.get(api_url)

        # Check for a successful response (status code 200)
        if response.status_code == 200:
            data = response.json()
            logger.info(f'Successful API call to {api_url}')
            logger.info(f'Response JSON: {json.dumps(data, indent=2)}')
            return data

        else:
            logger.error(f'Failed API call to {api_url}. Status code: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f'Error during API call to {api_url}: {str(e)}')
        return None


def calculate_hash(data):
    try:
        a = json.dumps(data, sort_keys=True).encode("utf-8")
        response_hash = hashlib.md5(a).hexdigest()
        return response_hash
    except Exception as e:
        print(f"Error calculating hash: {str(e)}")
        return None


def lambda_handler(event, context):
    response1 = make_api_call(api_url_1)
    if response1:
        print("API Response 1:")
        print(json.dumps(response1, indent=2))
        hash1 = calculate_hash(response1)
        print("API Response Hash 1:")
        print(hash1)

    response2 = make_api_call(api_url_2)
    if response2:
        print("API Response 2:")
        print(json.dumps(response2, indent=2))
        hash2 = calculate_hash(response2)
        print("API Response Hash 2:")
        print(hash2)

    # String comparison
    if response1 and response2:
        if response1 == response2:
            print("API Response 1 and Response 2 match.")
        else:
            print("API Response 1 and Response 2 do not match.")

    # Hashing comparison
    if hash1 and hash2:
        if hash1 == hash2:
            print(f"Hashes match: {hash1} == {hash2}")
        else:
            print(f"Checksums do not match: {hash1} != {hash2}")
    else:
        print("Checksum comparison could not be performed due to errors.")
