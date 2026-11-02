# Supportive Stranger – public help site

End-user documentation for the Supportive Stranger iPhone app, published with GitHub Pages at
<https://yroensch.github.io/supportive-stranger-docs/>.

- App Store: <https://apps.apple.com/de/app/supportive-stranger/id6760293353?l=en-GB>
- Website: <https://supportive-stranger-app.com>

## How this repository is maintained

This repository is a **published copy**. The source lives in the private app repository under
`docs-site/` and is copied here manually with `scripts/sync-public-docs.sh`. Edit the docs there,
not here – changes made directly in this repository are overwritten by the next sync.

Every push to `main` runs `.github/workflows/pages.yml`, which checks the content
(`scripts/check_public_content.py`), builds the site with MkDocs Material and deploys it to
GitHub Pages.

## Build locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

## Layout

| Path | Contents |
|---|---|
| `mkdocs.yml` | Site configuration and navigation |
| `docs/` | Pages (Markdown), screenshots, app icon, `llms.txt` |
| `hooks/faq_schema.py` | Turns each page's "Frequently asked questions" section into FAQPage JSON-LD |
| `overrides/main.html` | Open Graph tags, app JSON-LD, FAQ JSON-LD |
| `scripts/check_public_content.py` | Fails the build if secrets, internal architecture or banned words appear |

## Adding another language later

Use the `mkdocs-static-i18n` plugin with suffix files (`index.md`, `index.de.md`) and
`extra.alternate` for the language switcher. English URLs stay unchanged; German pages are
served under `/de/`.
