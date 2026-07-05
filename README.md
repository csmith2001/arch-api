# arch-api

FastAPI wrapper for ComfyUI image generation.

Features:

- FastAPI REST API
- ComfyUI integration
- Docker deployment
- Environment-based configuration
- Static image serving
- Linux service account support

## Architecture

Browser
↓
FastAPI
↓
ComfyUI
↓
AI-Models

## ComfyUI Service

`/etc/systemd/system/comfyui.service`

```ini
[Unit]
Description=ComfyUI
After=network.target

[Service]
User=comfyui
Group=comfyui
WorkingDirectory=/opt/ai-projects/comfyui
ExecStart=/opt/ai-projects/comfyui/.venv/bin/python main.py --listen
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Enable Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable comfyui
sudo systemctl start comfyui
```

## Service Account

```bash
sudo useradd -r -s /usr/sbin/nologin comfyui
```

## Shared Group

```bash
sudo groupadd ai-users
```

## Add Users to Group

```bash
sudo usermod -aG ai-users <username>
sudo usermod -aG ai-users comfyui
```

## Make Service Account Own AI Data

```bash
sudo chown -R comfyui:ai-users /ai-data
```

## Group Read / Write Access

```bash
sudo chmod -R 775 /ai-data
```

## Preserve Group Ownership on New Files

```bash
sudo find /ai-data -type d -exec chmod g+s {} \;
```

## Verify Permissions

```bash
ls -ld /ai-data
ls -ld /ai-data/models
ls -ld /ai-data/workflows
ls -ld /ai-data/output
```

Expected:

```text
drwxrwsr-x comfyui ai-users ...
```

## Verify Service

```bash
sudo systemctl status comfyui
```

Expected:

```text
Active: active (running)
```

## Logs

```bash
journalctl -u comfyui -f
```

# AI Data Layout

```text
/ai-data
├── models
│   ├── checkpoints
│   ├── loras
│   └── vae
├── output
└── workflows
```

## License

This repository is source-available for evaluation and educational
purposes only.

No permission is granted to use, modify, distribute, host, or create
derivative works from this software without written permission from the
copyright holder.

See LICENSE for details.

## Third Party Software

This project integrates with:

- ComfyUI
- FastAPI
- Docker

All third-party software remains subject to its own licensing terms.
