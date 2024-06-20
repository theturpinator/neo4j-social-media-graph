CALL gds.graph.project(
  'test',
  'USER', 
  'FRIENDS_WITH'   
)
;

CALL gds.wcc.stream('test')
YIELD componentId
RETURN COUNT(DISTINCT componentId) AS numberOfConnectedComponents
;