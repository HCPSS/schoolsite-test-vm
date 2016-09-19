#!/usr/bin/env bash

school=$1

git clone https://github.com/HCPSS/hcpss_schoolsite_config.git \
	/var/www/schools/$school/sites/all/modules/hcpss_schoolsite_config

git clone \
	https://github.com/HCPSS/hcpss_schoolsite_theme.git \
	/var/www/schools/$school/sites/all/themes/hcpss_schoolsite_theme

ln -s /vagrant/extensions/modules/schoolsite_deploy /var/www/schools/$school/sites/all/modules/schoolsite_deploy

drush dl --root=/var/www/schools/$school shiny -y

drush --root=/var/www/schools/$school en schoolsite_deploy -y
