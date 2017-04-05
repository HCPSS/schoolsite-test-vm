import os, shutil, tarfile, gzip, tempfile

class SchoolMover(object):
    def __init__(self, path, code, destination):
        self.path        = path
        self.code        = code
        self.destination = destination

    def move(self):
        """Determine the type of data we are moving and move it."""
        if self.path.endswith(".sql.gz"):
            self.move_database()
        elif self.path.endswith(".tar.gz"):
            self.move_data()

    def move_database(self):
        """Unarchive and move the sql backup."""
        dest_file_path = "{0}/database/{1}.bak.sql".format(
            self.destination,
            self.code)

        # Read the gzip sql.
        tar = gzip.open(self.path)
        sql_string = tar.read()
        tar.close()

        # The backup files do not have a database name in them. In order to
        # easily import the files, we want to add that.
        sql_string = "-- {0}\nCREATE DATABASE {1};\nUSE {1};\n\n{2}".format(
            "Added by backup processor",
            self.code,
            sql_string)

        # Write the ouput.
        sql_file = open(dest_file_path, 'w')
        sql_file.write(sql_string)
        sql_file.close()

    def move_data(self):
        """Unarchive and move the Drupal directory."""
        temp_dir = tempfile.mkdtemp()

        # Extract the tarball to a temp location.
        tar = tarfile.open(self.path)
        tar.extractall(temp_dir)
        tar.close()

        drupal_data = SchoolMover.find_drupal_install(temp_dir, self.code)

        # Sometimes the archive is empty and copytree throws an error so we just
        # want to make sure it exists first.
        if drupal_data:
            # Sometimes there are more than one backup of a school. copytree
            # throws an arror when this happens, so lets just make sure the
            # destination does not exist before we copy it.
            if not os.path.isdir(os.path.join(self.destination, self.code)):
                shutil.copytree(
                    drupal_data,
                    os.path.join(self.destination, "data", self.code))

        else:
            print("there is no drupal data")

        shutil.rmtree(temp_dir)

    @staticmethod
    def find_drupal_install(tar_directory, school_code):
        """Sometimes drupal is in the archive in /var/www/<school-code>/drupal
        and sometimes it's in /var/www/<school-code>/docroot. I just want to
        find which it is and encapsulate that logic, here.
        """
        known_path = os.path.join(
            tar_directory,
            "var",
            "www",
            "{0}.hcpss.org".format(school_code.replace("_", "-"))
        )

        candidates = [
            os.path.join(known_path, "drupal"),
            os.path.join(known_path, "docroot"),
        ]

        for candidate in candidates:
            if os.path.isdir(candidate):
                return candidate
