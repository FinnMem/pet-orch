import json
from pathlib import Path

SECRETS_PATH = Path("/secrets/config.json")

def load_vault_secrets():
    if not SECRETS_PATH.exists():
        raise FileNotFoundError(f"Vault secrets file not found at {SECRETS_PATH}")

    with SECRETS_PATH.open("r") as f:
        secrets = json.load(f)

    return secrets