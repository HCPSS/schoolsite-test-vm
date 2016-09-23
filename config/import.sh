#!/usr/bin/env bash

echo "[client]" >> /tmp/config.cnf
echo "user = root" >> /tmp/config.cnf
echo "password = root" >> /tmp/config.cnf

parallel -j 10 '/bin/bash /process.sh' ::: /seed/*

rm /tmp/config.cnf
