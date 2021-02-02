#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:11:12 2020

@author: clement frainay
"""
import igraph as graph
import click
import sys

@click.command()
@click.argument('input', type=click.Path(exists=True, file_okay=True, writable=False, readable=True))
@click.option('--output',  '-o', multiple=False, default=None, type=click.Path(exists=False, writable=True, readable=True), help='Write cypher commands in specified output file.')
@click.option('--nodelabel', '-n', multiple=False, default='Node', help='Label describing the type of entity represented by nodes.', show_default=True)
@click.option('--edgelabel', '-e', multiple=False, default='Edge', help='Label describing the type of relationship represented by edges.', show_default=True)
@click.option('--verbose', '-v', is_flag=True, default=False, help='Enables verbose mode')
def cli(input, output, nodelabel, edgelabel, verbose):
    """Generate cypher commands to import a graph in a GML file into a Neo4J database. If no output file is specified, the cypher commands can be directly piped to cypher-shell in order to populate a Neo4J database"""
    g = graph.read(input, format="gml")
    if verbose : click.echo(g.summary(), err=True)

    if output and output != '-':
        f = open(output, "w")
    else:
        f = sys.stdout
   
    del(g.vs['id']) #remove duplicated index as attribute
    
    #create nodes
    i = 0
    for v in g.vs:
        p = ", ".join(f'{k}: \"{a}\"' for k, a in v.attributes().items())
        l="CREATE (:"+nodelabel+" {id: "+str(v.index)+", " +p+"})"
        f.write(l + ";\n" )
        i+=1
    if verbose : click.echo(str(i)+" nodes created", err=True)
        
    #retrieve sources and targets, then create edges
    j = 0
    for e in g.es:
        v1 = str(e.source)
        v2 = str(e.target)
        p = ", ".join(f'{k}: \"{v}\"' for k, v in e.attributes().items())
        l="MATCH (v1:"+nodelabel+") WHERE v1.id ="+v1+"\n"
        l+="MATCH (v2:"+nodelabel+") WHERE v2.id ="+v2+"\n"
        l+="MERGE (v1) -[:"+edgelabel+" {"+p+"}]-> (v2);\n"
        
        f.write(l + "\n" )
        j+=1
    if verbose : click.echo(str(j)+" edges created", err=True) 
       
    if f is not sys.stdout:
        f.close()
    
    
    if verbose : click.echo('conversion done.', err=True)
    
    
if __name__ == '__main__':
    cli()