# BoostX-Token-API

**fetch.py** 

This script loads a configuration file (config.yaml) with details like the API key and the number of tokens to fetch. It sends a request to an API to purchase tokens and displays the results. Errors are handled for invalid responses or missing configuration data.

**buy_tokens.py**

This script defines a `/buy_tokens` command for a Discord bot. It allows authorized users to purchase tokens using the BoostX API, verifies if the user has permission, and saves the purchased tokens to a local file. After the transaction, it sends a confirmation message to the user with the details or an error message if something fails.

Make sure you configure everything so it works with your Boost Bot
