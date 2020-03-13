import rdflib

def printGraph(g):
    for stmt in g:
        print(stmt)

#print(rdflib.util.guess_format("RML.ttl"))

g = rdflib.Graph()
#g.parse("RML.ttl", format="turtle")
g.parse("C:\\Users\\Birte\\Documents\\GitHub\\rml-test-cases\\test-cases\\RMLTC0000-CSV\\mapping.ttl", format="turtle")


len(g) # prints 2

#import pprint
#for stmt in g:
#    pprint.pprint(stmt)

#for stmt in g:
#    print(stmt)

for s,p,o in g:
    for s2,p2,o2 in g:
        if o == s2:
            g.add((p,p2,o2))
            g.remove((s2,p2,o2))
            g.remove((s,p,o))
#wat als we meerdere triplemaps hebben?? testen op eerste subject en daaruit naam triples map halen

#from rdflib import Namespace
rml = rdflib.Namespace('http://semweb.mmlab.be/ns/rml#')
r2rml = rdflib.Namespace('http://www.w3.org/ns/r2rml#')
n = rdflib.Namespace("http://example.org/")
s = r2rml.subjectMap

for s,p,o in g.triples((s,None,None)):
    print(s,p,o)



