from typing import List, Union
import build123d.topology.naming.naming_data as NamingData

# Layout for MappedName's sections:
# IterationTag and OpCode do not determine an element's identification, it determines what the match method should look for.
# Those initial two entries tell the design intent algorithm what to look for in a loop name. They're used as a
# `key` of sorts.
# ReferenceIDs;ReferenceNames;IterationTag;OperationCode;Index;ElementType;DuplicateCount;MapperInfo
#      ^     other mapped names    ^           SKT         0      E/V/F           0        anything
# g1:1233:0,g2:1233:1,g3:1233:0   1234

class MappedName:
    def __init__(self, baseString = ""):
        self._baseString = baseString
        self._baseStringHash = hash(self._baseString)
        self._sections = self.toSections()
    
    def __hash__(self) -> int:
        return hash(self.toString())

    def __eq__(self, value) -> bool:
        if isinstance(value, MappedName) or isinstance(value, str):
            return self.equal(value)
        return False
    
    def __str__(self) -> str:
        return self.toString()
    
    def equal(self, otherMappedName) -> bool:
        return str(self) == str(otherMappedName)

    def makeSection(referenceIDs: List[str] = ["_"],
                    referenceNames: List[str] = ["_"],
                    iterationTag: int = 0,
                    operationCode: str = "MKR",
                    index: int = 0,
                    elementType: str = "E",
                    duplicateCount: int = 0,
                    mapperInfo: str = "_"
    ) -> str:
        formattedRefNames = ""

        for i, name in enumerate(referenceNames):
            if i != 0:
                formattedRefNames += ","

            formattedRefNames += MappedName.escapeDeliminators(name, [";", ":", ","])

        return f"{','.join(referenceIDs)};{formattedRefNames};{str(iterationTag)};{operationCode};{str(index)};{elementType};{str(duplicateCount)};{mapperInfo}"
    
    @staticmethod
    def escapeDeliminators(string: str, delims = [";"]) -> str:
        newStr = ""

        for char in string:
            if char in delims:
                newStr += "^"
            
            newStr += char
        
        return newStr

    @staticmethod
    def stringToSections(str, deliminator = "|") -> List[str]:
        sections = []
        sectionString = ""
        escapeNumber = 0
        # escapedChar = ""

        for i, char in enumerate(str):
            lastChar = (i == (len(str) - 1))

            if char == "^":
                escapeNumber += 1

                if escapeNumber == 1:
                    continue
            elif (char == deliminator and escapeNumber == 0) or lastChar:
                if lastChar and char != deliminator:
                    sectionString += char

                sections.append(sectionString)
                sectionString = ""
                continue
            elif escapeNumber > 0:
                # escapedChar = char
                escapeNumber = 0
            
            sectionString += char
        
        return sections
    
    def toSections(self) -> List[str]:
        selfHash = hash(self)

        if (selfHash != self._baseStringHash 
            or (len(self._sections) == 0 
                and NamingData.NAME_SECTION_DELIMINATOR in self._baseString)
        ):
            self._sections = MappedName.stringToSections(self.toString(), NamingData.NAME_SECTION_DELIMINATOR)
            self._baseStringHash = selfHash

        return self._sections
    
    @staticmethod
    def stringGetOpCode(string: str) -> str:
        return MappedName.stringGetSectionData(string, 3, True)

    @staticmethod
    def stringGetElementType(string: str) -> str:
        return MappedName.stringGetSectionData(string, 5)

    @staticmethod
    def stringGetDuplicateCount(string: str) -> str:
        return MappedName.stringGetSectionData(string, 6, True)

    @staticmethod
    def stringGetMapperInfo(string: str) -> str:
        return MappedName.stringGetSectionData(string, 7)

    @staticmethod
    def stringGetTag(string: str) -> str:
        return MappedName.stringGetSectionData(string, 2, True)

    @staticmethod
    def stringGetIndex(string: str) -> str:
        return MappedName.stringGetSectionData(string, 4, True)

    @staticmethod
    def makeName(sections: List[str] = []):
        return MappedName(NamingData.NAME_SECTION_DELIMINATOR.join(sections))
    
    @staticmethod
    def stringSetSectionData(string: str, sectionIndex: int, editString):
        sections = MappedName.stringToSections(string, ";")

        if len(sections) > sectionIndex:
            sections[sectionIndex] = str(editString)

            return ";".join(sections)
        
        return string

    def addSection(self, section: str):
        prefix = ""

        if not self._baseString.endswith(NamingData.NAME_SECTION_DELIMINATOR):
            prefix = NamingData.NAME_SECTION_DELIMINATOR

        self._baseString += f"{prefix}{section}"

    def setSectionData(self, sectionIndex: str, dataIndex: int, newValue: Union[int, str]):
        sections = self.toSections()

        section = MappedName.stringSetSectionData(sections[sectionIndex], dataIndex, newValue)
        sections[sectionIndex] = section

        self._baseString = NamingData.NAME_SECTION_DELIMINATOR.join(sections)

    def setSection(self, newSection: str, index: int):
        sections = self.toSections()
        sections[index] = newSection

        self._baseString = NamingData.NAME_SECTION_DELIMINATOR.join(sections)