# Phase 3a: MCP Setup Complete

**Date:** 2026-05-18
**Status:** ✅ Step 3a closed

## What's configured

Local Hermes (Ubuntu WSL2) `~/.hermes/config.yaml`:

### github MCP server
- Transport: stdio via npx
- Package: @modelcontextprotocol/server-github
- Tools enabled (6/26): create_or_update_file, get_file_contents, push_files, create_pull_request, create_branch, get_pull_request
- Auth: GITHUB_PERSONAL_ACCESS_TOKEN env var from ~/.hermes/.env

### filesystem MCP server
- Transport: stdio via npx
- Package: @modelcontextprotocol/server-filesystem
- Allowed roots: /home/omar/dev/nexoura-agent, /home/omar/dev/nexoura-engagements
- Tools enabled (5/14): read_file, write_file, create_directory, list_directory, list_allowed_directories

## Security note

GitHub PAT was rotated during this phase due to chat-log exposure.
New token replaced old in: local .env, gh CLI, git credentials, Zeabur cloud Hermes.
Old token revoked at github.com/settings/tokens.

## Next: Step 3c

Consult on worker dispatch brief for nexoura-engagement-lifecycle SKILL.md authoring.
