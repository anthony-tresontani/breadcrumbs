import re
from collections import deque

class Breadcrumbs(object):
    def __init__(self, nodes):
        self.nodes= nodes

    def create(self):
        def bc(path):
            self.cursor_level = 0
            result = []
            try:
                tokens =  deque(path.strip("/").split("/"))
                token  = tokens.popleft()
                for level, expr, value in self:
                    regexp = re.compile(expr)
                    if regexp.match(token):
                        result.append(value)
                        token = tokens.popleft()
                        self.cursor_level += 1
            except IndexError:
                pass
            return result
        return bc
    
    def __iter__(self):
       for node in self.nodes:
           level = node[0]
           if level != self.cursor_level:
               continue
           yield node

def node(level, expr, string):
   level = len(level.split("-->")) -1
   return level, expr, string

