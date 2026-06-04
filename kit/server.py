"""
Arc Onboarding Kit: get from nothing to a confirmed transaction on Arc testnet in minutes.
Network config and MetaMask steps, a fresh testnet wallet, an RPC health check, a balance
read, and a first test transaction. Exposed as MCP tools (and a CLI: python -m kit).
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .onboard import (
    network_info, metamask_instructions, new_wallet, doctor, check_balance, send_test,
)

mcp = FastMCP("arc-onboarding-kit")


@mcp.tool()
def onboard_network() -> dict:
    """Arc testnet network configuration (RPC, chain id, gas token, explorer, faucet)."""
    return network_info()


@mcp.tool()
def onboard_metamask() -> dict:
    """Copy-paste MetaMask add-network instructions for Arc testnet."""
    return {"instructions": metamask_instructions()}


@mcp.tool()
def onboard_new_wallet() -> dict:
    """Generate a fresh testnet wallet (address and private key). Testnet only."""
    return new_wallet()


@mcp.tool()
def onboard_doctor() -> dict:
    """Check that the Arc RPC is reachable and reports chain id 5042002."""
    return doctor()


@mcp.tool()
def onboard_balance(address: str) -> dict:
    """Native USDC balance of an address on Arc testnet."""
    return check_balance(address)


@mcp.tool()
def onboard_send_test(to: str, amount_usdc: float = 0.01) -> dict:
    """Send a tiny first transaction to confirm a funded wallet works. Key from
    ARC_PRIVATE_KEY in the environment."""
    return send_test(to, amount_usdc)


if __name__ == "__main__":
    mcp.run()
