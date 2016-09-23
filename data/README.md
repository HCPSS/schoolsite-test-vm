Put your schoolsite Drupal installation in this directory. Call it by its "school code".
When you are done this directory should be full of directories called:

aes
ahs
bbes
bbms
etc.

<VirtualHost *:80>
\tDocumentRoot "/var/www/html/${schoolcode}"
\tServerName /var/www/html/README.md.schools.dev
\t<Directory /var/www/html//var/www/html/README.md/>
\t\tOptions FollowSymLinks
\t\tAllowOverride None
\t\tRequire all granted
\t</Directory>
</VirtualHost>
