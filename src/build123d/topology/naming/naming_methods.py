from typing import List, Union
from build123d.topology import Shape
import build123d.topology.naming.naming_data as NamingData

def losToPyList(listOfShapes):
    returnList = []

    while listOfShapes.Size() > 0:
        returnList.append(listOfShapes.First())
        listOfShapes.RemoveFirst()
    
    return returnList

# FOR DEVELOPERS: this method might fit better in `../utils.py`?
def mapShapeHistory(mapShape: Shape, sourceShapes: List[Shape], generatedMap: NamingData.ShapeHistoryList, modifiedMap: NamingData.ShapeHistoryList):
    pass