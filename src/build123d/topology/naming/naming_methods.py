from typing import List
from build123d.topology import Shape
import build123d.topology.naming.naming_data as NamingData
import build123d.topology.naming.indexed_name as IndexedName

def losToPyList(listOfShapes):
    returnList = []

    while listOfShapes.Size() > 0:
        returnList.append(listOfShapes.First())
        listOfShapes.RemoveFirst()
    
    return returnList

class ShapeHistoryList:
    def __init__(self, historyType: int):
        self.historyList = {}
        self.reverseHistoryList = {}
        self.historyType = historyType

    def extendList(self, indexedName: IndexedName, OCCTList, parentShape):
        if OCCTList.Size() == 0: return

        self.historyList[indexedName] = []

        for element in losToPyList(OCCTList):
            foundName = parentShape.get_indexed_name_of_child(element)
            foundName.parentIdentifier = parentShape.tag

            if foundName not in self.historyList[indexedName]:
                self.historyList[indexedName].append(foundName)

    def getHistoryOfElement(self, indexedName: IndexedName):
        if indexedName in self.reverseHistoryList:
            return self.reverseHistoryList[indexedName]
    
    def getReverseHistoryOfElement(self, indexedName: IndexedName):
        if indexedName in self.historyList:
            return self.historyList[indexedName]
    
    def updateReverseList(self):
        self.reverseHistoryList = {}

        for sourceIndexedName, destinationNames in self.historyList.items():
            for name in destinationNames:
                if name not in self.reverseHistoryList: self.reverseHistoryList[name] = []

                self.reverseHistoryList[name].append(sourceIndexedName)

# FOR DEVELOPERS: this method might fit better in `../utils.py`?
def mapShapeHistory(mapShape: Shape, sourceShapes: List[Shape], generatedMap: ShapeHistoryList, modifiedMap: ShapeHistoryList):
    pass