"""Tests for the onboarding helpers that do not need a chain: config correctness, the
MetaMask instructions, and fresh wallet generation."""
from kit.onboard import network_info, metamask_instructions, new_wallet, CHAIN_ID


def test_network_info_has_correct_chain():
    n = network_info()
    assert n["chain_id"] == 5042002
    assert n["rpc_url"].startswith("https://")
    assert n["currency_symbol"] == "USDC"


def test_metamask_instructions_mention_chain_and_faucet():
    s = metamask_instructions()
    assert "5042002" in s
    assert "faucet" in s.lower()


def test_new_wallet_produces_valid_address_and_key():
    w = new_wallet()
    assert w["address"].startswith("0x") and len(w["address"]) == 42
    assert w["private_key"].startswith("0x") and len(w["private_key"]) == 66


def test_new_wallet_key_derives_to_address():
    from eth_account import Account
    w = new_wallet()
    assert Account.from_key(w["private_key"]).address == w["address"]


def test_new_wallets_are_unique():
    assert new_wallet()["address"] != new_wallet()["address"]
