from dotenv import load_dotenv
import os
from neo4j import GraphDatabase

load_dotenv()

AURA_INSTANCENAME = os.environ["AURA_INSTANCENAME"]
NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)

def connect_and_query():
    try:
        with driver.session() as session:
            res = session.run("MATCH (n) RETURN count(n)")
            count = res.single().value()
            print(f"Number of nodes: {count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
        
# connect_and_query()

def create_entities(tx):
    # Create Iron Man node
    tx.run("MERGE (i:Character {name: 'Iron Man'})")
    # Create other nodes
    tx.run("MERGE (p:Person {name: 'Tony Stark'})")
    tx.run("MERGE (s:Superpower {name: 'Versatile Genius'})")
    tx.run("MERGE (b:Place {name: 'Manhattan'})")
    tx.run("MERGE (d:Place {name: 'Upstate'})")
    tx.run("MERGE (p:Place {name: 'New York City'})")
    tx.run("MERGE (l:Place {name: 'Stark Tower'})")
    tx.run("MERGE (m:Person {name: 'Pepper Potts'})")
    tx.run("MERGE (o:Organization {name: 'Stark Industries'})")
    tx.run("MERGE (a:Organization {name: 'Avengers'})")
    
def create_relationships(tx):
    # Create is alter ego of relationship
    tx.run(
        """    MATCH (i:Character {name: 'Iron Man'}), (p:Person {name: 'Tony Stark'})
        MERGE (i)-[:IDENTIFIED_AS]->(p)
    """
    )
    # Create has superpower relationship
    tx.run(
        """    MATCH (i:Character {name: 'Iron Man'}), (s:Superpower {name: 'Versatile Genius'})
    MERGE (i)-[:HAS_SUPERPOWER]->(s)
    """    )
    # Create lives in relationship
    tx.run(
        """    MATCH (p:Person {name: 'Tony Stark'}), (b:Place {name: 'Manhattan'})
    MERGE (p)-[:BORN_IN]->(b)
    """    )
    tx.run(
        """    MATCH (p:Person {name: 'Tony Stark'}), (d:Place {name: 'Upstate'})
    MERGE (p)-[:DIED_IN]->(d)
    """    )
    tx.run(
        """    MATCH (p:Person {name: 'Tony Stark'}), (l:Place {name: 'Stark Tower'})
    MERGE (p)-[:LIVES_IN]->(l)
    """    )
    # Create has relationship    
    tx.run(
        """    MATCH (p:Person {name: 'Tony Stark'}), (m:Person {name: 'Pepper Potts'})
    MERGE (p)-[:MARRIED_TO]->(m)
    """    )
    # Create works for relationship
    tx.run(
        """    MATCH (p:Person {name: 'Tony Stark'}), (o:Organization {name: 'Stark Industries'})
    MERGE (p)-[:FOUNDER_OF]->(o)
    """    )
    tx.run(
        """    MATCH (p:Person {name: 'Tony Stark'}), (a:Organization {name: 'Avengers'})
    MERGE (p)-[:MEMBER_OF]->(a)
    """    )
    # Create place manhattan located and upstate in new york city relationship
    tx.run(
        """    MATCH (b:Place {name: 'Manhattan'}), (p:Place {name: 'New York City'})
    MERGE (b)-[:LOCATED_IN]->(p)
    """    )
    tx.run(
        """    MATCH (d:Place {name: 'Upstate'}), (p:Place {name: 'New York City'})
    MERGE (d)-[:LOCATED_IN]->(p)
    """    )
    
def query_graph_simple(cypher_query):
    driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
    try:
        with driver.session() as session:
            res = session.run(cypher_query)
            print("query_graph_simple result:")
            for rec in res:
                print(rec["name"])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

# Function to connect and run a Cypher query
def query_graph(cypher_query):
    driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
    try:
        with driver.session() as session: #database=NEO4J_DATABASE
            result = session.run(cypher_query)
            print("query_graph result:")
            for record in result:
                print(record["path"])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

def build_knowledge_graph():
    # Open a session with the Neo4j database

    try:
        with driver.session() as session: #database=NEO4J_DATABASE
            # Create entities
            session.execute_write(create_entities)
            # Create relationships
            session.execute_write(create_relationships)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
        
if __name__ == "__main__":
    build_knowledge_graph()
    
# # Run this to see the entire graph in the neo4j browser/console
# # MATCH (n)-[r]->(m) RETURN n, r, m;
    


