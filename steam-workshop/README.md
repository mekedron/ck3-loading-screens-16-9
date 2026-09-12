# Listing texts

    description-en.txt               Steam Workshop, BBCode
    description-ru.txt               Steam Workshop, BBCode
    description-paradoxmods-en.txt   Paradox Mods, plain text
    description-paradoxmods-ru.txt   Paradox Mods, plain text
    short-description-en.txt         one-paragraph summary
    short-description-ru.txt         one-paragraph summary

The Paradox Mods files are **generated** from the Steam ones by
`tools/bbcode_to_plain.py`; edit the BBCode version and re-run it rather than
editing them directly, or the two will drift apart.

**Do not use `[code]` in the Steam files.** Steam has no inline code tag - it
renders `[code]` as a full-width block, so an identifier written mid-sentence
breaks the line and becomes its own boxed paragraph. Write identifiers as
plain text. `[b]`, `[i]` and `[list]` are fine.

## Naming

The mod is called **16:9 Loading Screens**, not an "ultrawide fix". The
distinction is deliberate: the mod changes an aspect ratio, it does not add
wider artwork. Naming it after ultrawide invites people to expect
full-width illustrations that do not exist.

## Preview

`thumbnail.png` in the repository root, built by `tools/make_thumbnail.py`
from a real screenshot. 1024x1024, about 690 KB, under the Workshop's 1 MB
cap. The band outlined on the picture is the exact slice vanilla keeps on
5120x1440 - the middle 50% by height - not an impression of it.

The script also writes `thumbnail-200px.png`, which exists only to check the
image still reads at the size Steam renders previews in listings. A first
version compared before and after as two stacked 32:9 strips; at 200px they
were 48 pixels tall each and the difference did not read at all.
