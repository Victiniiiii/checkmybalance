import requests

def get_uuid(username):
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if response.status_code == 200:
        return response.json().get('id')
    return None

def get_coin_amount(uuid, api_key):
    response = requests.get(f"https://api.hypixel.net/skyblock/profiles?uuid={uuid}&key={api_key}")
    data = response.json()
    if data.get('success'):
        for profile_data in data.get('profiles', []):
            if profile_data.get('selected', False):
                banking = profile_data.get('banking', {})
                bank_coins = banking.get('balance', 0)
                coin_purse = sum(member.get('coin_purse', 0) for member in profile_data.get('members', {}).values())
                return bank_coins, coin_purse
    return None, None

username = input("Enter your Minecraft username: ")
api_key = input("Enter your Hypixel API key: ")

uuid = get_uuid(username)
if uuid:
    bank_coins, coin_purse = get_coin_amount(uuid, api_key)
    if bank_coins is not None and coin_purse is not None:
        print("Bank coins:", bank_coins)
        print("Coin purse coins:", coin_purse)
else:
    print("Failed to retrieve UUID. Please check your username and try again.")
