# BoostX-Token-API

**fetch.py** 

This script loads a configuration file (config.yaml) with details like the API key and the number of tokens to fetch. It sends a request to an API to purchase tokens and displays the results. Errors are handled for invalid responses or missing configuration data.

**buy_tokens.py**

This script defines a `/buy_tokens` command for a Discord bot. It allows authorized users to purchase tokens using the BoostX API, verifies if the user has permission, and saves the purchased tokens to a local file. After the transaction, it sends a confirmation message to the user with the details or an error message if something fails.

Make sure you configure everything so it works with your Boost Bot (for Developers)

**get_balance.py**

This scripts fetches the balance of the api thats placed in the config. Make sure you configure everything so it works with your Boost Bot (for Developers)



Here are the updated API endpoints and their responses, all in English as requested.

### 1. **Get Balance**
- **Endpoint**: `/get_api_balance`
- **Method**: `GET`
- **Description**: Get the balance of a user by sending the **API key** in the request headers.
- **Headers**:
  - `API-Key`: The user's API key
- **Response**:
  ```json
  {
      "balance": 100
  }
  ```

### Example Request:
```http
GET /get_api_balance
Headers:
API-Key: your_api_key
```

### Example Response:
```json
{
    "balance": 100
}
```

---

### 2. **Get Stock**
- **Endpoint**: `/get_stock`
- **Method**: `GET`
- **Description**: Get the stock of tokens (1m and 3m).
- **Response**:
  ```json
  {
      "1m_tokens": 200,
      "3m_tokens": 150
  }
  ```

### Example Request:
```http
GET /get_stock
```

### Example Response:
```json
{
    "1m_tokens": 200,
    "3m_tokens": 150
}
```

---

### 3. **Buy Tokens**
- **Endpoint**: `/api_buy_tokens`
- **Method**: `POST`
- **Description**: Buy tokens via the API. Attach the **API key**, the **number of tokens**, and the **token type** in the request body.
- **Request Body**:
  ```json
  {
      "api_key": "user_api_key",
      "tokens": 5,
      "token_type": "1m"
  }
  ```
- **Response**:
  ```json
  {
      "status": "success",
      "message": "Tokens bought",
      "invoice_id": "572a3a42-4bc7-4cd7-ba60-8b85929d6b91",
      "order_id": "572a3a42-4bc7-4cd7-ba60-8b85929d6b91",
      "tokens_delivered": ["dfaasdfafds"],
      "total_cost": 0.1
  }
  ```

### Example Request:
```http
POST /api_buy_tokens
Content-Type: application/json
{
    "api_key": "user_api_key",
    "tokens": 5,
    "token_type": "1m"
}
```

### Example Response:
```json
{
    "status": "success",
    "message": "Tokens bought",
    "invoice_id": "572a3a42-4bc7-4cd7-ba60-8b85929d6b91",
    "order_id": "572a3a42-4bc7-4cd7-ba60-8b85929d6b91",
    "tokens_delivered": ["dfaasdfafds"],
    "total_cost": 0.1
}
```

---

### Error Responses:

#### 1. **Insufficient tokens in stock**:
When there are not enough tokens in stock to fulfill the request.

```json
{
    "error": "Insufficient tokens in stock"
}
```

#### 2. **Invalid API key**:
When the provided API key is invalid and no matching user is found.

```json
{
    "error": "Invalid API key"
}
```

#### 3. **Insufficient balance**:
When the user does not have enough balance to purchase the tokens.

```json
{
    "error": "Insufficient balance"
}
```


