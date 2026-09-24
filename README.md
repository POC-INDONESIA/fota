# POC INDONESIA — Firmware Over-The-Air (FOTA)

OTA update server for POC INDONESIA PTT devices (Quectel EC600M-CNLE).

## How It Works

1. Device polls `manifest.json` every hour (configurable)
2. Compares version + SHA256 hashes of each file
3. Downloads only changed files
4. Reboots if `main.py` (boot stub) was updated

## Repository Structure

```
├── manifest.json          # Version + file hashes (downloaded by device)
└── latest/
    ├── main.py            # Boot stub (auto-run entry point)
    └── pocind/
        ├── config.mpy
        ├── main.mpy
        ├── ptt_link.py
        ├── ...
        └── opening.mp3
```

## Manifest Format

```json
{
  "version": "1.0.0",
  "total_size": 281088,
  "file_count": 28,
  "base_url": "https://raw.githubusercontent.com/POC-INDONESIA/fota/main/",
  "files": [
    {
      "path": "/usr/main.py",
      "size": 1640,
      "sha256": "abc123...",
      "integrity": "sha256-...",
      "url": "latest/main.py"
    }
  ]
}
```

## Deploying Updates

### Option A: Using the generator script

```bash
# From the quectel workspace (where pocind/ lives)
python fota_gen.py --version 1.0.0 --out /path/to/fota-repo

# Push to GitHub
cd /path/to/fota-repo
git add -A
git commit -m "v1.0.0"
git push
```

### Option B: Manual

1. Compile `.py` to `.mpy`: `python -m mpy_cross pocind/*.py`
2. Copy compiled files + assets to `latest/pocind/`
3. Copy boot stub to `latest/main.py`
4. Generate `manifest.json` with SHA256 hashes
5. `git commit && git push`

## Device-Side Update Flow

The device uses `pocind/updater.py`:

```python
from pocind import updater

# Initialize (call once at boot)
updater.init()

# In main loop:
updater.tick()

# Check state
state, name, ver, done, total, msg = updater.status()
if updater.should_reboot():
    updater.reboot_now()
```

### Config Options (`config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `FOTA_URL` | GitHub manifest URL | URL to manifest.json |
| `FOTA_CHECK_SEC` | 3600 (1 hour) | Check interval |
| `FOTA_ENABLED` | True | Master switch |

## Requirements

- Firmware: EC600M-CNLE with `request` module (HTTP client)
- Network: device must have internet access
- GitHub raw URLs: `raw.githubusercontent.com` (no auth needed)

## Safety

- Files verified by SHA256 hash before writing
- Download failures are retried after 2 minutes
- Version field prevents re-downloading same version
- Boot stub is simple and stable (rarely changes)
- Power loss during update: device boots with old files, next check re-downloads
