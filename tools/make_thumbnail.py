#!/usr/bin/env python3
"""Build the Workshop preview for 16:9 Loading Screens.

The comparison is made from a single screenshot, so both halves are literally
the same pixels:

The image is the full 16:9 illustration, lifted straight out of a screenshot
taken with the mod on, with the part vanilla throws away dimmed and the part
it keeps outlined.

That band is exact, not an impression. Vanilla draws the 3840x2160 image with
fittype = centercrop, which on 5120x1440 scales it by
max(5120/3840, 1440/2160) = 1.333 to 5120x2880 and keeps the middle 1440 of
those rows - the middle 50% of the artwork by height, at full width.

Designed for 200x200, the size Steam renders previews at in listings. A first
version put the before and after side by side as two 32:9 strips; at 200px
they were 48 pixels tall each and the difference did not read. One picture
with the crop marked on it does.

    thumbnail.png         1280x1280, the Workshop preview
    thumbnail-200px.png   the legibility check, regenerated every run

Usage: tools/make_thumbnail.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

SRC = "/home/nikita/Pictures/Screenshots/Screenshot_20260912_214508.png"
OUT = pathlib.Path(__file__).resolve().parent.parent

S = 1280
MARGIN = 96
BG = (9, 12, 18)
FG = (238, 240, 244)
MUTED = (128, 136, 150)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fit(d, text, avail, start=260, minimum=24):
    size = start
    while size > minimum and d.textlength(text, font=ImageFont.truetype(FB, size)) > avail:
        size -= 2
    return ImageFont.truetype(FB, size)


def artwork(width):
    """The full 16:9 illustration, lifted out of the screenshot."""
    shot = Image.open(SRC).convert("RGB")
    w, h = shot.size
    stage_w = round(h * 16 / 9)
    x0 = (w - stage_w) // 2
    art = shot.crop((x0, 0, x0 + stage_w, h))
    return art.resize((width, round(width * 9 / 16)), Image.LANCZOS)


def main():
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    avail = S - 2 * MARGIN

    d.text((MARGIN, 66), " ".join("CRUSADER KINGS III"),
           font=ImageFont.truetype(FB, 30), fill=MUTED)

    f1 = fit(d, "LOADING SCREENS", avail)
    f2 = fit(d, "IN 16:9", avail, start=176)
    d.text((MARGIN, 112), "LOADING SCREENS", font=f1, fill=FG)
    y = 112 + f1.size + 10
    d.text((MARGIN, y), "IN 16:9", font=f2, fill=FG)

    art = artwork(avail)
    top = y + f2.size + 58

    # Dim everything outside the middle 50% by height - that band is the whole
    # of what vanilla puts on an ultrawide screen.
    band_top, band_bottom = art.height // 4, art.height - art.height // 4
    dim = art.copy()
    ImageDraw.Draw(dim, "RGBA").rectangle([0, 0, art.width, band_top],
                                          fill=(6, 8, 12, 105))
    ImageDraw.Draw(dim, "RGBA").rectangle([0, band_bottom, art.width, art.height],
                                          fill=(6, 8, 12, 105))
    im.paste(dim, (MARGIN, top))

    d.rectangle([MARGIN, top + band_top, MARGIN + art.width - 1, top + band_bottom],
                outline=(226, 96, 74), width=4)

    cap = ImageFont.truetype(FB, 31)
    d.text((MARGIN, top + art.height + 22),
           "vanilla shows only the band. this mod shows the picture.",
           font=cap, fill=MUTED)

    # 1024 keeps the file comfortably under the Workshop's 1 MB cap; the
    # preview is never rendered anywhere near that size anyway.
    out = im.resize((1024, 1024), Image.LANCZOS)
    out.save(OUT / "thumbnail.png", optimize=True)
    out.resize((200, 200), Image.LANCZOS).save(OUT / "thumbnail-200px.png")
    kb = (OUT / "thumbnail.png").stat().st_size / 1024
    print(f"thumbnail.png {out.size[0]}x{out.size[1]} {kb:.0f} KB")


if __name__ == "__main__":
    main()
