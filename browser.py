
from neo4j import GraphDatabase

# Connect to your Neo4j database
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Run a Cypher query
with driver.session() as session:
    result = session.run("MATCH (n) RETURN n LIMIT 25")

    for record in result:
        print(record["n"])

# Close the driver
driver.close()
