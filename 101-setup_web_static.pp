# This Puppet manifest sets up a static website served by Nginx

file { '/data/':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test/':
  ensure => 'directory',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

file { '/data/web_static/releases/test/index.html':
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

exec { 'update_permissions':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => '/usr/bin',
  require => [
    File['/data/web_static/releases/test/index.html'],
    File['/data/web_static/current'],
  ],
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Exec['update_permissions'],
}

file { '/etc/nginx/sites-available/default':
  ensure => 'file',
  content => '
server {
    listen 80;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current;
    }
}
',
  require => Service['nginx'],
  notify  => Service['nginx'],
}
