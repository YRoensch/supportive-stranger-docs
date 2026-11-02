"""Fail if the public help site contains anything that must stay private.

Run before every sync and in CI:  python scripts/check_public_content.py .

Checks every text file under the given directory for
- secrets: API keys, tokens, private keys, env-var assignments;
- internal architecture: backend hosts, server/provider names, endpoints;
- words the copy must not use.
"""

import pathlib
import re
import sys

RULES = {
    "secret-like value": r"(sk-[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{30,}|ghp_[A-Za-z0-9]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|re_[A-Za-z0-9]{20,})",
    "env var": r"\b[A-Z][A-Z0-9]*_(KEY|TOKEN|SECRET|PASSWORD|API_KEY|EMAIL)\b|process\.env|import\.meta\.env",
    "internal host or architecture": r"railway|up\.railway\.app|localhost|staging|\bbackend\b|\bserver(s)?\b|vertex|postgres|express\.js|capacitor|/generate-|/check-quota|/verify-purchase|/decrement-reflection|/register-device|x-device-token",
    "AI provider name": r"\bclaude\b|anthropic|gemini|imagen|openai|\bgpt\b",
    "banned word": r"\brumina\w*",
}

TEXT_SUFFIXES = {".md", ".txt", ".html", ".yml", ".yaml", ".css", ".js", ".json", ".xml", ".py"}
# The checker itself lists the patterns, and build output is generated from docs/.
SKIP_DIRS = {"scripts", "site", ".git"}


def main(root):
    problems = []
    for path in sorted(pathlib.Path(root).rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if SKIP_DIRS.intersection(path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, pattern in RULES.items():
                if re.search(pattern, line, re.IGNORECASE if label != "env var" else 0):
                    problems.append(f"{path}:{lineno}: {label}: {line.strip()[:120]}")
    if problems:
        print("Public content check FAILED:\n" + "\n".join(problems))
        return 1
    print(f"Public content check passed ({root}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
