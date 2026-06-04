# arc-onboarding-kit

Get from nothing to a confirmed transaction on Arc testnet in a couple of minutes. It
prints the network details and the MetaMask steps, checks the RPC is healthy, generates a
fresh testnet wallet so you can fund it at the faucet, and sends a first test transaction.
A CLI and a set of [MCP](https://modelcontextprotocol.io) tools.

Arc uses USDC as its native gas token, so the one thing newcomers trip on is expecting ETH
or not seeing their USDC. This kit removes that friction.

## CLI

```bash
uv run -m kit                       # network details, MetaMask steps, RPC health check
uv run -m kit --wallet              # also generate a fresh testnet wallet to fund
uv run -m kit --balance 0xYourAddr  # check a balance
```

Then fund the address at https://faucet.circle.com and you are ready.

## MCP tools

| Tool | What it does |
|------|--------------|
| `onboard_network` | Arc testnet config (RPC, chain id, gas token, explorer, faucet) |
| `onboard_metamask` | copy-paste MetaMask add-network instructions |
| `onboard_new_wallet` | generate a fresh testnet wallet (address and key) |
| `onboard_doctor` | check the RPC is reachable and on chain id 5042002 |
| `onboard_balance` | native USDC balance of an address |
| `onboard_send_test` | send a tiny first transaction (key from ARC_PRIVATE_KEY) |

## Network details

| | |
|---|---|
| Network name | Arc Testnet |
| RPC URL | `https://rpc.testnet.arc.network` |
| Chain ID | `5042002` |
| Currency symbol | USDC |
| Block explorer | https://testnet.arcscan.app |
| Faucet | https://faucet.circle.com |

## Run as an MCP server

```bash
uv run -m kit.server
```

## Safety

Generated wallets are for **testnet only**. Never fund them with real assets, and keep the
private key secret.

## Tests

The chain-free parts (config correctness, MetaMask instructions, wallet generation) are
covered by a deterministic suite:

```bash
uv run -m pytest
```

## License

MIT, see [LICENSE](LICENSE). Part of an agent payments stack for Arc.
