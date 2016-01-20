#!/usr/bin/env python
import os
from lib import ResetParamResolver

params = ResetParamResolver()
school_code = params.parse().school_code

sql = "DROP DATABASE {0};CREATE DATABASE {0};".format(school_code)
drop = 'echo "{0}" | mysql -u root -proot'.format(sql)

zcat = "zcat /vagrant/database/{0}.bak.sql.gz".format(school_code)
dbimport = "{0} | mysql -u root -proot {1}".format(zcat, school_code)

params = "--root=/vagrant/data/{0} --uri={0}.schoolsite.dev".format(school_code)
drush = 'drush upwd --password="admin" {0} "admin"'.format(params)

command = "{0} && {1} && {2}".format(drop, dbimport, drush)
os.system(command)
