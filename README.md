# Claude → Nano Banana via MCP

This project exposes Google's Nano Banana image model as a remote MCP tool for Claude.

## 1. Create a Gemini API key

Create an API key in Google AI Studio and keep it private.

Important: a Google AI/Gemini subscription is separate from Gemini API billing/quota. The API may have a free tier and paid usage depending on the model/account/project.

## 2. Deploy

The included `render.yaml` is designed for Render.

Create a new Web Service from this folder/repository and set:

- `GEMINI_API_KEY` = your Google AI Studio API key
- `GEMINI_IMAGE_MODEL` = `gemini-2.5-flash-image`

The service must be publicly reachable over HTTPS.

After deployment, your MCP endpoint will be:

`https://YOUR-SERVICE-DOMAIN/mcp`

## 3. Add it to Claude

In Claude:

Customize → Connectors → + → Add custom connector

Name:
Nano Banana

URL:
https://YOUR-SERVICE-DOMAIN/mcp

Then connect it.

In a chat, enable the connector from the + menu → Connectors.

## 4. Use it

Examples:

"Generate a 4:5 premium real-estate Instagram image of a modern living room..."

"Create a product photo with a clean beige studio background..."

The tool accepts `prompt` and `aspect_ratio`.

## Security

Do not put your Gemini API key in the source code or commit it to GitHub.
Use the hosting provider's environment-variable/secret settings.
The MCP endpoint should ideally be protected with authentication before exposing it publicly.
