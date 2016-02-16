import argparse

class BatchCommandParamResolver(object):
    """Resolve user input params"""
    
    def __init__(self):        
        self.args = argparse.ArgumentParser()
        
        self.set_params()
        
    def set_params(self):
        """Manage parameters"""
        
        self.args.add_argument("command", help="A command to run on all schools sites.")
        
    def parse(self):
        return self.args.parse_args()
        