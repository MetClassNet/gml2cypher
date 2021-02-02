# gml2cypher

  Generate cypher commands to import a graph in a GML file into a Neo4J
  database. If no output file is specified, the cypher commands can be
  directly piped to cypher-shell in order to populate a Neo4J database

## Usage: 
  ```
  gml2cypher.py [OPTIONS] INPUT
  ```

## Options:
  **-o**, **--output** PATH     Write cypher commands in specified output file.  
  **-n**, **--nodelabel** TEXT  Label describing the type of entity represented by
                        nodes.  [default: Node]  

  **-e**, **--edgelabel** TEXT  Label describing the type of relationship represented
                        by edges.  [default: Edge]  

  **-v**, **--verbose**         Enables verbose mode  
  **--help**                Show this message and exit.  

## Notes:
Directly run generated cypher commands using:
```
gml2cypher.py -n 'MyNodeLabel' -e 'MyEdgeLabel' myGraphFile.gml | cypher-shell -u [user] -p [password]
```
