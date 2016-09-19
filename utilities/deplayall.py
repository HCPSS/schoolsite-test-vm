#!/usr/bin/env python
import os, subprocess

root = "/var/www/schools"

def link_extension(name, school, exttype):
    target = os.path.join(root, school, "sites/all", exttype, name)
    if not os.path.isdir(target):
        os.symlink(os.path.join("/vagrant/extensions", exttype, name), target)

for item in os.listdir(root):
    target = os.path.join(root, item)
    if os.path.isdir(target):
        # Link our custom modules and theme
        link_extension("hcpss_media", item, "modules")
        link_extension("hcpss_schoolsite_config", item, "modules")
        link_extension("schoolsite_deploy", item, "modules")
        link_extension("hcpss_schoolsite_theme", item, "themes")

        # Make sure we have the Shiny theme.
        p = subprocess.Popen("drush dl -n shiny", cwd=target, shell=True)
        p.wait()

        # Here we go son!
        print(target)
        p = subprocess.Popen("drush en -y schoolsite_deploy", cwd=target, shell=True)
        p.wait()
