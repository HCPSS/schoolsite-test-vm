#!/usr/bin/env python
from __future__ import print_function
import os, shutil, tarfile, sys
from lib import BackupOptionResolver
from multiprocessing import Process
import tempfile
import gzip

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

    def find_drupal_install(self, temp_dir):
        """Sometimes drupal is in the archive in /var/www/<school-code>/drupal
        and sometimes it's in /var/www/<school-code>/docroot. I just want to
        find which it is and encapsulate that logic, here.
        """
        known_path = os.path.join(
            temp_dir,
            "var",
            "www",
            "{0}.hcpss.org".format(self.school_code.replace("_", "-"))
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
        temp_dir = tempfile.mkdtemp()
        tar = tarfile.open(self.tar_location)
        tar.extractall(temp_dir)
        tar.close()

        drupal = self.find_drupal_install(temp_dir)

        # Sometimes the archive is empty and copytree throws an error so we just
        # want to make sure it exists first.
        if drupal:
            # Sometimes there are more than one backup of a school. copytree
            # throws an arror when this happens, so lets just make sure the
            # destination does not exist before we copy it.
            if not os.path.isdir(destination):
                shutil.copytree(drupal, destination)
            else:
                print("Duplicate installtion found for {0}".format(school_code), file=sys.stderr)
        else:
            print("Could not find Drupal installation for {0}".format(school_code), file=sys.stderr)

        shutil.rmtree(temp_dir)

def move_sql(path, school_code):
    """Move the SQL tarball
    :type school_code: String - The school code.
    """
    gz = gzip.open(path, "rb")
    directory = os.path.join(options.destination(), "database")
    create_path(directory)
    sql = open(os.path.join(directory, "{0}.bak.sql".format(school_code)), "wb")
    sql.write(gz.read())
    sql.close()
    gz.close()

    print("Moved SQL for {0}".format(school_code))

def move_data(path, school_code):
    """Move the drupal source code.
    :type path: String - The path to the drupal source.
    :type school_code: String - The school code.
    """
    drupal = DrupalSourceMover(path, school_code)
    directory = os.path.join(options.destination(), "data")
    create_path(directory)
    drupal.move(os.path.join(directory, school_code))
    print("Moved data for {0}".format(school_code))

def create_path(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except (OSError):
            # Sometimes different threads are checking the existance of the same
            # directory. This can cause errors, but we don't really care.
            pass

def process_file(filename, path, school_code):
    """Process a tarball that is either a sql dump or drupal source code.
    :type filename: String - The path to the tarball.
    :type path: String - The path to the drupal source.
    :type school_code: String - The school code.
    """
    if (filename.endswith(".sql.gz")):
        move_sql(path, school_code)
    elif (filename.endswith(".tar.gz")):
        move_data(path, school_code)

processes = []
for subdir, dirs, files in os.walk(options.backup_location()):
    for filename in files:
        path = os.path.join(subdir, filename)
        school_code = filename.split("-")[0].split("_", 2)[-1]

        if school_code == "school":
            # Indicative of a test site
            continue

        p = Process(target=process_file, args=(filename, path, school_code,))
        p.start()
        processes.append(p)

for p in processes:
    p.join()
