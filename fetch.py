import requests
import yaml

# Load the config from the config.yaml
def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("config.yaml not found.")
        return {}

def fetch_tokens(api_key, tokens, token_type):
    url = 'http://fi7.bot-hosting.net:20030/api_buy_tokens'  # Will be updated soon


    # JSON body to send to the server
    data = {
        'api_key': api_key,
        'tokens': tokens,
        'token_type': token_type
    }

    # Send the request to the server
    response = requests.post(url, json=data)


    try:
        return response.json()
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return {"Error": "Invalid response from server."}


def main():
    # Load the config.yaml
    config = load_config()

    if not config or 'api_key' not in config or 'tokens_to_fetch' not in config or 'token_type' not in config:
        print("config1.yaml is niet goed geconfigureerd. Zorg ervoor dat de API-sleutel, het aantal tokens en het type zijn opgegeven.")
        return

    api_key = config['api_key']
    tokens_to_fetch = config['tokens_to_fetch']
    token_type = config['token_type']

    # Send the request to fetch tokens
    response_data = fetch_tokens(api_key, tokens_to_fetch, token_type)

    if 'error' in response_data:
        print(f"Error: {response_data['error']}")
    else:
        print(f"Successfuly fetched {tokens_to_fetch}X {token_type} tokens !")
        print(f"Order ID: {response_data['order_id']}")
        print(f"Tokens Delivered: {response_data['tokens_delivered']}")
        print(f"Total Cost: {response_data['total_cost']}")


if __name__ == '__main__':
    main()
