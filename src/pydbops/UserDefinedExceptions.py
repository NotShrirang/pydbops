class InvalidReturnTypeError(Exception):
    """
    Class for user defined exception.
    """
    def __init__(self, ReturnType, function) -> None:
        self.__returnType = ReturnType
        self.__function = function

    def __str__(self) -> str:
        if self.__function == "getFieldNames":
            self.__returnTypeList = ["list", "int"]
            return (f"\treturnType cannot be '{self.__returnType}'\nDid you mean {self.__returnTypeList}?")
        elif self.__function == "searchEntry":
            self.__returnTypeList = ["values", "ids"]
            return (f"\treturnType cannot be '{self.__returnType}'\nDid you mean any of {self.__returnTypeList} ?")
        elif self.__function == "tableNames":
            self.__returnTypeList == ["int", "list", "dict"]
            return (f"\trReturn type cannot be two or more.\nDid you mean any one of {self.__returnTypeList} ?")
