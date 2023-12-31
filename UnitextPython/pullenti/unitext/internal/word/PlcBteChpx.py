﻿# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import math

class PlcBteChpx:
    
    def __init__(self) -> None:
        self._afc = None;
        self._apn_bte_chpx = None;
    
    @staticmethod
    def _get_length(size : int) -> int:
        return (math.floor((((size) - 4)) / ((4 + 4))))