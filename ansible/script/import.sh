#!/usr/bin/env bash

for f in /seed/*; do
    if [ ${f: -4} == ".sql" ]; then
        schoolcode=${f%%.*}
        schoolcode=${schoolcode: 6}
        echo "CREATE DATABASE $schoolcode;" | mysql -u root -proot
        mysql -u root -proot $schoolcode < $f
    fi
done
