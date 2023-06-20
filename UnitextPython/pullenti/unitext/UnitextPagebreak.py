# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import xml.etree
from UnitextPython.pullenti.unisharp.Utils import Utils
from UnitextPython.pullenti.unisharp.Xml import XmlWriter

from UnitextPython.pullenti.unitext.UnitextItem import UnitextItem
from UnitextPython.pullenti.unitext.UnitextContainerType import UnitextContainerType
from UnitextPython.pullenti.unitext.UnitextContainer import UnitextContainer
from UnitextPython.pullenti.unitext.UnitextDocblock import UnitextDocblock
from UnitextPython.pullenti.unitext.WhitespaceType import WhitespaceType

class UnitextPagebreak(UnitextItem):
    """ Разрыв страниц """
    
    def __init__(self) -> None:
        super().__init__()
        self.typ = WhitespaceType.ORIGINAL
        self.page_number = 0
    
    def __str__(self) -> str:
        res = "PageBreak"
        if (self.page_number > 0): 
            res = "PageBreak N={0}".format(self.page_number)
        if (self.typ == WhitespaceType.IGNORABLE): 
            res += " - ignore"
        elif (self.typ == WhitespaceType.ONESPACE): 
            res += " - space"
        return res
    
    def clone(self) -> 'UnitextItem':
        res = UnitextPagebreak()
        res._clone_from(self)
        res.typ = self.typ
        res.page_number = self.page_number
        return res
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam') -> None:
        if (pars is not None and pars.set_positions): 
            self.begin_char = res.tell()
        if (self.typ == WhitespaceType.IGNORABLE): 
            pass
        elif (self.typ == WhitespaceType.ONESPACE): 
            print(' ', end="", file=res)
        else: 
            print(Utils.ifNotNull((Utils.ifNotNull(pars, UnitextItem._m_def_params)).new_line, ""), end="", file=res)
            print(Utils.ifNotNull((Utils.ifNotNull(pars, UnitextItem._m_def_params)).page_break, ""), end="", file=res)
        if (pars is not None and pars.set_positions): 
            self.end_char = (res.tell() - 1)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam') -> None:
        if (self.typ == WhitespaceType.IGNORABLE): 
            return
        if (self.typ == WhitespaceType.ONESPACE): 
            print(' ', end="", file=res)
            return
        if (not par.call_before(self, res)): 
            return
        k = 0
        p = self.parent
        while p is not None and (k < 10): 
            cnt = Utils.asObjectOrNull(p, UnitextContainer)
            if (cnt is not None): 
                if (cnt.typ != UnitextContainerType.UNDEFINED and cnt.typ != UnitextContainerType.HEAD): 
                    print("\r\n<BR/>", end="", file=res)
                    par.call_after(self, res)
                    return
            db = Utils.asObjectOrNull(p, UnitextDocblock)
            if (db is not None): 
                if (Utils.compareStrings(Utils.ifNotNull(db.typname, ""), "Document", True) == 0 or Utils.compareStrings(Utils.ifNotNull(db.typname, ""), "Subdocument", True) == 0 or Utils.compareStrings(Utils.ifNotNull(db.typname, ""), "Appendix", True) == 0): 
                    pass
                elif (db.typname is not None): 
                    print("\r\n<BR/>", end="", file=res)
                    par.call_after(self, res)
                    return
            p = p.parent; k += 1
        if (par is not None): 
            par._out_footnotes(res)
        print("\r\n<HR", end="", file=res)
        if (self.page_number > 0): 
            print(" title=\"End of page {0}\"".format(self.page_number), end="", file=res, flush=True)
        print("/><br/></br>", end="", file=res)
        par.call_after(self, res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        xml0_.write_start_element("pagebreak")
        self._write_xml_attrs(xml0_)
        if (self.typ != WhitespaceType.ORIGINAL): 
            xml0_.write_attribute_string("typ", Utils.enumToString(self.typ).lower())
        if (self.page_number > 0): 
            xml0_.write_attribute_string("pagenum", str(self.page_number))
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        super().from_xml(xml0_)
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "typ"): 
                    try: 
                        self.typ = (Utils.valToEnum(a[1], WhitespaceType))
                    except Exception as ex575: 
                        pass
                elif (Utils.getXmlAttrLocalName(a) == "pagenum"): 
                    self.page_number = int(a[1])
    
    @property
    def is_whitespaces(self) -> bool:
        return True
    
    @property
    def is_inline(self) -> bool:
        if (self.typ != WhitespaceType.ORIGINAL): 
            return True
        return False
    
    def _set_default_text_pos(self, cp : int, res : io.StringIO) -> None:
        self.end_char = cp.value
        self.begin_char = self.end_char
        cp.value += 1
        if (res is not None): 
            print('\f', end="", file=res)
    
    @staticmethod
    def _new333(_arg1 : str, _arg2 : int) -> 'UnitextPagebreak':
        res = UnitextPagebreak()
        res.page_section_id = _arg1
        res.page_number = _arg2
        return res
    
    @staticmethod
    def _new351(_arg1 : str) -> 'UnitextPagebreak':
        res = UnitextPagebreak()
        res.page_section_id = _arg1
        return res
    
    @staticmethod
    def _new378(_arg1 : 'UnitextItem') -> 'UnitextPagebreak':
        res = UnitextPagebreak()
        res.parent = _arg1
        return res