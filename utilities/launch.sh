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

# Is elasticsearch running?
ELASTICRUNNING=`docker inspect -f {{.State.Running}} school_elasticsearch 2> /dev/null`
if [ "$ELASTICRUNNING" != "true" ]; then
	echo "+++++++++++++++++ Start Elasticsearch"
	docker run -d --name school_elasticsearch \
		-p 9200:9200 \
		-e "http.host=0.0.0.0" \
		-e "transport.host=127.0.0.1" \
		docker.elastic.co/elasticsearch/elasticsearch:5.2.2
fi

# Start the DB
echo "+++++++++++++++++ Start MySQL"
docker run -d \
    --name ${SCHOOL}_db \
    -e MYSQL_ROOT_PASSWORD=root \
    -v $PROJECTDIR/database/$SCHOOL.bak.sql:/docker-entrypoint-initdb.d/$SCHOOL.bak.sql \
    -v $PROJECTDIR/.data/$SCHOOL:/var/lib/mysql \
    mysql --max-allowed-packet=64M

# Does the web image exist?
if [[ "$(docker images -q school_web:latest 2> /dev/null)" == "" ]]; then
	echo "+++++++++++++++++ Build Web"
    docker build -t school_web $PROJECTDIR/docker/web
fi

# Wait for the database to be ready for connections before we start the web container.
while ! is_db_ready; do
	echo "+++++++++++++++++ Waiting..."
    sleep 1
done

# Start the web container.
echo "+++++++++++++++++ Start Web"
docker run -d \
    --name ${SCHOOL}_web \
    --link ${SCHOOL}_db:drupal_db \
	--link school_elasticsearch:elasticsearch \
    -e SCHOOLCODE=$SCHOOL \
    -e VIRTUAL_HOST=$SCHOOL.schools.dev \
    -v $PROJECTDIR/data/$SCHOOL:/var/www/html \
    -v $PROJECTDIR/utilities:/srv/utilities \
    -v $PROJECTDIR/extensions:/srv/extensions \
    school_web
