

class Graph:
    def __init__(self, p):
        self.row_main = []
        self.row_sup = []
        self.row_inf = []
        delf.processus = p
    def search_main_path(self):
        work = []
    def search_end(self, task):
        pass

class Path:
    pathes = []
    def __init__(self, steps=[]):
        self.steps = list(steps)
    
    def step(self, ob):
        print "step", ob.label
        if not ob in self.steps:
            self.steps.append(ob)
            if ob.end():
                self.pathes.append(self)
                return
        else:
            return
        
        first = True
        for o in ob.followers():
            if first:
                self.step(o)
                first = False
            else:
                self.clone().step(o)
    def clone(self):
        return Path(self.steps)
    
    @classmethod
    def sort_pathes(cls):
        cls.pathes.sort(key=lambda p: len(p.steps))

class Node:
    def __init__(self, label):
        self.label = label
        self.fo = []
    def followers(self):
        return self.fo
    def end(self):
        return self.label == "end"
    def __unicode__(self): return label

a = Node("a")
b = Node("b")
c = Node("c")
d = Node("d")
e = Node("end")

a.fo = [c]
b.fo = [a]
c.fo = [d]
d.fo = [e,b]

p = Path()
p.step(a)

p.sort_pathes()
