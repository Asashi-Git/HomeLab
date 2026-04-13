#!/bin/bash
set -e

# INSTALL Packages

echo "[+] Updating system..."
sudo pacman -Syu --noconfirm

echo "[+] Installing Pacman packages..."
sudo pacman -S --noconfirm --needed apache mariadb php php-apache php-gd git msmtp-mta base-devel fakeroot debugedit

# INSTALL YAY (AUR helper)

if ! command -v yay &>/dev/null; then
  echo "[+] Installing yay..."

  git clone https://aur.archlinux.org/yay.git
  cd yay
  makepkg -si --noconfirm
  cd ..
  rm -rf yay
else
  echo "[+] yay is already installed, skipping..."
fi

# INSTALL PHP 7.4 STACK

# echo "[+] Installing PHP 7.4..."
#
# yay -S --noconfirm php74 php74-apache php74-gd

# APACHE CONFIG

echo "[+] Configuring Apache..."

HTTPD_CONF="/etc/httpd/conf/httpd.conf"

# Enable prefork
sudo sed -i 's/^LoadModule mpm_event_module/#LoadModule mpm_event_module/' $HTTPD_CONF
sudo sed -i 's/^#LoadModule mpm_prefork_module/LoadModule mpm_prefork_module/' $HTTPD_CONF

# Enable PHP
if ! grep -q "libphp.so" $HTTPD_CONF; then
  echo "LoadModule php_module modules/libphp.so" | sudo tee -a $HTTPD_CONF
  echo "AddHandler php-script .php" | sudo tee -a $HTTPD_CONF
  echo "Include conf/extra/php_module.conf" | sudo tee -a $HTTPD_CONF
fi

echo "[+] Setting DVWA as default web root..."

sudo sed -i 's#^DocumentRoot ".*"#DocumentRoot "/srv/http/DVWA"#' $HTTPD_CONF
sudo sed -i '/<Directory "\/srv\/http">/,/<\/Directory>/c\<Directory "/srv/http/DVWA">\n    AllowOverride All\n    Require all granted\n</Directory>' $HTTPD_CONF

echo "[+] Making some tweak for DVWA"

sudo sed -i 's/^#LoadModule rewrite_module/LoadModule rewrite_module/' /etc/httpd/conf/httpd.conf
sudo sed -i 's/^;*display_startup_errors\s*=.*/display_startup_errors = On/' /etc/php/php.ini

# PHP CONFIG

echo "[+] Configuring PHP..."

PHP_INI="/etc/php/php.ini"

sudo sed -i 's/^;*allow_url_fopen = .*/allow_url_fopen = On/' $PHP_INI
sudo sed -i 's/^;*allow_url_include = .*/allow_url_include = On/' $PHP_INI
sudo sed -i 's/^;*display_errors = .*/display_errors = On/' $PHP_INI

sudo sed -i 's/^;extension=mysqli/extension=mysqli/' $PHP_INI
sudo sed -i 's/^;extension=pdo_mysql/extension=pdo_mysql/' $PHP_INI
sudo sed -i 's/^;extension=gd/extension=gd/' $PHP_INI

# MARIADB

echo "[+] Initializing MariaDB..."

if [ ! -d "/var/lib/mysql/mysql" ]; then
  sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
fi

sudo systemctl enable mariadb
sudo systemctl start mariadb

# DATABASE

echo "[+] Setting up database..."

DB_PASS="dvwa123"

sudo mariadb -u root <<EOF
CREATE DATABASE IF NOT EXISTS dvwa;
DROP USER IF EXISTS 'dvwa'@'localhost';
CREATE USER 'dvwa'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'localhost';
FLUSH PRIVILEGES;
EOF

# DVWA INSTALL

echo "[+] Installing DVWA..."

sudo mkdir -p /srv/http
cd /srv/http

if [ ! -d "DVWA" ]; then
  sudo git clone https://github.com/digininja/DVWA.git
fi

sudo chown -R http:http DVWA
sudo chmod -R 755 DVWA

# DVWA CONFIG

echo "[+] Configuring DVWA..."

cd DVWA/config

sudo cp -n config.inc.php.dist config.inc.php

sudo sed -i "s/'db_user'.*/'db_user' ] = 'dvwa';/" config.inc.php
sudo sed -i "s/'db_password'.*/'db_password' ] = '$DB_PASS';/" config.inc.php
sudo sed -i "s/'db_database'.*/'db_database' ] = 'dvwa';/" config.inc.php

# START APACHE

echo "[+] Starting Apache..."

sudo systemctl enable httpd
sudo systemctl restart httpd

echo ""
echo "Installation completed!"
echo "URL: http://localhost"
echo "Login: admin / password"
echo ""
echo "Click 'Create / Reset Database'"
