#!/usr/bin/env python
import os, shutil, tarfile
from lib import BackupOptionResolver

options = BackupOptionResolver()

class DrupalSourceMover(object):    
    def __init__(self, tar_location, school_code):
        """
        :type tar_location: String - The absolute path to the tarball.
        :type school_code: String - School code, for example bses, fes, ahs.        
        """
        self.tar_location   = tar_location
        self.school_code    = school_code
        self.tar_directory  = os.path.dirname(tar_location)
        
    def find_drupal_install(self):
        """Sometimes drupal is in the archive in /var/www/<school-code>/drupal
        and sometimes it's in /var/www/<school-code>/docroot. I just want to
        find which it is and encapsulate that logic, here.
        """
        known_path = os.path.join(
            self.tar_directory, 
            "var", 
            "www", 
            "{0}.hcpss.org".format(self.school_code)
        )
        
        candidates = [
            os.path.join(known_path, "drupal"),
            os.path.join(known_path, "docroot"),
        ]
        
        for candidate in candidates:
            if os.path.isdir(candidate):
                return candidate
        
    def move(self, destination):
        """Move the drupal source code to a new location
        :type destination: String - The the root folder. Drupal will be placed
        in a directory INSIDE this directory named after the school code. So,
        don't include the school code here.
        """        
        tar = tarfile.open(self.tar_location)
        tar.extractall(self.tar_directory)
        tar.close()
        
        drupal = self.find_drupal_install();
        
        # Sometimes the archive is empty and copytree throws an error so we just 
        # want to make sure it exists first.
        if drupal:
            # Sometimes there are more than one backup of a school. copytree
            # throws an arror when this happens, so lets just make sure the
            # destination does not exist before we copy it.
            if not os.path.isdir(os.path.join(destination, self.school_code)):
                shutil.copytree(drupal, os.path.join(destination, self.school_code))
                
            shutil.rmtree(os.path.join(self.tar_directory, "var"))

for subdir, dirs, files in os.walk(options.backup_location()):
    for filename in files:
        path        = os.path.join(subdir, filename)
        school_code = filename.split("-")[0].split("_")[-1];
        
        if school_code == "school":
            # Indicative of a test site
            continue
        
        if (filename.endswith(".sql.gz")):
            # This is a sql dump
            destination = "{0}/database/{1}.bak.sql.gz".format(
                options.destination(), 
                school_code)
            
            shutil.copy(path, destination)
        elif (filename.endswith(".tar.gz")):
            drupal = DrupalSourceMover(path, school_code)
            destination = os.path.join(options.destination(), "data")
            drupal.move(destination)
