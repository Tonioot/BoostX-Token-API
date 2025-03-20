import requests
import yaml

# Laad de configuratie uit config1.yaml
def load_config():
    try:
        with open('fetch.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("fetch.yaml not found.")
        return {}

def fetch_tokens(api_key, tokens, token_type):
    url = 'http://127.0.0.1:5000/api_buy_tokens'  # Dit is het adres van de server


    # JSON body die we sturen naar de server
    data = {
        'api_key': api_key,
        'tokens': tokens,
        'token_type': token_type
    }

    # Verstuur het verzoek naar de server
    response = requests.post(url, json=data)


    try:
        return response.json()
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return {"Error": "Invalid response from server."}


def main():
    # Laad de config1.yaml
    config = load_config()

    if not config or 'api_key' not in config or 'tokens_to_fetch' not in config or 'token_type' not in config:
        print("config1.yaml is niet goed geconfigureerd. Zorg ervoor dat de API-sleutel, het aantal tokens en het type zijn opgegeven.")
        return

    api_key = config['api_key']
    tokens_to_fetch = config['tokens_to_fetch']
    token_type = config['token_type']

    # Verstuur de aanvraag om tokens op te halen
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
