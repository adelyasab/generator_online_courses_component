﻿# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class UseZip64(IntEnum):
    # Determines how entries are tested to see if they should use Zip64 extensions or not.
    OFF = 0
    ON = 1
    DYNAMIC = 2
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)