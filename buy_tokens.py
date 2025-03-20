# Configuration  - you need to configure this to let it work with your Boost Bot
CONFIG_FILE_PATH = "config/config.yaml"  # Path to the config file (either YAML or JSON)
STOCK_FILE_PATH_1M = "data/1m.txt"  # Path to 1M token stock file
STOCK_FILE_PATH_3M = "data/3m.txt"  # Path to 3M token stock file
ALLOWED_TO_USE_BOOSTXAPI_COMMANDS = ['owners_ids']# fill in the allowed users/roles to use the command or use ['...'].get['...']

def load_config():
    # Controleer of het bestand bestaat
    if not os.path.exists(CONFIG_FILE_PATH):
        raise FileNotFoundError(f"The configuration file {CONFIG_FILE_PATH} does not exist.")
    
    # Open en laad het bestand afhankelijk van het type
    try:
        if CONFIG_FILE_PATH.endswith('.yaml'):
            with open(CONFIG_FILE_PATH, "r") as file:
                return yaml.safe_load(file)
        elif CONFIG_FILE_PATH.endswith('.json'):
            with open(CONFIG_FILE_PATH, "r") as file:
                return json.load(file)
        else:
            raise ValueError("Unsupported config file format. Please use .yaml or .json.")
    except Exception as e:
        # Voeg foutmelding toe voor betere debugging
        raise RuntimeError(f"Error loading the configuration file: {e}")

# Fetch tokens via the API
def fetch_tokens(api_key, tokens, token_type):
    url = 'http://fi7.bot-hosting.net:20030/api_buy_tokens'
    
    data = {
        'api_key': api_key,
        'tokens': tokens,
        'token_type': token_type
    }
    response = requests.post(url, json=data)

    try:
        return response.json()
    except ValueError as e:
        logging.error(f"Error in JSON processing: {e}")
        return {"error": "Invalid response from the server."}
    
# Check if the user is the owner
def is_allowed_to_use_command(interaction: discord.Interaction) -> bool:
    config = load_config()
    allowed_to_use_key = ALLOWED_TO_USE_BOOSTXAPI_COMMANDS[0]  # Dit haalt 'owner_ids' op uit de lijst
    allowed_to_use = config.get(allowed_to_use_key, [])  # Haal de lijst van toegestane gebruikers op via de sleutel
    print(allowed_to_use)
    return str(interaction.user.id) in allowed_to_use

@bot.tree.command(name="buy_tokens", description="Automatically purchase tokens via BoostX API")
@app_commands.choices(tokentype=[
    app_commands.Choice(name="1 Month", value="1m"),
    app_commands.Choice(name="3 Months", value="3m")
])
async def buy_tokens(interaction: discord.Interaction, tokentype: str, amount: int):
    config = load_config()

    # Check if the user is the owner
    if not is_allowed_to_use_command(interaction):
        embed = discord.Embed(
            title="Permission Denied",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Retrieve API settings
    api_key = config["boostx_token_api"].get("api_key")

    # Load the stock file paths for 1M and 3M
    if tokentype == "1m":
        stock_file = STOCK_FILE_PATH_1M
    elif tokentype == "3m":
        stock_file = STOCK_FILE_PATH_3M
    else:
        stock_file = None

    if stock_file is None:
        embed = discord.Embed(
            title="Error",
            description="Invalid token type specified. Choose '1m' or '3m'.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Fetch tokens via the API
    response_data = fetch_tokens(api_key, amount, tokentype,)

    if "error" in response_data:
        embed = discord.Embed(
            title="Error",
            description=f"Error: {response_data['error']}",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Check if tokens were delivered
    tokens_delivered = response_data.get("tokens_delivered", [])
    if not tokens_delivered:
        embed = discord.Embed(
            title="Error",
            description="No tokens received from the API.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    # Save tokens to the specified stock file
    try:
        with open(stock_file, "a") as file:
            file.write("\n".join(tokens_delivered) + "\n")
    except Exception as e:
        logging.error(f"Error saving tokens: {e}")
        return await interaction.response.send_message("Failed to save tokens.", ephemeral=True)

    # Create embed message
    embed = discord.Embed(
        title="Token Purchase Successful",
        description=(
            f"**Amount:** {amount} tokens \n"
            f"**Type:** {tokentype}\n"
            f"**Order ID:** `{response_data.get('order_id', 'Unknown')}`\n"
            f"**Total Cost:** `{response_data.get('total_cost', 'Unknown')}`"
        ),
        color=discord.Color.green()
    )
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1289594755910729739/1352021003051733054/BoostX_2.png")
    embed.set_footer(text="Tokens have been added to your stock.")

    # Attempt to send a DM to the user
    member = interaction.user
    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message(
            f"Unable to send a message to {member.name}. DMs may be disabled.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(embed=embed, ephemeral=True)
