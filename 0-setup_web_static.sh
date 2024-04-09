#!/usr/bin/env bash
# Prepare web servers for deployment of web_static

if ! dpkg -s nginx &> /dev/null; then
    sudo apt update
    sudo apt install nginx -y
fi

mkdir -p /data/web_static/releases/test /data/web_static/shared

echo "<html>
<head>
</head>
<body>
    Welcome to the Matrix!
</body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data
config_path="/etc/nginx/sites-available/default"
sed -i "/listen 80 default_server;/a location /hbnb_static/ {\\n    alias /data/web_static/current/;\\n}" $config_path
service nginx restart

exit 0
