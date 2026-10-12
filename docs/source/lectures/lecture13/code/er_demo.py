"""L13 demonstration: ask an embodied-reasoning model about a cell.

The client side is the real google-genai SDK, called the way the
Gemini API robotics overview page shows (client.interactions.create).
The server side is a SCRIPTED STAND-IN: no API key exists here, so an
httpx mock transport catches the request and returns answers written
in advance. A real model's answers vary.

The images are synthetic 8 x 8 gray PNG files, not ARIAC camera
images.
The cell IDs and the stand-in's answers are chosen for this example.

Run: python3 er_demo.py   (needs google-genai and jsonschema)
"""

import base64
import json
import struct
import zlib

import httpx
from google import genai
from google.genai import types
from jsonschema import Draft7Validator

MODEL = "gemini-robotics-er-2-preview"
CELLS = [f"c{n:02d}" for n in range(1, 13)]

PROMPT = (
    "The image shows one battery cell on a conveyor. List each "
    "surface defect: a dent is a round hollow, a scratch is a long "
    "narrow groove, a bulge is a round bump. Answer only with JSON: "
    '{"defective": <true|false>, "defects": [{"type": '
    '<"DENT"|"SCRATCH"|"BULGE">, "point": [y, x]}]}. '
    "The points are in [y, x] format normalized to 0-1000."
)

ANSWER_SCHEMA = {
    "type": "object",
    "required": ["defective", "defects"],
    "additionalProperties": False,
    "properties": {
        "defective": {"type": "boolean"},
        "defects": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type", "point"],
                "properties": {
                    "type": {"enum": ["DENT", "SCRATCH", "BULGE"]},
                    "point": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "items": {"type": "integer",
                                  "minimum": 0, "maximum": 1000},
                    },
                },
            },
        },
    },
}

# The stand-in's scripted answers, one per call, in call order.
NONE = {"defective": False, "defects": []}


def one(kind, y, x):
    return {"defective": True,
            "defects": [{"type": kind, "point": [y, x]}]}


SCRIPT = [
    NONE, one("DENT", 412, 530), NONE, NONE, one("DENT", 388, 471),
    one("BULGE", 455, 602), one("BULGE", 431, 515), NONE,
    one("SCRATCH", 300, 498), one("CRACK", 520, 505),
    one("BULGE", 470, 489), NONE,
]


def placeholder_png():
    """A synthetic 8 x 8 gray PNG (not a camera image)."""
    def chunk(tag, data):
        body = tag + data
        crc = zlib.crc32(body) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + body + struct.pack(
            ">I", crc)
    head = struct.pack(">IIBBBBB", 8, 8, 8, 0, 0, 0, 0)
    rows = b"".join(b"\x00" + bytes([128] * 8) for _ in range(8))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head)
            + chunk(b"IDAT", zlib.compress(rows))
            + chunk(b"IEND", b""))


class StandIn:
    """Scripted stand-in for the model server (not a real model)."""

    def __init__(self):
        self.requests = []
        self.answers = iter(SCRIPT)

    def __call__(self, request):
        self.requests.append(json.loads(request.content))
        self.method, self.url = request.method, request.url
        text = json.dumps(next(self.answers))
        reply = {"id": f"standin-{len(self.requests)}",
                 "status": "completed",
                 "steps": [{"type": "model_output",
                            "content": [{"type": "text",
                                         "text": text}]}]}
        return httpx.Response(200, json=reply)


def make_client(stand_in):
    mock = httpx.Client(transport=httpx.MockTransport(stand_in))
    options = types.HttpOptions(httpx_client=mock)
    return genai.Client(api_key="no-key-stand-in",
                        http_options=options)


def ask(client, png):
    response = client.interactions.create(
        model=MODEL,
        input=[
            {"type": "image", "mime_type": "image/png",
             "data": base64.b64encode(png).decode()},
            {"type": "text", "text": PROMPT},
        ],
        generation_config={"thinking_level": "medium"},
    )
    return response.output_text


def check(text):
    """Return (answer, errors): the parsed JSON and schema errors."""
    try:
        answer = json.loads(text)
    except json.JSONDecodeError as err:
        return None, [f"not JSON: {err.msg}"]
    found = Draft7Validator(ANSWER_SCHEMA).iter_errors(answer)
    errors = sorted(
        f"{'.'.join(map(str, e.absolute_path))}: {e.message}"
        for e in found)
    return answer, errors


def ask_all():
    """Ask about every cell; return the stand-in and the answers."""
    stand_in = StandIn()
    client = make_client(stand_in)
    png = placeholder_png()
    results = {}
    for cell in CELLS:
        text = ask(client, png)
        results[cell] = (text,) + check(text)
    return stand_in, results


def show_request(body):
    """Print the request body, image data and prompt shortened."""
    assert set(body) == {"model", "generation_config", "input"}
    print("{")
    print(f'  "model": {json.dumps(body["model"])},')
    config = json.dumps(body["generation_config"])
    print(f'  "generation_config": {config},')
    print('  "input": [')
    for turn in body["input"]:
        assert set(turn) == {"content", "type"}
        print("    {")
        print('     "content": [')
        parts = turn["content"]
        for k, part in enumerate(parts):
            part = dict(part)
            if "data" in part:
                part["data"] = f"<{len(part['data'])} chars>"
            if "text" in part:
                part["text"] = part["text"][:24] + " ..."
            end = "," if k < len(parts) - 1 else ""
            print("      " + json.dumps(part) + end)
        print("     ],")
        print(f'     "type": {json.dumps(turn["type"])}')
        print("    }")
    print("  ]")
    print("}")


def main():
    stand_in, results = ask_all()
    print(f"Requests sent: {len(stand_in.requests)}")
    url = stand_in.url
    print(f"Each one: {stand_in.method} to {url.host}")
    print(f"          path {url.path}")
    show_request(stand_in.requests[0])
    print()
    text, answer, _ = results["c07"]
    print("Raw answer text for c07 (scripted stand-in):")
    print(text)
    print()
    print("Schema check of every answer:")
    for cell, (text, answer, errors) in results.items():
        if errors:
            print(f"  {cell} rejected")
            for error in errors:
                print(f"      {error}")
            continue
        kinds = [d["type"] for d in answer["defects"]] or ["none"]
        print(f"  {cell} valid     defects: {', '.join(kinds)}")

if __name__ == "__main__":
    main()
