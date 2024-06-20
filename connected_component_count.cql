MATCH (n)
WITH n, id(n) AS nodeId
MATCH p = (n)-[*0..]-(m) //match all nodes with 0 or more relationships
WITH n, collect(distinct id(m)) AS connected_component_ids //aggregate all related nodes into an array 
WITH n, REDUCE(maxID = -1, x IN connected_component_ids | CASE WHEN x > maxID THEN x ELSE maxID END) AS maxID //get the maximum ID in each CC as a representative
RETURN COUNT(DISTINCT maxID) as connected_component_count //return distinct count of CCs