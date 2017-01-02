#!/usr/bin/env bash

SCHOOL=$1

SCRIPTDIR=`dirname $0`
PROJECTDIR=`$SCRIPTDIR/get_project_directory.py`

function is_db_ready() {
    docker run -it --rm \
        --link ${SCHOOL}_db:school_db \
        mysql mysqladmin ping -h school_db --silent
}

PROXYRUNNING=`docker inspect -f {{.State.Running}} nginx-proxy 2> /dev/null`
if [ "$PROXYRUNNING" != "true" ]; then
    # The proxy is not running, so start it.
    docker run -d --name nginx-proxy \
        -p 80:80 \
        -v /var/run/docker.sock:/tmp/docker.sock:ro \
        jwilder/nginx-proxy

    # And give it a second to start.
    sleep 1
fi

# Start the DB
docker run -d \
    --name ${SCHOOL}_db \
    -e MYSQL_ROOT_PASSWORD=root \
    -v $PROJECTDIR/database/$SCHOOL.bak.sql:/docker-entrypoint-initdb.d/$SCHOOL.bak.sql \
    mysql --max-allowed-packet=64M

# Does the web image exist?
if [[ "$(docker images -q school_web:latest 2> /dev/null)" == "" ]]; then
    docker build -t school_web $PROJECTDIR/docker/web
fi

# Wait for the database to be ready for connections before we start the web container.
while ! is_db_ready; do
    sleep 1
done

# Start the web container.
docker run -d \
    --name ${SCHOOL}_web \
    --link ${SCHOOL}_db:drupal_db \
    -e SCHOOLCODE=$SCHOOL \
    -e VIRTUAL_HOST=$SCHOOL.schools.dev \
    -v $PROJECTDIR/data/$SCHOOL:/var/www/html \
    -v $PROJECTDIR/utilities:/srv/utilities \
    -v $PROJECTDIR/extensions:/srv/extensions \
    school_web
