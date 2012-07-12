from collections import deque

class Breadcrumbs(object):
    def __init__(self, nodes):
        self.nodes= nodes

    def create(self):
        def bc(path):
            result = []
            try:
                nodes = deque(self.nodes[:])
                tokens =  deque(path.strip("/").split("/"))

                token, node  = tokens.popleft(), nodes.popleft()
                cursor_level = 0
                while True:
                    print node, token, cursor_level
                    level, expr, string = node   
                    if cursor_level != level:
                        break

                    if expr in token:
                        result.append(string)
                        token = tokens.popleft()
                        cursor_level += 1 
                    node = nodes.popleft()
                    level_before = level
            except IndexError:
                pass
            return result
        return bc
    
def node(level, expr, string):
   level = len(level.split("-->")) -1
   return level, expr, string

