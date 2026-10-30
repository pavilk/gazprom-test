#!/usr/bin/env bash
set -euo pipefail

APP_USER=hello-app
APP_DIR=/opt/hello-app

apt-get update
apt-get install -y python3-venv iputils-ping

id -u "$APP_USER" >/dev/null 2>&1 || \
    useradd --system --no-create-home --shell /usr/sbin/nologin "$APP_USER"

mkdir -p "$APP_DIR"
cp -r app requirements.txt "$APP_DIR"/
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --no-cache-dir -r "$APP_DIR/requirements.txt"
chown -R root:"$APP_USER" "$APP_DIR"
chmod -R o-rwx "$APP_DIR"

install -m 644 deploy/systemd/hello-app.service /etc/systemd/system/hello-app.service
systemctl daemon-reload
systemctl enable --now hello-app

systemctl --no-pager status hello-app
