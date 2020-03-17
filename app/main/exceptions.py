class InvalidSite(Exception):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):

        return f"No site with name '{self.name}' found"