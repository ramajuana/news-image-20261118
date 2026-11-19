"""news-image-20261118: copy the front-page image to the output directory.

The entry image (entry.png, a 1024x1024 front page summing up the world
news of Wednesday 18 November 2026) lives in this repository next to this
script. This program copies it byte for byte to $MAKEFUN_OUTPUT_DIR
(default /output) as entry.png, after checking the PNG magic bytes, the
IEND trailer (the file is whole), and the 1 MiB size limit.
Standard library only; deterministic: the same input always produces the
same output bytes.
"""

import os
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"
MAX_BYTES = 1_048_576


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")
    with open(source, "rb") as handle:
        data = handle.read()
    if data[: len(PNG_MAGIC)] != PNG_MAGIC:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if not data.endswith(PNG_IEND):
        print("entry.png is truncated: missing IEND chunk", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
