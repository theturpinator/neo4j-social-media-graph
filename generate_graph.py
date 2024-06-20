import random
from neo4j import GraphDatabase, basic_auth
from faker import Faker
import uuid
import numpy as np

fake = Faker()

COMMUNITY_SIZES = [50, 100, 150]
RELATIONSHIPS = [100, 200, 300]

uri = 'bolt://localhost:7687'
user = 'neo4j'
password = '<enter password here>'

driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

with driver.session() as session:
        
    #delete existing nodes and relationships
    session.run("MATCH (n) detach delete n")


for i in range(len(COMMUNITY_SIZES)):

    NUM_USERS = COMMUNITY_SIZES[i]
    NUM_RELATIONSHIPS = RELATIONSHIPS[i]

    users = [
        {
            "id": str(uuid.uuid4()),
            "first_name": fake.first_name(), 
            "last_name": fake.last_name(), 
            "age": random.randint(18, 99)
        } 
        for x in range(NUM_USERS)
    ]

    #generate probability distribution for sampling users (used to generate relationships)
    vals = abs(np.random.lognormal(size=NUM_USERS))
    probs = vals/np.sum(vals)

    #create user attribute dictionaries for neo4j ddl
    user_data = [f'id: "{user["id"]}", first_name: "{user["first_name"]}", last_name: "{user["last_name"]}", age: {user["age"]}' for user in users]

    # TODO: generate user->user relationships
    friendship = [(np.random.choice(users, p=probs)["id"], np.random.choice(users, p=probs)["id"]) for _ in range(NUM_RELATIONSHIPS)]
    friendship = list(filter(lambda x: x[0] != x[1], friendship)) # filter out self-relationships

    # becuase relationships are inherently bi-directional, filter out relationships where b -> a if a -> b already exists
    relationships = set()
    for (x, y) in friendship:
        if (y, x) not in relationships:
            relationships.add((x, y))


    # create user node DDL
    user_node_ddl = [f"CREATE (:USER {{{str(user_attrs)}}})"for user_attrs in user_data]

    # create relationship DDL
    relationship_ddl = [f'MATCH (a:USER {{id: "{r[0]}"}}), (b:USER {{id: "{r[1]}"}}) CREATE (a)-[:FRIENDS_WITH]->(b)' for r in relationships]


    with driver.session() as session:

        #create nodes
        for stmt in user_node_ddl:
            session.run(stmt)
        
        #create relationships
        for stmt in relationship_ddl:
            session.run(stmt)

driver.close()