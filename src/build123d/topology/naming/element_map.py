from .mapped_name import MappedName
from .indexed_name import IndexedName
from typing import Union, List
from anytree import NodeMixin
import copy

class ElementMap:
    def __init__(self):
        self._map = {}
    
    def hasIndexedName(self, indexedName: IndexedName) -> bool:
        return indexedName.cleaned() in self._map.values()
    
    def setElement(self, indexedName: IndexedName, mappedName: MappedName, overwrite: bool = False) -> None:
        if not overwrite and self.hasIndexedName(indexedName):
            self._map.pop(self.getMappedName())
        
        self._map[mappedName] = indexedName.cleaned()
    
    def getMappedNames(self, indexedName: IndexedName) -> List[MappedName]:
        names = []
        cleanedName = indexedName.cleaned()

        for mappedName, loopIndexName in self._map.items():
            if loopIndexName.cleaned() == cleanedName:
                names.append(mappedName)

        return names

    def getMappedName(self, indexedName: IndexedName) -> Union[MappedName, None]:
        names = self.getMappedNames(indexedName)

        if len(names) == 0:
            return None

        return names[0]
    
    def getIndexedName(self, mappedName: MappedName) -> Union[MappedName, None]:
        if mappedName not in self._map:
            return None
        
        return self._map[mappedName]
    
    def __eq__(self, value):
        if isinstance(value, ElementMap):
            return value._map == self._map
    
    def copy(self):
        return copy.deepcopy(self)
    
    def getInternalMap(self) -> dict:
        """
            this returns a copy of the internal dictionary of this `ElementMap`
        """
        return self._map.copy()