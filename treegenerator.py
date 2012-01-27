#features dict

maindic = {"php5":{"months":12,"parent":"php"},
        "php4":{"months":4,"parent":"php"},
        "python3":{"months":12,"parent":"python"},
        "python2":{"months":40,"parent":"python"},
        "ruby":{"months":6,"parent":"dynamic"},
        "c++":{"months":40,"parent":"lang"},
        "c":{"months":10,"parent":"lang"},
        "ada":{"months":8,"parent":"lang"},
        "fortran":{"months":4,"parent":"lang"},
        "lisp":{"months":4,"parent":"functional"},
        "haskell":{"months":1,"parent":"functional"},
        "java":{"months":1,"parent":"lang"},
        "perl":{"months":1,"parent":"lang"},
        "bash":{"months":4,"parent":"lang"},
        "R":{"months":3,"parent":"lang"},
        "django":{"months":6,"parent":"web"},
        "html":{"months":6,"parent":"web"},
        "css":{"months":2,"parent":"web"},
        "javascript":{"months":1,"parent":"web"},
        "jquery":{"months":1,"parent":"web"},
        "git":{"months":12,"parent":"VC"},
        "mercurial":{"months":12,"parent":"VC"},
        "cvs":{"months":2,"parent":"VC"},
        "svn":{"months":6,"parent":"VC"},
        "debian":{"months":30,"parent":"linux"},
        "gentoo":{"months":30,"parent":"linux"},
        "arch":{"months":12,"parent":"linux"},
        "ubuntu":{"months":4,"parent":"linux"},
        "suse":{"months":1,"parent":"linux"},
        "centos":{"months":1,"parent":"linux"},
        "HTK":{"months":3,"parent":"speech"},
        "MMIIndexer":{"months":2,"parent":"speech"},
        "Nuance dragon":{"months":2,"parent":"speech"},
        "sphinx4":{"months":2,"parent":"sphinx"},
        "sphinx3":{"months":8,"parent":"sphinx"},
        "nltk":{"months":8,"parent":"NLP"},
        "mysql":{"months":12,"parent":"db"},
        "postgresql":{"months":2,"parent":"db"},
        "access":{"months":2,"parent":"db"},
        "QT":{"months":24,"parent":"GUI"},
        "GTK":{"months":2,"parent":"GUI"},
        "builder":{"months":2,"parent":"GUI"},
        "dynamic":{"parent":"lang"},
        "functional":{"parent":"lang"},
        "php":{"parent":"lang"},
        "python":{"parent":"dynamic"},
        "lang":{"parent":"development"},
        "VC":{"parent":"development"},
        "web":{"parent":"development"},
        "GUI":{"parent":"development"},
        "development":{"parent":"root"},
        "nagios":{"months":3,"parent":"sysadmin"},
        "linux":{"parent":"sysadmin"},
        "sysadmin":{"parent":"root"},
        "db":{"parent":"root"},
        "sphinx":{"parent":"speech"},
        "speech":{"parent":"NLP"},
        "NLP":{"parent":"root"},
        "root":{},
        }


def annotate_size(key):
    value = maindic[key]
    if "size" in value or "months" in value:
        return
    value["size"] = 0
    childlist = [x for x in maindic if x != "root" and maindic[x]["parent"] == key]
    for x in childlist:
        annotate_size(x)
        childvalue = maindic[x]
        if "months" in childvalue:
            value["size"] += childvalue["months"]
        elif "size" in childvalue:
            value["size"] += childvalue["size"]
        else:
            raise Exception

annotate_size("root")
import pydot

graph = pydot.Dot(graph_type='graph', rankdir='BT', layout='twopi', ranksep='1.3')
for key,value in maindic.items():
    print(key)
    size = 0
    style = "solid"
    shape = "ellipse"
    if "months" in value:
        size = value["months"]
    else:
        size = value["size"]

    if size < 6:
        size = 6
        style = "dotted"
    if size > 18:
        if size > 36:
            shape = "rect"
        if size > 24:
            style = "bold"
        size = 18

    node = pydot.Node(key, shape=shape, style=style, fontsize=str(size))
    value["node"] = node
    graph.add_node(node)


for key, value in maindic.items():
    thisnode = value["node"]
    if not "parent" in value:
        continue
    if not value["parent"] in maindic:
        othernode = value["parent"]
    else:
        othernode = maindic[value["parent"]]["node"]
    edge = pydot.Edge(othernode, thisnode)
    graph.add_edge(edge)

graph.write_png('example1_graph.png')
