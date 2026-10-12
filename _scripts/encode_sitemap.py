"""Post-render step: percent-encode the sitemap's URLs.

Several post folders have spaces in their names ("posts/2026 Xenolith Melting/"), and Quarto
writes those paths into sitemap.xml as they are. A sitemap URL must be escaped, so a space
becomes %20 here; nothing else in the URL changes.
"""

import os
import re
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

out = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs"))
sitemap = out / "sitemap.xml"
if sitemap.exists():

    def encode(match: re.Match) -> str:
        parts = urlsplit(match.group(1))
        path = quote(parts.path, safe="/%")
        return f"<loc>{urlunsplit(parts._replace(path=path))}</loc>"

    sitemap.write_text(re.sub(r"<loc>(.*?)</loc>", encode, sitemap.read_text()))
