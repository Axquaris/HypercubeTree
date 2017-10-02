from simpletree import Tree
margin = 30

def setup():
    size(800, 800)
    colorMode(HSB)
    global d, n
    d, n = 0, 3
    update_tree(d, n)

def draw():
    pass
    
def mousePressed():
    global d, n
    d += 1
    d %= 3
    update_tree(d, n)
    
def keyPressed():
    global d, n
    try:
        n = int(key)
        if 0 < n <= 9:
            update_tree(d, n)
    except: pass
    
def update_tree(d, n):
    t = build_hypertree(n)
    background(200)
    eval("draw_tree_"+str(d+1)+"(t)")
    
    
def build_hypercube(n):
    """
    Takes number of dmensions of hypercube as n
    Returns the n-D hypercube's vertices and edges

    ALGORITHM:
      take n-1 D hypercube, duplicate at 0 and 1 on new axis, then connect both instances (via edges traversing nth dimension)
      tip - "n"th dimension is at index 0 of vertices
    """
    assert(n > 0)
    zero, one = [0], [1]
    
    if n == 1: # base case = 1D Hypercube
        return [zero, one], [[zero, one]]
    vertices, edges = build_hypercube(n-1) # build n-1 hypercube
    
    edges = [[[p+v for v in e] for e in edges] for p in [zero, one]] # compute all edges in n cube that are parelell to edges in n-1 cube
    edges = edges[0] + edges[1] # add together sets of edges with leading zeros and ones
    edges += [[p+v for p in [zero, one]] for v in vertices] # compute all edges in n cube that are perpendicular to edges in n-1 cube
    
    vertices = [[p+v for v in vertices] for p in [zero, one]]
    vertices = vertices[0] + vertices[1] # add together sets of vertices with leading zeros and ones
    return vertices, edges
    
def build_hypertree(n):
    """
    Takes number of dimensions of hypertree as n
    A hypertree contains all the edges that a hypercube has, with the root being the hypercube's origin
      no edges are repeated, however vertices may be repeated
    ALGORITHM:
      Two-part tree recursion; first build a tree with redundant vertices, then cut away redundant edges (subtrees)
      Both parts are based on patterns I noticed while crunching trees for (1 through 4) dimensional hypercubes
    """
    assert(n > 0)
    zero, one = [0], [1]
    
    def builder(d):
        if d == 1: # base case 
            return Tree(zero, [Tree(one)]) 
        tree = Tree([zero[0] for i in range(d)] ) # build tree with vertex = origin
        branches = [apply_to_tree(builder(d-1), lambda x: one+x)] # creates one sub-tree
        for i in range(d-1):
            branches += [apply_to_tree(branches[i], wrap)] # takes original subtree and duplicates it d-1 times, 
        return tree.set_branches(branches)                 #   rotating the subtree around line thru origin and apex each time
    
    def pruner(tree, deg=n):
        if deg < 0: # cut tree
            return []
        if deg == n: # handles first layer
            branches = []
            for b in tree.get_branches():
                branches += pruner(b, deg-1)
            return tree.set_branches(branches)
        branches = []
        for i, b in enumerate(tree.get_branches()):
            branches += pruner(b, deg-1-i) # deg is reduced by going down in tree or to the right
        return [tree.set_branches(branches)]
    return pruner(builder(n)) # build tree with redundant vertices, then prune to remove duplicate edges

def apply_to_tree(tree, op):
    """ Applies given operation to every vertex of tree, and makes a new tree object """
    return Tree(op(tree.get_label()), [apply_to_tree(b, op) for b in tree.get_branches()])

def wrap(v, deg=1):
    return v[-deg:]+v[:-deg]
    
def test_build_hypertree(a=1, b=6):
    assert(a > 0)
    assert(b > a)
    for i in range(a, b): # WORKS FOR UP TO 9 DIMENSIONS!
        v, hypercube_edges = build_hypercube(i)
        hypertree_edges = build_hypertree(i).get_edges()
        isequal = equal_sets(hypercube_edges, hypertree_edges)
        print(i, isequal)
        if not isequal:
            print("hypercube_edges", hypercube_edges)
            print("hypertree_edges", hypertree_edges)
            break

def equal_sets(x, y):
    if len(x) != len(y):
        return False
    for i in x:
        if i not in y:
            return False
    return True

def draw_tree_1(tree, x=400, y=400, t1=0, t2=TAU, line_r=60):
    branches = tree.get_branches()
    b_size = len(branches)
    if b_size:
        spread = .8/b_size
        partitions = [[flerp(t1, t2, i/float(b_size))-spread, flerp(t1, t2, (i+1)/float(b_size))+spread] for i in range(b_size)]
        for i, p in enumerate(partitions): #enum the branches in
            theta = (p[0]+p[1])/2
            x2, y2 = x+line_r*cos(theta), y+line_r*sin(theta)
            line(x, y, x2, y2)
            if branches[i]: draw_tree_1(branches[i], x2, y2, p[0], p[1])
    pushStyle()
    fill(*color_vertex(tree.get_label()))
    ellipse(x, y, 10, 10)
    popStyle()
    
def draw_tree_2(tree, x=400, y=400, t1=0, t2=TAU, line_r=60):
    branches = tree.get_branches()
    b_size = len(branches)
    if b_size:
        partitions = [[flerp(t1, t2, i/float(b_size)), flerp(t1, t2, (i+1)/float(b_size))] for i in range(b_size)]
        for i, p in enumerate(partitions): #enum the branches in
            theta = (p[0]+p[1])/2
            x2, y2 = 400+line_r*cos(theta), 400+line_r*sin(theta)
            line(x, y, x2, y2)
            if branches[i]: draw_tree_2(branches[i], x2, y2, p[0], p[1], line_r+60)
    pushStyle()
    fill(*color_vertex(tree.get_label()))
    ellipse(x, y, 10, 10)
    popStyle()
    
def draw_tree_3(tree, x=400, y=30, t1=30, t2=800-30, line_r=80):
    branches = tree.get_branches()
    b_size = len(branches)
    if b_size:
        partitions = [[flerp(t1, t2, i/float(b_size)), flerp(t1, t2, (i+1)/float(b_size))] for i in range(b_size)]
        for i, p in enumerate(partitions): #enum the branches in
            theta = (p[0]+p[1])/2
            x2, y2 = theta, line_r
            line(x, y, x2, y2)
            if branches[i]: draw_tree_3(branches[i], x2, y2, p[0], p[1], line_r+60)
    pushStyle()
    fill(*color_vertex(tree.get_label()))
    ellipse(x, y, 10, 10)
    popStyle()
    
def flerp(x1, x2, s):
    return x1+((x2-x1)*s)

def color_vertex(v):
    l = len(v)
    sum = 0.0
    for i in v: sum += i
    ### shitty hue picker
    h = 0.0
    inc = 255.0/2
    for i in v:
        h += i*inc
        inc /= 2
    ###
    return h, 255, sum/l*255
    
    
    
    
    