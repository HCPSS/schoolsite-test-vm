#!/usr/bin/env python
from lib import BatchCommandParamResolver
import os, subprocess

options = BatchCommandParamResolver()

root = "/var/www/schools"
for item in os.listdir(root):
    target = os.path.join(root, item)
    if os.path.isdir(target):
        
        command = options.parse().command.format(target=target, school_code=item)
        
        print "Command \"{0}\" running on {1}".format(command, target)
        p = subprocess.Popen([command], cwd=target, shell=True)
        p.wait()
