"""
A guided CLI walkthrough: `python -m kit`.

Prints the network details and MetaMask steps, checks the RPC, and optionally generates a
fresh testnet wallet so you can fund it at the faucet and send your first transaction.
"""
from __future__ import annotations

import sys

from .onboard import metamask_instructions, doctor, new_wallet, FAUCET, check_balance


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    print("== Arc testnet onboarding ==\n")
    print(metamask_instructions())
    print()

    print("Checking the RPC...")
    health = doctor()
    if health.get("rpc_reachable") and health.get("chain_id_ok"):
        print(f"  RPC ok, chain id {health['chain_id']}, latest block {health['latest_block']}\n")
    else:
        print(f"  RPC problem: {health}\n")

    if "--wallet" in argv:
        w = new_wallet()
        print("Fresh testnet wallet (testnet only, keep the key secret):")
        print(f"  address:     {w['address']}")
        print(f"  private key: {w['private_key']}")
        print(f"\nFund this address at {FAUCET}, then check it:")
        print(f"  python -m kit --balance {w['address']}\n")

    if "--balance" in argv:
        i = argv.index("--balance")
        addr = argv[i + 1] if i + 1 < len(argv) else None
        if addr:
            print(f"Balance: {check_balance(addr)}")

    if "--wallet" not in argv and "--balance" not in argv:
        print("Next: run `python -m kit --wallet` to create a testnet wallet to fund.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
