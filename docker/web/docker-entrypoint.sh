#!/usr/bin/env bash

chown -R www-data:www-data /var/www/html/sites/default/files

twit \
    /srv/templates/settings.php.tpl \
    /var/www/html/sites/default/settings.php \
    -p '{"schoolcode": '"\"$SCHOOLCODE\""'}' \
    --no-escape

exec "$@"
