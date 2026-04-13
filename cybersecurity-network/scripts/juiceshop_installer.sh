#!/bin/bash

set -e

USER_NAME="${SUDO_USER:-$(whoami)}"
HOME_DIR=$(eval echo "~$USER_NAME")

if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run this script with sudo"
  exit 1
fi

if [ -z "$SUDO_USER" ]; then
  echo "[!] This script must be run via sudo, not as root directly"
  exit 1
fi

echo "[+] Installing dependencies..."
sudo pacman -S --noconfirm base-devel python git curl

echo "[+] Installing NVM..."
sudo -u $USER_NAME bash <<EOF
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
EOF

echo "[+] Loading NVM and installing Node..."
sudo -u $USER_NAME bash <<EOF
export NVM_DIR="$HOME_DIR/.nvm"
source "$HOME_DIR/.nvm/nvm.sh"
nvm install 22
nvm use 22
EOF

echo "[+] Cloning Juice Shop..."
cd /opt
sudo git clone https://github.com/juice-shop/juice-shop.git || true
sudo chown -R $USER_NAME:$USER_NAME juice-shop

echo "[+] Installing Node dependencies..."
sudo -u $USER_NAME bash <<EOF
export NVM_DIR="$HOME_DIR/.nvm"
source "$HOME_DIR/.nvm/nvm.sh"
cd /opt/juice-shop
rm -rf node_modules package-lock.json
npm install
EOF

echo "[+] Creating start script..."
cat <<EOF | sudo tee /opt/juice-shop/start.sh
#!/bin/bash
export NVM_DIR="$HOME_DIR/.nvm"
source "$HOME_DIR/.nvm/nvm.sh"
nvm use 22
cd /opt/juice-shop
npm start
EOF

sudo chmod +x /opt/juice-shop/start.sh

echo "[+] Creating systemd service..."
cat <<EOF | sudo tee /etc/systemd/system/juiceshop.service
[Unit]
Description=OWASP Juice Shop
After=network.target

[Service]
Type=simple
User=$USER_NAME
WorkingDirectory=/opt/juice-shop
ExecStart=/opt/juice-shop/start.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "[+] Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable juiceshop
sudo systemctl start juiceshop

echo "[+] DONE Juice Shop is running"
