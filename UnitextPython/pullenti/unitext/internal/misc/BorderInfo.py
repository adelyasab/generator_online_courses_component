﻿# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


class BorderInfo:
    
    def __init__(self) -> None:
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False
    
    @property
    def is_empty(self) -> bool:
        return (not self.top and not self.bottom and not self.left) and not self.right