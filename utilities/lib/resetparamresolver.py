import argparse

class ResetParamResolver(object):
    """Resolve user input params"""
    
    def __init__(self):        
        self.args = argparse.ArgumentParser()
        
        self.set_params()
        
    def set_params(self):
        """Manage parameters"""
        
        self.args.add_argument("school_code", help="School code")
        
    def parse(self):
        return self.args.parse_args()
        