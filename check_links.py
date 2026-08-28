"""Check external URLs stored in the site's local CSV source data."""

import argparse
import csv
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
URL_COLUMNS = {"url", "alternate_url", "twitter_url", "google_scholar"}
SOFT_BLOCKS = {401, 403, 405, 406, 418, 429, 451, 500, 502, 503, 598, 999}


def source_urls():
    sources = {}
    for path in sorted(DATA_DIR.glob("*.csv")):
        with path.open(newline="", encoding="utf-8") as file:
            for line_number, row in enumerate(csv.DictReader(file), start=2):
                for column, value in row.items():
                    if not value or column not in URL_COLUMNS:
                        continue
                    if not value.startswith(("https://", "http://")):
                        continue
                    sources.setdefault(value, []).append(
                        f"{path.relative_to(path.parent.parent)}:{line_number}"
                    )
    return sources


def check(url, timeout):
    command = [
            "curl",
            "--location",
            "--silent",
            "--show-error",
            "--output",
            "/dev/null",
            "--write-out",
            "%{http_code}\t%{url_effective}",
            "--connect-timeout",
            str(min(timeout, 5)),
            "--max-time",
            str(timeout),
            "--user-agent",
            "Mozilla/5.0 academic-site-link-checker/1.0",
            url,
        ]
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout + 2
        )
    except subprocess.TimeoutExpired:
        return 598, url, "process timeout"
    output = result.stdout.strip().split("\t", 1)
    status = int(output[0]) if output and output[0].isdigit() else 0
    final_url = output[1] if len(output) == 2 else url
    # Transport/protocol failures are usually bot blocking or transient. DNS
    # failure (curl 6) remains a hard failure because the host no longer exists.
    if result.returncode and result.returncode != 6 and status == 0:
        return 598, final_url, result.stderr.strip()
    return status, final_url, result.stderr.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()

    urls = source_urls()
    failures = []
    restricted = []
    redirects = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        jobs = {executor.submit(check, url, args.timeout): url for url in urls}
        for future in as_completed(jobs):
            url = jobs[future]
            status, final_url, note = future.result()
            if status in SOFT_BLOCKS:
                restricted.append((status, url))
            elif status == 0 or status >= 400:
                failures.append((status, url, note))
            elif final_url.rstrip("/") != url.rstrip("/"):
                redirects.append((url, final_url))

    for status, url, note in sorted(failures):
        print(f"FAIL {status or 'ERR'} {url} ({note})")
        print(f"     {', '.join(urls[url])}")
    for status, url in sorted(restricted):
        print(f"RESTRICTED {status} {url}")
    for url, final_url in sorted(redirects):
        print(f"REDIRECT {url} -> {final_url}")

    print(
        f"Checked {len(urls)} URLs: {len(failures)} failed, "
        f"{len(restricted)} access-restricted, {len(redirects)} redirected."
    )
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
