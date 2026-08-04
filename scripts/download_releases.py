#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

GITHUB_API = "https://api.github.com"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download all release assets for a GitHub repository."
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default="gledesma-bcf/NOAAweatherforecasts",
        help="Owner/Repository as owner/repo (default: gledesma-bcf/NOAAweatherforecasts)",
    )
    parser.add_argument(
        "--output-dir",
        default="releases",
        help="Directory where release assets will be saved (default: releases)",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="GitHub token. If omitted, GITHUB_TOKEN environment variable is used.",
    )
    return parser.parse_args()


def auth_headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "download-releases"}
    token = token or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_releases(owner: str, repo: str, headers: dict[str, str]) -> list[dict]:
    releases: list[dict] = []
    page = 1

    while True:
        url = f"{GITHUB_API}/repos/{owner}/{repo}/releases"
        response = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        response.raise_for_status()
        data = response.json()

        if not data:
            break

        releases.extend(data)
        if len(data) < 100:
            break
        page += 1

    return releases


def download_asset(asset: dict, output_dir: Path, headers: dict[str, str]) -> Path:
    asset_name = asset["name"] or asset["label"] or "asset"
    safe_name = asset_name.replace("/", "_")
    target_path = output_dir / safe_name

    response = requests.get(asset["browser_download_url"], headers=headers, stream=True)
    response.raise_for_status()

    with response:
        with target_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    handle.write(chunk)

    return target_path


def download_release(release: dict, output_dir: Path, headers: dict[str, str]) -> list[Path]:
    release_dir = output_dir / release["tag_name"]
    release_dir.mkdir(parents=True, exist_ok=True)

    downloaded: list[Path] = []
    for asset in release.get("assets", []):
        downloaded.append(download_asset(asset, release_dir, headers))

    return downloaded


def main() -> int:
    args = parse_args()
    owner, repo = args.repo.split("/", 1)
    headers = auth_headers(args.token)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        releases = fetch_releases(owner, repo, headers)
    except requests.RequestException as exc:
        print(f"Failed to fetch releases: {exc}", file=sys.stderr)
        return 1

    if not releases:
        print("No releases found.")
        return 0

    for release in releases:
        try:
            downloaded = download_release(release, output_dir, headers)
        except requests.RequestException as exc:
            print(f"Failed to download assets for {release.get('tag_name')}: {exc}", file=sys.stderr)
            continue

        if downloaded:
            print(f"Downloaded {len(downloaded)} asset(s) for {release['tag_name']}")
        else:
            print(f"No assets found for {release['tag_name']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
