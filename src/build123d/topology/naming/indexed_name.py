import copy

class IndexedName:
    def __init__(self, elementType = "", indexNumber = 0):
        self.elementType = elementType
        self.indexNumber = indexNumber
        self.parentIdentifier = 0
    
    @staticmethod
    def fromString(indexedNameString):
        returnName = IndexedName()

        if indexedNameString.startswith("Edge"):
            returnName.elementType = "Edge"
            returnName.indexNumber = int(indexedNameString[4:])
        elif indexedNameString.startswith("Vertex"):
            returnName.elementType = "Vertex"
            returnName.indexNumber = int(indexedNameString[6:])
        elif indexedNameString.startswith("Face"):
            returnName.elementType = "Face"
            returnName.indexNumber = int(indexedNameString[4:])
        
        return returnName
    
    def copy(self):
        return copy.deepcopy(self)
    
    def cleaned(self):
        copiedName = self.copy()
        copiedName.parentIdentifier = 0

        return copiedName
    
    def __str__(self) -> str:
        return self.toString()
    
    def __repr__(self) -> str:
        if self.parentIdentifier == 0:
            return self.toString()
        else:
            return f"{self.toString()};{self.parentIdentifier}"

    def __hash__(self) -> int:
        return hash(self.toString())

    def __eq__(self, value) -> bool:
        if isinstance(value, IndexedName):
            return (value.toString() == self.toString() and value.parentIdentifier == self.parentIdentifier)
        elif isinstance(value, str):
            return self.toString() == value
        else:
            return False
    
    def toString(self) -> str:
        return f"{self.elementType}{self.indexNumber}"