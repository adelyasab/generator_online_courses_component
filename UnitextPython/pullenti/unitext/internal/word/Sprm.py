# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from UnitextPython.pullenti.unisharp.Utils import Utils
from UnitextPython.pullenti.unisharp.Misc import RefOutArgWrapper

from UnitextPython.pullenti.unitext.internal.word.SinglePropertyModifiers import SinglePropertyModifiers

class Sprm:
    
    @property
    def _ispmd(self) -> int:
        return ((self._sprm) & 0x1FF)
    
    @property
    def _fspec(self) -> bool:
        return (((self._sprm) & 0x200)) != 0
    
    @property
    def _sgc(self) -> int:
        return ((((self._sprm) >> 10)) & 0x07)
    
    @property
    def _spra(self) -> int:
        return ((((self._sprm) >> 13)) & 0x07)
    
    def __init__(self, sprm : int=0) -> None:
        self._sprm = 0
        self._sprm = sprm
    
    def __str__(self) -> str:
        sprm_name = None
        wrapsprm_name495 = RefOutArgWrapper(None)
        inoutres496 = Utils.tryGetValue(SinglePropertyModifiers._map0_, self._sprm, wrapsprm_name495)
        sprm_name = wrapsprm_name495.value
        if (inoutres496): 
            return sprm_name
        else: 
            return "sprm: 0x" + "{:4X}".format(self._sprm)