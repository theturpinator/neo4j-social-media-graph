MATCH (a)-[:FRIENDS_WITH]-(b),
      (a)-[:FRIENDS_WITH]-(c),
      (a)-[:FRIENDS_WITH]-(d),
      (a)-[:FRIENDS_WITH]-(e),
      (b)-[:FRIENDS_WITH]-(c),
      (b)-[:FRIENDS_WITH]-(d),
      (b)-[:FRIENDS_WITH]-(e),
      (c)-[:FRIENDS_WITH]-(d),
      (c)-[:FRIENDS_WITH]-(e),
      (d)-[:FRIENDS_WITH]-(e)
WHERE id(a) < id(b) AND id(b) < id(c) AND id(c) < id(d) AND id(d) < id(e)
WITH collect([a, b, c, d, e]) AS cliques
UNWIND cliques AS clique
RETURN clique
