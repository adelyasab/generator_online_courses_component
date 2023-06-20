﻿# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from UnitextPython.pullenti.unisharp.Utils import Utils

class DocTableRow:
    
    def __init__(self) -> None:
        self.cells = list()
    
    def __str__(self) -> str:
        res = io.StringIO()
        for c in self.cells: 
            print("{0}  \r\n".format(str(c)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)