import time
import random
import requests
from web3 import Web3
from dotenv import dotenv_values

# ====== Load .env and multiple accounts ======
def load_private_keys(path=".env"):
    keys = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("PRIVATE_KEY="):
                keys.append(line.split("=", 1)[1])
    return keys

PRIVATE_KEYS = load_private_keys()
RPC_URL = "https://sepolia-rollup.arbitrum.io/rpc"
CHAIN_ID = 421614

# ====== Faucet Configuration ======
FAUCETS = [
    {"name": "ATH", "url": "https://app.x-network.io/maitrix-faucet/faucet"},
    {"name": "USDE", "url": "https://app.x-network.io/maitrix-usde/faucet"},
    {"name": "LVL", "url": "https://app.x-network.io/maitrix-lvl/faucet"},
    {"name": "Virtual USD", "url": "https://app.x-network.io/maitrix-virtual/faucet", "retry": True},
    {"name": "VANA", "url": "https://app.x-network.io/maitrix-vana/faucet"},
    {"name": "ai16z", "url": "https://app.x-network.io/maitrix-ai16z/faucet"},
    {"name": "USD1", "url": "https://app.x-network.io/maitrix-usd1/faucet"},
    {"name": "0G", "url": "https://app.x-network.io/maitrix-0g/faucet"}
]

def random_wait(max_sec=6):
    sec = random.uniform(1, max_sec)
    print(f"⏳ Waiting {sec:.2f} seconds to avoid bot detection...")
    time.sleep(sec)

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}h {m}m {s}s"

def claim_faucet(address, faucet):
    random_wait()
    headers = {"Content-Type": "application/json"}
    url = faucet["url"]
    name = faucet["name"]
    retry = faucet.get("retry", False)
    attempt = 1
    while attempt <= 3:
        try:
            res = requests.post(url, json={"address": address}, headers=headers)
            result = res.json()
            if "please wait" in result["message"].lower():
                seconds = int("".join(filter(str.isdigit, result["message"])))
                print(f"⏳   [{name}][{address}] Cooldown: {format_time(seconds)}")
            else:
                print(f"✅   [{name}][{address}] {result['message']} | Amount: {result.get('data', {}).get('amount')} | Tx: {result.get('data', {}).get('txHash', '-')}")
            break
        except Exception as e:
            if retry and attempt < 3:
                print(f"⚠️  [{name}][{address}] Error: {e}, retrying (attempt {attempt})...")
                time.sleep(3)
                attempt += 1
            else:
                print(f"❌   [{name}][{address}] Error: {e}")
                break

CONTRACTS = {
    "ausd": {
        "name": "Mint AUSD from ATH",
        "mint_contract": "0x2cFDeE1d5f04dD235AEA47E1aD2fB66e3A61C13e",
        "token_contract": "0x1428444Eacdc0Fd115dd4318FcE65B61Cd1ef399",
        "selector": "0x1bf6318b",
        "decimals": 18
    },
    "vusd": {
        "name": "Mint vUSD from VIRTUAL",
        "mint_contract": "0x3dCACa90A714498624067948C092Dd0373f08265",
        "token_contract": "0xFF27D611ab162d7827bbbA59F140C1E7aE56e95C",
        "selector": "0xa6d67510",
        "decimals": 9
    },
    "vanausd": {
        "name": "Mint VANAUSD from VANA",
        "mint_contract": "0xefbae3a68b17a61f21c7809edfa8aa3ca7b2546f",
        "token_contract": "0xbebf4e25652e7f23ccdcccaacb32004501c4bff8",
        "selector": "0xa6d67510",
        "decimals": 18
    },
    "azusd": {
        "name": "Mint AZUSD from AI16Z",
        "mint_contract": "0xB0b53d8B4ef06F9Bbe5db624113C6A5D35bB7522",
        "token_contract": "0x2d5a4f5634041f50180A25F26b2A8364452E3152",
        "selector": "0xa6d67510",
        "decimals": 18
    },
    "ousd": {
        "name": "Mint OUSD from 0G",
        "mint_contract": "0x0b4301877A981e7808A8F4B6E277C376960C7641",
        "token_contract": "0xFBBDAb7684A4Da0CFAE67C5c13fA73402008953e",
        "selector": "0xa6d67510",
        "decimals": 18
    }
}

STAKING = {
    "ausd": {
        "staking_contract": "0x054de909723ECda2d119E31583D40a52a332f85c",
        "token_contract": "0x78De28aABBD5198657B26A8dc9777f441551B477",
        "decimals": 18
    },
    "vusd": {
        "staking_contract": "0x5bb9Fa02a3DCCDB4E9099b48e8Ba5841D2e59d51",
        "token_contract": "0xc14A8E2Fc341A97a57524000bF0F7F1bA4de4802",
        "decimals": 9
    },
    "usde": {
        "staking_contract": "0x3988053b7c748023a1aE19a8ED4c1Bf217932bDB",
        "token_contract": "0xf4BE938070f59764C85fAcE374F92A4670ff3877",
        "decimals": 18
    },
    "lvlusd": {
        "staking_contract": "0x5De3fBd40D4c3892914c3b67b5B529D776A1483A",
        "token_contract": "0x8802b7bcF8EedCc9E1bA6C20E139bEe89dd98E83",
        "decimals": 18
    },
    "vanausd": {
        "staking_contract": "0x46a6585a0Ad1750d37B4e6810EB59cBDf591Dc30",
        "token_contract": "0x46a6585a0Ad1750d37B4e6810EB59cBDf591Dc30",
        "decimals": 18
    },
    "azusd": {
        "staking_contract": "0xf45Fde3F484C44CC35Bdc2A7fCA3DDDe0C8f252E",
        "token_contract": "0x5966cd11aED7D68705C9692e74e5688C892cb162",
        "decimals": 18
    },
    "usd1": {
        "staking_contract": "0x7799841734ac448b8634f1c1d7522bc8887a7bb9",
        "token_contract": "0x16a8A3624465224198d216b33E825BcC3B80abf7",
        "decimals": 18
    },
    "ousd": {
        "staking_contract": "0xF8F951DA83dAC732A2dCF207B644E493484047eB",
        "token_contract": "0xD23016Fd7154d9A6F2830Bfb4eA3F3106AAE0E88",
        "decimals": 18
    }
}

def get_web3():
    return Web3(Web3.HTTPProvider(RPC_URL))

def get_raw_balance(w3, token_address, address):
    abi = [{
        "name": "balanceOf",
        "type": "function",
        "inputs": [{"name": "owner", "type": "address"}],
        "outputs": [{"name": "balance", "type": "uint256"}],
        "stateMutability": "view"
    }]
    contract = w3.eth.contract(address=w3.to_checksum_address(token_address), abi=abi)
    return contract.functions.balanceOf(w3.to_checksum_address(address)).call()

def approve_erc20(w3, private_key, token_address, spender, amount_wei, address):
    random_wait()
    abi = [{
        "name": "approve",
        "type": "function",
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable"
    }]
    contract = w3.eth.contract(address=w3.to_checksum_address(token_address), abi=abi)
    nonce = w3.eth.get_transaction_count(w3.to_checksum_address(address))
    tx = contract.functions.approve(w3.to_checksum_address(spender), amount_wei).build_transaction({
        "from": w3.to_checksum_address(address),
        "gas": 100000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "chainId": CHAIN_ID
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[+] Approve transaction sent: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("[+] Approve succeeded!")
    time.sleep(5)

def mint_token(w3, account, private_key, token):
    random_wait()
    c = CONTRACTS[token]
    address = w3.to_checksum_address(account.address)
    raw_balance = get_raw_balance(w3, c["token_contract"], address)
    if raw_balance == 0:
        print(f"[!] No {token.upper()} balance to mint.")
        return
    approve_erc20(w3, private_key, c["token_contract"], c["mint_contract"], raw_balance, address)
    encoded_amount = hex(raw_balance)[2:].zfill(64)
    data = c["selector"] + encoded_amount
    nonce = w3.eth.get_transaction_count(address)
    tx = {
        "to": w3.to_checksum_address(c["mint_contract"]),
        "value": 0,
        "gas": 300000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "data": data,
        "chainId": CHAIN_ID
    }
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[+] Mint {token.upper()} tx: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"[+] Mint {token.upper()} successful!")
    time.sleep(5)

def stake_token(w3, account, private_key, token):
    random_wait()
    c = STAKING[token]
    address = w3.to_checksum_address(account.address)
    raw_balance = get_raw_balance(w3, c["token_contract"], address)
    if raw_balance == 0:
        print(f"[!] No {token.upper()} balance to stake.")
        return
    approve_erc20(w3, private_key, c["token_contract"], c["staking_contract"], raw_balance, address)
    data = "0xa694fc3a" + hex(raw_balance)[2:].zfill(64)
    nonce = w3.eth.get_transaction_count(address)
    tx = {
        "to": w3.to_checksum_address(c["staking_contract"]),
        "value": 0,
        "gas": 300000,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "data": data,
        "chainId": CHAIN_ID
    }
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[+] Stake {token.upper()} tx: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"[+] Stake {token.upper()} successful!")
    time.sleep(5)

def run_mint_and_stake_loop():
    print(f"\n🕒 {time.ctime()} | Starting Mint & Stake 24-Hour Loop...\n")
    w3 = get_web3()
    for pk in PRIVATE_KEYS:
        account = w3.eth.account.from_key(pk)
        print(f"---- Wallet: {account.address} ----")
        for token in CONTRACTS.keys():
            mint_token(w3, account, pk, token)
            stake_token(w3, account, pk, token)
            random_wait()
        stake_token(w3, account, pk, "usd1")
        print(f"---- Done with wallet {account.address} ----\n")
        random_wait()
    print("✅   All minting and staking processed.\n")

def run_bot():
    while True:
        print("=== MAITRIX BOT ===\n")
        print("1. Run Faucet (Claim Tokens)\n2. Run Mint & Stake\n3. 24-Hour Auto Loop (Claim + Mint & Stake)")
        choice = input("Select an option: ")

        if choice == "1":
            run_faucet_bot()
        elif choice == "2":
            run_mint_and_stake_loop()
        elif choice == "3":
            print("Starting the 24-hour loop... \n")
            while True:
                run_faucet_bot()
                run_mint_and_stake_loop()
                time.sleep(86400)
        else:
            print("❌ Invalid choice. Please try again.")
        print("\n")
        time.sleep(2)

if __name__ == "__main__":
    run_bot()
