# Healthcare AI Assistant - Communication Protocols

## A2A (Agent-to-Agent) Protocol
Agents communicate using the COIN protocol.

### Message Structure
See `a2a-schema.json` for full schema details.

### Supported Actions
- `assess_symptoms`
- `find_slots`
- `get_summary`
- `create_followup`

## MCP Tools Protocol
The MCP Server exposes tools as REST APIs.
The orchestrator or agents invoke them by sending HTTP POST requests.
