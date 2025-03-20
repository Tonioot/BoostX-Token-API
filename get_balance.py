# Configuration  - you need to configure this to let it work with your Boost Bot
CONFIG_FILE_PATH = "config/config.yaml"  # Path to the config file (either YAML or JSON)
ALLOWED_TO_USE_BOOSTXAPI_COMMANDS = ['owners_ids']# fill in the allowed users/roles to use the command or use ['...'].get['...']


@bot.tree.command(name="get_balance", description="Get your current balance from the BoostX API")
async def get_balance(interaction: discord.Interaction):
    # Check if the user is allowed to use this command
    if not is_allowed_to_use_command(interaction):
        await interaction.response.send_message("You are not allowed to use this command.", ephemeral=True)
        return

    # Laad de configuratie en haal de API key op
    config = load_config()
    api_key = config.get('boostx_token_api', {}).get('api_key', None)

    if not api_key:
        await interaction.response.send_message("API key not found in the configuration.", ephemeral=True)
        return

    # Verstuur een request naar de API om de balans op te halen
    url = f"{boostxtokenapi}/get_api_balance"
    headers = {
    "API-Key": api_key  # Gebruik de juiste header
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Gooi een fout als de status code niet 200 is

        # Verkrijg de balans uit de response
        data = response.json()

        # Controleer of de response de balans bevat
        if "balance" not in data:
            error_message = data.get("error", "Unknown error occurred.")
            await interaction.response.send_message(f"Error: {error_message}", ephemeral=True)
            return

        balance = data["balance"]
        balance = round(balance, 2)
        # Maak een embed en stuur de balans terug
        embed = discord.Embed(
            title="Your BoostX Token Balance",
            description=f"Your current balance is **${balance}**.",
            color=discord.Color.green()
        )
        embed.set_footer(text="This is the Balance of the BoostX Token API Key in your Config")
        await interaction.response.send_message(embed=embed)
        

    except requests.exceptions.RequestException as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
