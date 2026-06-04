"""
Arc testnet onboarding helpers: the network config, MetaMask instructions, a fresh testnet
wallet, a reachability check, a balance read, and a first test transaction. The goal is to
take someone from nothing to a confirmed transaction on Arc in a couple of minutes.
"""
from __future__ import annotations

import os
from typing import Optional

import httpx

RPC_URL = os.getenv("ARC_TESTNET_RPC_URL", "https://rpc.testnet.arc.network")
CHAIN_ID = 5042002
EXPLORER = "https://testnet.arcscan.app"
FAUCET = "https://faucet.circle.com"
NATIVE_DECIMALS = 18


def network_info() -> dict:
    return {
        "network_name": "Arc Testnet",
        "rpc_url": RPC_URL,
        "chain_id": CHAIN_ID,
        "currency_symbol": "USDC",
        "block_explorer": EXPLORER,
        "faucet": FAUCET,
        "note": "USDC is the native gas token on Arc. Get testnet USDC from the faucet.",
    }


def metamask_instructions() -> str:
    n = network_info()
    return (
        "Add Arc Testnet to MetaMask:\n"
        "  Settings > Networks > Add a network > Add manually\n"
        f"  Network name: {n['network_name']}\n"
        f"  RPC URL: {n['rpc_url']}\n"
        f"  Chain ID: {n['chain_id']}\n"
        f"  Currency symbol: {n['currency_symbol']}\n"
        f"  Block explorer: {n['block_explorer']}\n"
        f"Then get testnet USDC at {n['faucet']} ."
    )


def new_wallet() -> dict:
    """Generate a fresh testnet wallet. Use it only for testnet, never for real funds."""
    from eth_account import Account
    acct = Account.create()
    pk = acct.key.hex()
    if not pk.startswith("0x"):  # newer eth-account/hexbytes returns no 0x prefix
        pk = "0x" + pk
    return {
        "address": acct.address,
        "private_key": pk,
        "warning": "Testnet only. Never fund this with real assets. Keep the private key secret.",
    }


def _rpc(method: str, params: list):
    with httpx.Client(timeout=15.0) as client:
        r = client.post(RPC_URL, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
        r.raise_for_status()
        data = r.json()
        if data.get("error"):
            raise RuntimeError(data["error"])
        return data["result"]


def doctor() -> dict:
    """Check that the RPC is reachable and reports the expected chain id."""
    try:
        chain_hex = _rpc("eth_chainId", [])
        chain = int(chain_hex, 16)
        block = int(_rpc("eth_blockNumber", []), 16)
        return {
            "rpc_reachable": True,
            "chain_id": chain,
            "chain_id_ok": chain == CHAIN_ID,
            "latest_block": block,
        }
    except Exception as e:
        return {"rpc_reachable": False, "error": str(e)}


def check_balance(address: str) -> dict:
    wei = int(_rpc("eth_getBalance", [address, "latest"]), 16)
    return {"address": address, "usdc": wei / 10 ** NATIVE_DECIMALS}


def send_test(to: str, amount_usdc: float = 0.01, private_key: Optional[str] = None) -> dict:
    """Send a tiny first transaction to confirm the wallet works. Key from arg or env."""
    key = private_key or os.getenv("ARC_PRIVATE_KEY")
    if not key:
        return {"ok": False, "error": "no private key (pass private_key or set ARC_PRIVATE_KEY)"}
    from eth_account import Account
    from eth_utils import to_checksum_address

    acct = Account.from_key(key)
    nonce = int(_rpc("eth_getTransactionCount", [acct.address, "pending"]), 16)
    # Arc uses EIP-1559 (type 2) with a 20 Gwei minimum base fee.
    try:
        base = int(_rpc("eth_getBlockByNumber", ["latest", False]).get("baseFeePerGas", "0x0"), 16)
    except Exception:
        base = 0
    base = max(base, 20 * 10 ** 9)
    try:
        priority = int(_rpc("eth_maxPriorityFeePerGas", []), 16) or 10 ** 9
    except Exception:
        priority = 10 ** 9
    tx = {
        "to": to_checksum_address(to),
        "value": int(round(amount_usdc * 10 ** NATIVE_DECIMALS)),
        "gas": 21000,
        "maxFeePerGas": base * 2 + priority,
        "maxPriorityFeePerGas": priority,
        "nonce": nonce,
        "chainId": CHAIN_ID,
        "type": 2,
    }
    signed = Account.sign_transaction(tx, key)
    raw = signed.raw_transaction.hex()
    if not raw.startswith("0x"):
        raw = "0x" + raw
    tx_hash = _rpc("eth_sendRawTransaction", [raw])
    return {"ok": True, "tx_hash": tx_hash, "explorer": f"{EXPLORER}/tx/{tx_hash}"}
