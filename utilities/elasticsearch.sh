#!/usr/bin/env bash

SCHOOL=$1
SCRIPTDIR=`dirname $0`
PROJECTDIR=`$SCRIPTDIR/get_project_directory.py`
SCHOOL_DIR="/var/www/schools/$SCHOOL"
SCHOOL_CODE=`drush --root=$SCHOOL_DIR vget hcpss_school_code --exact`

# Create the index.
curl -X PUT "http://searchapi.hocoschools.org:9200/$SCHOOL_CODE/" -d '{
    "settings" : {
        "index" : {
            "number_of_shards" : 1,
            "number_of_replicas" : 0
        }
    }
}'

# Always a good idea to clear the cache.
drush cc all
drush --root=$SCHOOL_DIR cc all

ln -s /vagrant/extensions/modules/schoolsite_deploy $SCHOOL_DIR/sites/all/modules/schoolsite_deploy
drush --root=$SCHOOL_DIR cc all

drush --root=$SCHOOL_DIR en -y \
    composer_manager \
    search_api \
    search_api_multi \
    elasticsearch_connector

composer --working-dir=$SCHOOL_DIR/sites/default/files/composer install

drush --root=$SCHOOL_DIR updb -y

drush --root=$SCHOOL_DIR search-api-index
