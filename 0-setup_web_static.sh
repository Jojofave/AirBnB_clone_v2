#!/usr/bin/env bash

# Install Nginx if not already installed
if ! dpkg-query -W -f='${Status}' nginx | grep -q "ok installed"; then
    apt-get update
    apt-get install -y nginx
fi

# Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" > /data/web_static/releases/test/index.html

# Create a symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership of directories to the ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sed -i "s|^\(\s*location / {\).*|\1\n\t\talias /data/web_static/current/;|" $config_file

# Restart Nginx
service nginx restart

exit 0

