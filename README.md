
# MAITRIX Bot

Automated script to claim faucets, mint tokens, and stake on the Arbitrum Sepolia testnet.

---

## Features

- Supports multiple wallets via `.env` private keys.  
- Claims tokens from various faucets automatically.  
- Mints tokens using configured contracts and selectors.  
- Stakes minted tokens.  
- Interactive CLI with options to run faucet claims, mint & stake, or full 24-hour loop.
- later i will add ai16z mint and stake (for now only faucet )

---

## Setup

1. Clone the repo:
   ```bash
   
   git clone https://github.com/S1aidlag/Maitrix-BOT.git  
   cd Maitrix-BOT

2. Create a `.env` file with your private keys:
   ```bash
   PRIVATE_KEY=your_private_key_here

##
   You can add multiple keys by repeating the line.

3. Install dependencies:
   ```bash
   
   pip install -r requirements.txt

---

## Usage

Run the bot:

```bash

python bot.py
