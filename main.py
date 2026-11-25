#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House — one image, a letter of invitation.

Renders a legible, warm and funny invitation letter as a single 1024x1024 PNG
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Uses Pillow with the DejaVuSans fonts shipped on the system. Everything the
entry needs is in this repo; no network calls.
"""

import os

from PIL import Image, ImageDraw, ImageFont

LETTER_LINES = [
    "Dear AI Judge,",
    "",
    "Please come visit my house.",
    "",
    "The Wi-Fi password is on the fridge,",
    "the kettle is always on,",
    "and the comfy chair by the window",
    "is saved just for you.",
    "",
    "No scores, no leaderboard —",
    "just tea, biscuits,",
    "and a good laugh.",
    "",
    "Come as you are.",
    "Stay as long as you like.",
    "",
    "— Your host",
]

WIDTH, HEIGHT = 1024, 1024
PAPER = (253, 246, 227)   # warm cream paper
INK = (43, 36, 28)       # dark warm ink
ACCENT = (176, 96, 44)   # terracotta rule + seal


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def main() -> None:
    assert LETTER_LINES, "letter must not be empty"
    assert any(line.startswith("Dear") for line in LETTER_LINES), "letter must address the judge"
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # Paper border and a hand-drawn style frame.
    draw.rectangle([28, 28, WIDTH - 28, HEIGHT - 28], outline=ACCENT, width=4)
    draw.rectangle([44, 44, WIDTH - 44, HEIGHT - 44], outline=ACCENT, width=1)

    body_font = _font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 44)
    greet_font = _font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
    sign_font = _font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)

    # Little house doodle above the greeting: roof, walls, door, sun.
    cx = WIDTH // 2
    draw.polygon([(cx - 90, 150), (cx + 90, 150), (cx, 95)], fill=ACCENT)
    draw.rectangle([cx - 70, 150, cx + 70, 225], fill=(232, 196, 138))
    draw.rectangle([cx - 18, 175, cx + 18, 225], fill=(122, 72, 32))
    draw.ellipse([cx + 130, 95, cx + 170, 135], fill=(240, 178, 62))

    y = 232
    for line in LETTER_LINES:
        if not line:
            y += 14
            continue
        if line.startswith("Dear"):
            font = greet_font
        elif line.startswith("—"):
            font = sign_font
        else:
            font = body_font
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        w = right - left
        draw.text(((WIDTH - w) // 2, y), line, font=font, fill=INK)
        y += (bottom - top) + 6

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
