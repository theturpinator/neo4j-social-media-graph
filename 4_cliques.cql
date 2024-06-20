MATCH (a)-[:FRIENDS_WITH]-(b),
      (a)-[:FRIENDS_WITH]-(c),
      (a)-[:FRIENDS_WITH]-(d),
      (b)-[:FRIENDS_WITH]-(c),
      (b)-[:FRIENDS_WITH]-(d),
      (c)-[:FRIENDS_WITH]-(d)
WHERE id(a) < id(b) AND id(b) < id(c) AND id(c) < id(d)
WITH collect([a, b, c, d]) AS cliques
UNWIND cliques AS clique
RETURN clique
