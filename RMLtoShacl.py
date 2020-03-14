
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
        self.shaclNS = rdflib.Namespace('http://www.w3.org/ns/shacl#')  #iets doen met bind?
        self.exNM = rdflib.Namespace("http://example.org/")
        self.SHACL = SHACL()
        self.template = self.r2rmlNS.template
        self.reference = self.rmlNS.reference
        self.termType = self.r2rmlNS.termType
    def fillinSubjectMap(self):
        sSM = self.r2rmlNS.subjectMap
        #start of SHACL shape
        for s,p,o in self.RML.graph.triples((sSM,self.template,None)):
            for stm,ptm,otm in self.RML.graph.triples((None,None,self.r2rmlNS.TriplesMap)):
                self.SHACL.graph.add((stm,ptm,self.shaclNS.NodeShape))
                stringpattern = self.createPattern(o)
                uri = rdflib.URIRef(stringpattern)                                      #I can't use regex for targetNode = problem?
                self.SHACL.graph.add((stm,self.shaclNS.targetNode,uri))
                #can a template in a subject also be a blanknode?
        for s,p,o in self.RML.graph.triples((sSM,self.reference,None)):       #still testing with other example
                for ss,pp,oo in self.RML.graph.triples((sSM,self.termtype,None)):
                    if oo==self.r2rmlNS.IRI:
                        for stm,ptm,otm in self.RML.graph.triples((None,None,self.r2rmlNS.TriplesMap)):
                            self.SHACL.graph.add((stm,ptm,self.shaclNS.NodeShape))
                            self.SHACL.graph.add((stm,self.shaclNS.targetNode,o))
                    elif oo==self.r2rmlNS.BlankNode:
                        findClass(self)
    def findClass(self):
        sSM = self.r2rmlNS.subjectMap
        pclass = rdflib.URIRef("http://www.w3.org/ns/r2rml#class")     #self.r2rmlNS.class not possible because class is a reserved Pyhton keyword
        for s,p,o in self.RML.graph.triples((sSM,pclass,None)):
            for stm,ptm,otm in self.RML.graph.triples((None,None,self.r2rmlNS.TriplesMap)):
                self.SHACL.graph.add((stm,self.shaclNS.targetClass,o))
    def fillinProperty(self):
        sPOM  = self.r2rmlNS.predicateObjectMap
        pPred = self.r2rmlNS.predicate
        for s,p,o in self.RML.graph.triples((sPOM,pPred,None)):
            self.SHACL.graph.add((self.shaclNS.property,self.shaclNS.path,o))
    def findObject(self):
        sOM  = self.r2rmlNS.objectMap
        for s,p,o in self.RML.graph.triples((sOM,None,None)):
            if p == self.template:
                stringpattern= self.createPattern(o)
                self.SHACL.graph.add((self.shaclNS.property,self.shaclNS.pattern,stringpattern))
                for s,p,o in self.RML.graph.triples((sOM,None,None)):
                    if p == self.termType and o== self.r2rmlNS.Literal:
                        self.SHACL.graph.add((self.shaclNS.property,self.shaclNS.nodeKind,self.shaclNS.Literal))
                    else:
                        self.SHACL.graph.add((self.shaclNS.property,self.shaclNS.nodeKind,self.shaclNS.IRI))
        
            elif p == self.reference:
                self.SHACL.graph.add((self.shaclNS.property,self.shaclNS.pattern,o))    #doesn't really fit in pattern
                for s,p,o in self.RML.graph.triples((sOM,None,None)):
                    if p == self.termType and o== self.r2rmlNS.IRI:
                        self.SHACL.graph.add((self.shaclNS.property,self.shaclNS.nodeKind,self.shaclNS.IRI))
                    else:
                        self.SHACL.graph.add((self.shaclNS.property,self.shaclNS.nodeKind,self.shaclNS.Literal))
  
    def createPattern(self,templateString):
        parts = templateString.split('{')
        parts2 = []
        for part in parts:
            if '}' in part:
                parts2 = parts2 + part.split('}')
            else:
                parts2 = parts2 + [part]
        string = ''
        tel = 1
        for part in parts2:
            if tel%2 != 0: 
                string = string + part
            else:
                string = string + '.' #wildcard
            tel += 1
        return string
    def main(self):
        self.fillinSubjectMap()
        self.findClass()
        self.fillinProperty()
        self.findObject()
        self.SHACL.printGraph(1)
        #self.RML.printGraph(1)
        


RtoS = RMLtoSHACL()
RtoS.main()