
import rdflib
from RML import *
from SHACL import *
class RMLtoSHACL:
    def __init__(self):
        self.RML = RML()
        self.RML.createGraph()
        self.RML.removeBlankNodes()
        self.rmlNS = rdflib.Namespace('http://semweb.mmlab.be/ns/rml#')
        self.r2rmlNS = rdflib.Namespace('http://www.w3.org/ns/r2rml#')
        self.shaclNS = rdflib.Namespace('http://www.w3.org/ns/shacl#')
        self.exNM = rdflib.Namespace("http://example.org/")
        self.SHACL = SHACL()
    def namespace(self):
        sSM = self.r2rmlNS.subjectMap
        ptem = self.r2rmlNS.template
        pref = self.rmlNS.reference
        ptermtype = self.r2rmlNS.termType
        #start of SHACL shape
        for s,p,o in self.RML.graph.triples((sSM,ptem,None)):
            for stm,ptm,otm in self.RML.graph.triples((None,None,self.r2rmlNS.TriplesMap)):
                self.SHACL.graph.add((stm,ptm,self.shaclNS.NodeShape))
                uri = rdflib.URIRef(o)
                self.SHACL.graph.add((stm,self.shaclNS.targetNode,uri))
                #can a template in a subject also be a blanknode?
        for s,p,o in self.RML.graph.triples((sSM,pref,None)):       #still testing with other example
                for ss,pp,oo in self.RML.graph.triples((sSM,ptermtype,None)):
                    if oo==self.r2rmlNS.IRI:
                        for stm,ptm,otm in self.RML.graph.triples((None,None,self.r2rmlNS.TriplesMap)):
                            self.SHACL.graph.add((stm,ptm,self.shaclNS.NodeShape))
                            self.SHACL.graph.add((stm,self.shaclNS.targetNode,o))
                    elif oo==self.r2rmlNS.BlankNode:
                        findClass(self)
    def findClass(self):
        pass


    def main(self):
        self.namespace()
        self.SHACL.printGraph(1)


RtoS = RMLtoSHACL()
RtoS.main()