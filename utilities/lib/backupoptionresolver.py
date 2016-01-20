import optparse, os

class BackupOptionResolver(object):
    """Resolve user input options"""
    
    def __init__(self):
        self.parser = optparse.OptionParser()
        self.set_options()
        
    def set_options(self):
        """Use optparser to manage options"""
        
        bhelp = "The location of the backup files. This entire directory tree "
        bhelp += "will be searched for any *.sql.gz and *.tar.gz files to act "
        bhelp += "on."
        self.parser.add_option(
            "--backup-location", "-b", 
            help    = bhelp, 
            default = ".")
        
        dhelp = "Where to assemble the code and databases. Code will be placed "
        dhelp += "in a subfolder data/<school-code>. Database dumps will be "
        dhelp += "placed in database/<school-code.bak.sql.gz>."
        
        self.parser.add_option(
            "--destination", "-d", 
            help    = dhelp, 
            default = ".")
        
    def parse(self):
        """Return the raw parsed user supplied values
        :rtype: dict[str, str]
        """
        
        return self.parser.parse_args()[0]
    
    def backup_location(self):
        """Return the location of the manifest file
        :rtype: str
        """
        
        return os.path.abspath(self.parse().backup_location)
    
    def destination(self):
        """Get the assembly location
        :rtype: str
        """
        
        return os.path.abspath(self.parse().destination)
