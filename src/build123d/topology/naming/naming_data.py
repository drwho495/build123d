from enum import Enum
from .indexed_name import IndexedName
from .mapped_name import MappedName
import build123d.topology.naming.naming_methods as NamingMethods
from build123d.topology import Shape

NAME_SECTION_DELIMINATOR    = "|"
SECTION_DATA_DELIMINATOR    = ";"
SUBSECTION_DATA_DELIMINATOR = ":"
DATA_LIST_DELIMINATOR       = ","

class OpCode(Enum):
    EXTRUSION = "EXT"
    DRESSUP = "DRE"
    SKETCH = "SKT"
    REFINE = "RFI"
    BOOLEAN = "BOL"
    THICKNESS = "THK"
    COMPOUND = "CMP"

class ShapeHistoryList:
    def __init__(self, historyType: int):
        self.historyList = {}
        self.reverseHistoryList = {}
        self.historyType = historyType

    def extendList(self, indexedName: IndexedName, OCCTList, parentShape: Shape):
        if OCCTList.Size() == 0: return

        self.historyList[indexedName] = []

        for element in NamingMethods.occtLOStoList(OCCTList):
            foundName = parentShape.getIndexedNameOfShape(element)
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