# **BoostX-Token-API Documentation**

### **Overview**
This API allows you to manage BoostX tokens by interacting with three main scripts:

- **fetch.py**: Loads the configuration (API key and token quantity), sends a request to the API to purchase tokens, and handles error responses.
- **buy_tokens.py**: This script defines a `/buy_tokens` command for a Discord bot. Authorized users can purchase tokens using the BoostX API. After the transaction, the purchased tokens are saved to a local file, and the bot sends a confirmation message to the user.
- **get_balance.py**: This script fetches the balance of tokens associated with the API key in the configuration file. It retrieves the user's balance for use in other operations.

---

### **API Endpoints**

## **1. Get Balance**
- **Endpoint**: `/get_api_balance`
- **Method**: `GET`
- **Description**: Retrieve the current balance of the user by sending the **API key** in the request headers.
- **Headers**:
  - `API-Key`: The user's API key.
  
- **Example Request**:
  ```http
  GET /get_api_balance
  Headers:
  API-Key: your_api_key
  ```

- **Example Response**:
  ```json
  {
      "balance": 100
  }
  ```

  **Error Response (Invalid API key)**:
  ```json
  {
      "error": "Invalid API key"
  }
  ```

---

## **2. Get Stock**
- **Endpoint**: `/get_stock`
- **Method**: `GET`
- **Description**: Retrieve the available stock of tokens (1m and 3m tokens).
  
- **Example Request**:
  ```http
  GET /get_stock
  ```

- **Example Response**:
  ```json
  {
      "1m_tokens": 200,
      "3m_tokens": 150
  }
  ```

  **Error Response (Invalid API key)**:
  ```json
  {
      "error": "Invalid API key"
  }
  ```

---

## **3. Buy Tokens**
- **Endpoint**: `/api_buy_tokens`
- **Method**: `POST`
- **Description**: Allows users to buy tokens via the API by providing their **API key**, the **number of tokens**, and the **token type** in the request body.
  
- **Request Body**:
  ```json
  {
      "api_key": "user_api_key",
      "tokens": {token_amount},
      "token_type": "{token_type}" // Can be '1m' or '3m'
  }
  ```

- **Example Request**:
  ```http
  POST /api_buy_tokens
  Content-Type: application/json
  {
      "api_key": "user_api_key",
      "tokens": 5,
      "token_type": "1m"
  }
  ```

- **Example Response**:
  ```json
  {
      "message": "Successfully bought 5X 1m tokens!",
      "order_id": "297a3a42-4bc7-4cd7-ba60-8b85289d6b91",
      "tokens_delivered": ["MTMxNTU47f0ccxct2JeJyIxAFf4MDk4MzYzMjU4NDc4Ng.G4rIEw.IOZQ4-PPKDq8fo4FXQY"],
      "total_cost": 0.5
  }
  ```

  **Error Response (Insufficient Tokens in Stock)**:
  ```json
  {
      "error": "Insufficient tokens in stock"
  }
  ```

  **Error Response (Insufficient Balance)**:
  ```json
  {
      "error": "Insufficient balance"
  }
  ```

  **Error Response (Invalid API Key)**:
  ```json
  {
      "error": "Invalid API key"
  }
  ```

---

