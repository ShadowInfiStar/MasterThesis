import rdflib


print(rdflib.util.guess_format("RML.ttl"))

g = rdflib.Graph()
g.parse("RML.ttl", format="turtle")

len(g) # prints 2

import pprint
for stmt in g:
    pprint.pprint(stmt)
