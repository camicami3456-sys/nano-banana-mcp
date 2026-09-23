import os
import base64
from mcp.server.fastmcp import FastMCP
from google import genai
from google.genai import types

mcp = FastMCP("Nano Banana Image Generator")

MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

@mcp.tool()
def generate_image(
    prompt: str,
    aspect_ratio: str = "1:1",
) -> dict:
    """Generate an image with Google's Nano Banana (Gemini image model).

    Args:
        prompt: Detailed image-generation or image-editing instruction.
        aspect_ratio: One of 1:1, 3:4, 4:3, 16:9, or 9:16.
    """
    allowed = {"1:1", "3:4", "4:3", "16:9", "9:16"}
    if aspect_ratio not in allowed:
        raise ValueError(f"aspect_ratio must be one of: {', '.join(sorted(allowed))}")

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            response_format={"image": {"aspect_ratio": aspect_ratio}},
        ),
    )

    for part in response.candidates[0].content.parts:
        if getattr(part, "inline_data", None):
            data = part.inline_data.data
            if isinstance(data, str):
                data = base64.b64decode(data)
            mime = part.inline_data.mime_type or "image/png"
            b64 = base64.b64encode(data).decode("ascii")
            return {
                "mime_type": mime,
                "base64": b64,
                "model": MODEL,
            }

    raise RuntimeError("Nano Banana did not return an image.")

if __name__ == "__main__":
    # Claude's remote connector requires a public HTTPS MCP endpoint.
    mcp.run(transport="streamable-http", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
