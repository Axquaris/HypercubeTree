class Tree:
    """A simple tree class"""
    
    def __init__(self, label, branches = []):
        self.__label = label
        self.__branches = branches
    
    def is_leaf(self):
        return not self.__branches
    
    def add_branch(self, branch):
        self.__branches += [branch]
        return self
    
    def add_branches(self, branches):
        self.__branches += branches
        return self

    def set_branches(self, branches):
        self.__branches = branches
        return self
    
    def set_label(self, label):
        __label = label
        return self
    
    def get_edges(self):
        if self.is_leaf():
            return []
        edges = [[self.__label, b.get_label()] for b in self.__branches]
        for b in self.__branches:
            edges += b.get_edges()
        return edges
        
    def get_branches(self):
        return self.__branches
    
    def get_label(self):
        return self.__label
    
    def to_list(self):
        return [self.__label, [b.to_list() for b in self.__branches]]
    
    def print_self(self, indent=""):
        print(indent+str(self.__label))
        for b in self.__branches:
            b.print_self(indent=indent+"\t")
        
    