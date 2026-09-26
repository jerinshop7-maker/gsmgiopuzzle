"""Capture public GSMG puzzle repositories and issue material.

This tool preserves repository history, raw assets, and metadata so later
claims can be traced back to a specific commit or issue id. It does not
alter any remote state. GitHub API access is anonymous by default and
respects rate limits with retry/backoff.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

from .paths import RAW, ensure_dirs
from .provenance import fingerprint, now_utc_iso, write_json

ISSUE_API = "https://api.github.com/repos/{owner_repo}/issues?state=all&per_page=100&page={page}"
ISSUE_COMMENT_API = "https://api.github.com/repos/{owner_repo}/issues/{number}/comments?per_page=100&page={page}"


def api_headers() -> dict:
    headers = {"User-Agent": "gsmg-forensic-capture/0.1", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_json(url: str, max_attempts: int = 5) -> dict | list:
    headers = api_headers()
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code in (403, 429):
                wait = min(60, 2 ** attempt)
                print(f"  rate-limited on {url}; waiting {wait}s (attempt {attempt})", flush=True)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def git_available() -> bool:
    return shutil.which("git") is not None


def clone_or_update(url: str, target: Path) -> None:
    if not git_available():
        raise RuntimeError("git is not available in PATH")
    if (target / ".git").exists():
        subprocess.run(["git", "-C", str(target), "fetch", "--all", "--prune"], check=True)
    else:
        target.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--mirror", url, str(target / ".git")], check=True)
        subprocess.run(["git", "clone", str(target / ".git"), str(target / "working")], check=True)


def repository_facts(target: Path) -> dict:
    working = target / "working" if (target / "working").exists() else target
    head = subprocess.run(
        ["git", "-C", str(working), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    remotes = subprocess.run(
        ["git", "-C", str(working), "remote", "-v"], capture_output=True, text=True, check=True
    ).stdout.strip()
    log = subprocess.run(
        ["git", "-C", str(working), "log", "--all", "--date=iso-strict", "--oneline"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return {"head": head, "remotes": remotes, "log_tail": log.splitlines()[-10:]}


def persist_issues(owner_repo: str, target: Path) -> dict:
    page = 1
    all_issues = []
    while True:
        issues = fetch_json(ISSUE_API.format(owner_repo=owner_repo, page=page))
        if not issues:
            break
        all_issues.extend(issues)
        page += 1

    index_path = target / "issues.jsonl"
    with index_path.open("w", encoding="utf-8") as handle:
        for issue in all_issues:
            number = issue.get("number")
            handle.write(json.dumps(issue, sort_keys=True) + "\n")
            if number is not None:
                persist_issue_comments(owner_repo, number, target)
    return {"issue_count": len(all_issues), "index": str(index_path)}


def persist_issue_comments(owner_repo: str, number: int, target: Path) -> None:
    page = 1
    while True:
        comments = fetch_json(ISSUE_COMMENT_API.format(owner_repo=owner_repo, number=number, page=page))
        if not comments:
            break
        comment_path = target / "issues" / f"{number}" / "comments.jsonl"
        comment_path.parent.mkdir(parents=True, exist_ok=True)
        with comment_path.open("w", encoding="utf-8") as handle:
            for comment in comments:
                handle.write(json.dumps(comment, sort_keys=True) + "\n")
        page += 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owner_repo", help="GitHub owner/repo slug.")
    parser.add_argument("--no-clone", action="store_true", help="Skip cloning, only fetch issues.")
    parser.add_argument("--issues-only", action="store_true", help="Only fetch issues, skip cloning.")
    args = parser.parse_args(argv)

    ensure_dirs()
    target = RAW / "github" / args.owner_repo.replace("/", "-")
    target.mkdir(parents=True, exist_ok=True)
    write_json(target / "provenance.json", {
        "owner_repo": args.owner_repo,
        "acquired_at_utc": now_utc_iso(),
        "fingerprint": fingerprint(),
    })

    if not args.issues_only and not args.no_clone:
        clone_or_update(f"https://github.com/{args.owner_repo}.git", target)
        facts = repository_facts(target)
        write_json(target / "repository_facts.json", facts)

    if not args.no_clone or args.issues_only:
        try:
            summary = persist_issues(args.owner_repo, target)
            write_json(target / "issue_summary.json", summary)
        except Exception as exc:
            write_json(target / "issue_summary.json", {"error": str(exc)})
            print(f"issue capture failed: {exc}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
