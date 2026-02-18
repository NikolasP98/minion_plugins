# provision-server

End-to-end remote server provisioning for Minion instances — SSH check, dry run, credential collection, setup execution, monitoring, and config registration.

## What it does

Guides the full provisioning lifecycle:

1. Verify SSH connectivity to target server
2. Check for port conflicts with existing instances
3. Dry run to validate configuration
4. Collect credentials (API key, GitHub PAT, gateway port)
5. Execute provisioning via `setup/setup.sh`
6. Monitor progress through all phases (00-70)
7. Register server in config files
8. Run lessons-learned for improvement observations

## Prerequisites

This plugin is designed for the Minion project and requires:

- The `setup/` framework from the Minion repository
- SSH access to the target server
- Server config files at `.github/servers/`

## Skills

- `provision-server` — Main provisioning workflow

## Usage

```
/provision-server
```

Or trigger with: "provision server", "deploy new instance", "set up VPS", "add server"
