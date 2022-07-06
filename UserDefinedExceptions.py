class InvalidReturnTypeError(Exception):
    def __init__(self, ReturnType):
        self.__returnType = ReturnType
        self.__returnTypeList = ["values", "ids"]
    def __str__(self) -> str:
        return (f"\treturnType cannot be '{self.__returnType}'\nDid you mean any of {self.__returnTypeList} ?")
    
