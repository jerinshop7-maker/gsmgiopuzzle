from __future__ import annotations

import json
from pathlib import Path

from scripts import codex_accounts


def write_auth(path: Path, marker: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"marker": marker}), encoding="utf-8")


def test_save_list_and_use_profiles(tmp_path: Path, capsys) -> None:
    home = tmp_path / "codex"
    active = home / "auth.json"
    write_auth(active, "one")

    assert codex_accounts.main(["--codex-home", str(home), "save", "one"]) == 0
    write_auth(active, "two")
    assert codex_accounts.main(["--codex-home", str(home), "save", "two"]) == 0

    assert codex_accounts.main(["--codex-home", str(home), "list"]) == 0
    output = capsys.readouterr().out
    assert "one" in output
    assert "two" in output
    assert "marker" not in output

    assert codex_accounts.main(["--codex-home", str(home), "use", "one"]) == 0
    assert json.loads(active.read_text(encoding="utf-8"))["marker"] == "one"


def test_profile_names_reject_path_traversal(tmp_path: Path) -> None:
    home = tmp_path / "codex"
    write_auth(home / "auth.json", "one")
    assert codex_accounts.main(["--codex-home", str(home), "save", "../escape"]) == 1


def test_saved_credentials_are_private(tmp_path: Path) -> None:
    home = tmp_path / "codex"
    write_auth(home / "auth.json", "one")
    assert codex_accounts.main(["--codex-home", str(home), "save", "one"]) == 0
    assert (home / "account-profiles").stat().st_mode & 0o777 == 0o700
    assert (home / "account-profiles" / "one").stat().st_mode & 0o777 == 0o700
    assert (home / "account-profiles" / "one" / "auth.json").stat().st_mode & 0o777 == 0o600
