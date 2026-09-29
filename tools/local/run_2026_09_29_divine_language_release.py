#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTS = ROOT / "tools" / "local" / "divine-language-authority"
TARGET = ROOT / "tools" / "local" / "2026-09-29-divine-language-authority.zlib.b64"
EXPECTED_PACKED_LENGTH = 18344
EXPECTED_RAW_SHA256 = "616f64c6e8d1eab8dd87952c9027a24439e4c8f23af9a61ef7de405797d7df65"

parts = sorted(PARTS.glob("part-*.b64"))
if len(parts) != 5:
    raise RuntimeError(f"expected 5 authority chunks, found {len(parts)}")
packed = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
if len(packed) != EXPECTED_PACKED_LENGTH:
    raise RuntimeError(f"authority packed length mismatch: {len(packed)} != {EXPECTED_PACKED_LENGTH}")
raw = zlib.decompress(base64.b64decode(packed, validate=True))
actual = hashlib.sha256(raw).hexdigest()
if actual != EXPECTED_RAW_SHA256:
    raise RuntimeError(f"authority raw SHA-256 mismatch: {actual} != {EXPECTED_RAW_SHA256}")
TARGET.write_text(packed + "\n", encoding="utf-8")

import release_2026_09_29_divine_language as release

release.main()
