#!/usr/bin/env bash

import_database() {
    echo "Creating the $1 database..."
    echo "CREATE DATABASE $1;" | mysql --defaults-extra-file=/tmp/config.cnf
    echo "Importing the $1 database..."
    zcat /seed/$1.bak.sql.gz | mysql --defaults-extra-file=/tmp/config.cnf $1
}

if [ ${1: -7} == ".sql.gz" ]; then
    schoolcode=${1%%.*}
    schoolcode=${schoolcode: 6}
    import_database $schoolcode
fi
