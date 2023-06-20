# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import pathlib
import base64
import xml.etree
import typing
from UnitextPython.pullenti.unisharp.Utils import Utils
from UnitextPython.pullenti.unisharp.Misc import RefOutArgWrapper
from UnitextPython.pullenti.unisharp.Xml import XmlWriter
from UnitextPython.pullenti.unisharp.Xml import XmlWriterSettings

from UnitextPython.pullenti.unitext.FileFormatClass import FileFormatClass
from UnitextPython.pullenti.util.MiscHelper import MiscHelper
from UnitextPython.pullenti.util.FileFormatsHelper import FileFormatsHelper
from UnitextPython.pullenti.unitext.CorrectDocumentParam import CorrectDocumentParam
from UnitextPython.pullenti.unitext.CreateDocumentParam import CreateDocumentParam
from UnitextPython.pullenti.unitext.UnitextContainerType import UnitextContainerType
from UnitextPython.pullenti.unitext.UnitextContainer import UnitextContainer
from UnitextPython.pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from UnitextPython.pullenti.unitext.GetPlaintextParam import GetPlaintextParam
from UnitextPython.pullenti.unitext.UnitextItem import UnitextItem
from UnitextPython.pullenti.unitext.FileFormat import FileFormat
from UnitextPython.pullenti.unitext.internal.uni.ChangeTextPosInfo import ChangeTextPosInfo
from UnitextPython.pullenti.unitext.UnitextStyledFragment import UnitextStyledFragment
from UnitextPython.pullenti.unitext.UnitextStyle import UnitextStyle
from UnitextPython.pullenti.unitext.GetHtmlParam import GetHtmlParam

class UnitextDocument(UnitextItem):
    """ Unitext - документ
    
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.content = None;
        self.inner_documents = list()
        self.pages = list()
        self.styles = list()
        self.sections = list()
        self.source_format = FileFormat.UNKNOWN
        self.source_file_name = None;
        self.source_file_pages = None;
        self.error_message = None;
        self.attrs = dict()
        self.source_plain_text = None;
        self.default_get_html_param = None;
    
    def __str__(self) -> str:
        res = "{0}{1}{2}".format(Utils.enumToString(self.source_format), ("" if self.source_file_name is None else " :"), Utils.ifNotNull(self.source_file_name, ""))
        if (self.source_file_pages is not None): 
            res = "{0} (стр.{1})".format(res, self.source_file_pages)
        return res
    
    def clone(self) -> 'UnitextItem':
        from UnitextPython.pullenti.unitext.UnitextPagesection import UnitextPagesection
        res = UnitextDocument()
        res._clone_from(self)
        for s in self.styles: 
            res.styles.append(s.clone(False))
        if (self.content is not None): 
            res.content = self.content.clone()
            if (self.content._m_styled_frag is not None): 
                res.content._m_styled_frag = self.content._m_styled_frag.clone()
        for d in self.inner_documents: 
            res.inner_documents.append(Utils.asObjectOrNull(d.clone(), UnitextDocument))
        for s in self.sections: 
            res.sections.append(Utils.asObjectOrNull(s.clone(), UnitextPagesection))
        res.pages = list(self.pages)
        res.source_format = self.source_format
        res.source_file_name = self.source_file_name
        res.source_file_pages = self.source_file_pages
        res.source_info = self.source_info
        res.error_message = self.error_message
        res.source_plain_text = self.source_plain_text
        res.default_get_html_param = self.default_get_html_param
        for a in self.attrs.items(): 
            res.attrs[a[0]] = a[1]
        self.refresh_parents()
        return res
    
    @property
    def is_inline(self) -> bool:
        return False
    
    def get_plaintext(self, res : io.StringIO, pars : 'GetPlaintextParam'=None) -> None:
        """ Сгенерировать плоский текст
        
        Args:
            res(io.StringIO): куда записать
            pars(GetPlaintextParam): параметры генерации
        
        """
        if (self.source_plain_text is not None): 
            print(self.source_plain_text, end="", file=res)
            return
        if (pars is None): 
            pars = GetPlaintextParam._new339(True)
        if (pars.set_positions): 
            self.begin_char = res.tell()
        if (self.content is not None): 
            ii = None
            if (self.content._m_styled_frag is not None): 
                ii = ChangeTextPosInfo(self.content._m_styled_frag, self.content)
            self.content.get_plaintext(res, pars)
            if (ii is not None): 
                ii.restore(res.tell())
        if (len(self.inner_documents) > 0 and pars.use_inner_documents): 
            for d in self.inner_documents: 
                if (res.tell() > 0): 
                    if (pars.new_line is not None): 
                        print(pars.new_line, end="", file=res)
                        print(pars.new_line, end="", file=res)
                    if (pars.page_break is not None): 
                        print(pars.page_break, end="", file=res)
                d.get_plaintext(res, pars)
        if (pars.set_positions): 
            self.end_char = (res.tell() - 1)
            if (len(self.sections) == 1): 
                self.sections[0].end_char = self.end_char
            elif (len(self.sections) > 1 and self.content is not None): 
                its = list()
                self.get_all_items(its, 0)
                i0 = -1
                for it in its: 
                    ps = it.page_section
                    if (ps is None): 
                        continue
                    ii = Utils.indexOfList(self.sections, ps, 0)
                    if (ii < i0): 
                        continue
                    i0 = ii
                    if (it.begin_char > 0 and ps.begin_char == 0): 
                        ps.begin_char = it.begin_char
                    if (it.end_char > ps.end_char): 
                        ps.end_char = it.end_char
                self.sections[0].begin_char = 0
                self.sections[len(self.sections) - 1].end_char = self.end_char
    
    def get_plaintext_string(self, pars : 'GetPlaintextParam'=None) -> str:
        """ Сгенерировать плоский текст
        
        Args:
            pars(GetPlaintextParam): параметры генерации
        
        Returns:
            str: результат
        
        """
        res = io.StringIO()
        self.get_plaintext(res, pars)
        if (res.tell() == 0): 
            return None
        return Utils.toStringStringIO(res)
    
    def get_html(self, res : io.StringIO, par : 'GetHtmlParam'=None) -> None:
        """ Сгенерировать HTML
        
        Args:
            res(io.StringIO): куда записать
            par(GetHtmlParam): параметры генерации
        
        """
        if (par is None): 
            par = self.default_get_html_param
        if (par is None): 
            par = GetHtmlParam()
        if (not par.call_before(self, res)): 
            return
        if (par.out_html_and_body_tags): 
            print("<html><meta charset=\"utf-8\"/>", end="", file=res)
            if (not Utils.isNullOrEmpty(par.title)): 
                print("\r\n<title>", end="", file=res)
                MiscHelper.correct_html_value(res, par.title, False, False, False)
                print("</title>", end="", file=res)
            print("<body>", end="", file=res)
        if (self.id0_ is not None): 
            print("<a name=\"{0}\"> </a>".format(self.id0_), end="", file=res, flush=True)
        if (self.error_message is not None): 
            print("\r\n<div style=\"border:2pt solid red\">".format(), end="", file=res, flush=True)
            MiscHelper.correct_html_value(res, self.error_message, False, False, False)
            print("</div>".format(), end="", file=res, flush=True)
        if (self.content is not None): 
            self.content.get_html(res, par)
            par._out_footnotes(res)
            par._out_endnotes(res)
            if (par is not None and res.tell() > par.max_html_size): 
                print("\r\n<br/><div style=\"color:red\"><b>ВНИМАНИЕ!</b> Размер Html превышает установленные {0} символов, часть информации не попало в Html.</div>".format(par.max_html_size), end="", file=res, flush=True)
        if (par is None or par.use_inner_documents): 
            for d in self.inner_documents: 
                print("\r\n<HR/><H2>Внутренний документ {0}</H1>".format(Utils.ifNotNull(d.source_file_name, "")), end="", file=res, flush=True)
                d.get_html(res, par)
        par.call_after(self, res)
        if (par.out_html_and_body_tags): 
            print("\r\n</body></html>", end="", file=res)
    
    def get_html_string(self, par : 'GetHtmlParam'=None) -> str:
        """ Сгенерировать HTML
        
        Args:
            par(GetHtmlParam): параметры генерации
        
        Returns:
            str: результат
        """
        res = io.StringIO()
        self.get_html(res, par)
        return Utils.toStringStringIO(res)
    
    def get_xml(self, xml0_ : XmlWriter) -> None:
        """ Сериализовать в XML. Потом можно восстановить фукнцией FromXml().
        
        Args:
            xml0_(XmlWriter): куда сериализовать
        
        """
        xml0_.write_start_element("doc")
        if (self.source_format != FileFormat.UNKNOWN): 
            xml0_.write_attribute_string("format", Utils.enumToString(self.source_format).lower())
        if (self.source_file_name is not None): 
            xml0_.write_attribute_string("filename", MiscHelper.correct_xml_value(pathlib.PurePath(self.source_file_name).name))
        if (self.source_file_pages is not None): 
            xml0_.write_attribute_string("filepages", self.source_file_pages)
        if (self.error_message is not None): 
            xml0_.write_attribute_string("error", MiscHelper.correct_xml_value(self.error_message))
        for a in self.attrs.items(): 
            xml0_.write_start_element("attr")
            xml0_.write_attribute_string("name", a[0])
            xml0_.write_attribute_string("val", Utils.ifNotNull(MiscHelper.correct_xml_value(a[1]), ""))
            xml0_.write_end_element()
        if (self.source_plain_text is not None): 
            xml0_.write_element_string("sourcetext", base64.encodestring(MiscHelper.encode_string_utf8(self.source_plain_text, False)).decode('utf-8', 'ignore'))
        if (len(self.styles) > 0): 
            xml0_.write_start_element("styles")
            for s in self.styles: 
                s.get_xml(xml0_)
            xml0_.write_end_element()
        for s in self.sections: 
            s.get_xml(xml0_)
        if (self.content is not None): 
            xml0_.write_start_element("content")
            self.content.get_xml(xml0_)
            xml0_.write_end_element()
            if (self.content._m_styled_frag is not None): 
                self.content._m_styled_frag.get_xml(xml0_, None, False)
        for d in self.inner_documents: 
            d.get_xml(xml0_)
        xml0_.write_end_element()
    
    def from_xml(self, xml0_ : xml.etree.ElementTree.Element) -> None:
        """ Десериализовать из XML, полученный функцией GetXml().
        
        Args:
            xml0_(xml.etree.ElementTree.Element): корневой узел, куда сериализовали
        
        """
        from UnitextPython.pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper
        from UnitextPython.pullenti.unitext.UnitextPagesection import UnitextPagesection
        if (xml0_.attrib is not None): 
            for a in xml0_.attrib.items(): 
                if (Utils.getXmlAttrLocalName(a) == "format"): 
                    try: 
                        self.source_format = (Utils.valToEnum(a[1], FileFormat))
                    except Exception as ex553: 
                        pass
                elif (Utils.getXmlAttrLocalName(a) == "filename"): 
                    self.source_file_name = a[1]
                elif (Utils.getXmlAttrLocalName(a) == "filepages"): 
                    self.source_file_pages = a[1]
                elif (self.error_message is not None): 
                    self.error_message = a[1]
        for x in xml0_: 
            if (Utils.getXmlLocalName(x) == "content"): 
                for xx in x: 
                    self.content = UnitextHelper.create_item(xx)
                    self.content.parent = (self)
                    break
            elif (Utils.getXmlLocalName(x) == "sourcetext"): 
                try: 
                    self.source_plain_text = MiscHelper.decode_string_utf8(base64.decodestring((Utils.getXmlInnerText(x)).encode('utf-8', 'ignore')), 0, -1)
                except Exception as ex: 
                    pass
            elif (Utils.getXmlLocalName(x) == "section"): 
                s = UnitextPagesection()
                s.from_xml(x)
                self.sections.append(s)
            elif (Utils.getXmlLocalName(x) == "doc"): 
                d = UnitextDocument()
                d.from_xml(x)
                self.inner_documents.append(d)
            elif (Utils.getXmlLocalName(x) == "attr" and x.attrib is not None): 
                try: 
                    self.attrs[Utils.getXmlAttrByName(x.attrib, "name")[1]] = Utils.getXmlAttrByName(x.attrib, "val")[1]
                except Exception as ex554: 
                    pass
            elif (Utils.getXmlLocalName(x) == "styles"): 
                self.styles.clear()
                for xx in x: 
                    sty = UnitextStyle()
                    sty.from_xml(xx)
                    self.styles.append(sty)
            elif (Utils.getXmlLocalName(x) == "stylefrag" and self.content is not None): 
                self.content._m_styled_frag = UnitextStyledFragment()
                self.content._m_styled_frag.doc = self
                self.content._m_styled_frag.from_xml(x)
        self.get_all_items(None, 0)
    
    def optimize(self, is_content : bool, pars : 'CreateDocumentParam') -> 'UnitextItem':
        if (self.content is not None): 
            self.content = self.content.optimize(True, pars)
        for s in self.sections: 
            for it in s.items: 
                if (it.content is not None): 
                    it.content = it.content.optimize(True, pars)
        for d in self.inner_documents: 
            d.optimize(False, pars)
        return self
    
    def refresh_parents(self) -> None:
        # Обновить ссылки на родительские элементы
        self.get_all_items(None, 0)
    
    def refresh_content_by_pages(self) -> None:
        """ После OCR-распознавания обновить СТП (Content) на основе нового ТГП (Pages) """
        from UnitextPython.pullenti.unitext.internal.uni.UnitextCorrHelper import UnitextCorrHelper
        from UnitextPython.pullenti.unitext.internal.uni.UnilayoutHelper import UnilayoutHelper
        if (len(self.pages) == 0): 
            return
        UnilayoutHelper.create_content_from_pages(self, True)
        UnitextCorrHelper.remove_false_new_lines(self, True)
        self.refresh_parents()
    
    @property
    def content_items(self) -> typing.List['UnitextItem']:
        """ Получить список всех элементов (включая и сам документ как элемент).
        Порядок последовательный, как они входят в дерево и в какой последовательности генерируется плоский текст.
        Колонтитулы не включаются. """
        res = list()
        self.get_all_items(res, 0)
        return res
    
    def get_all_items(self, res : typing.List['UnitextItem'], lev : int=0) -> None:
        if (res is not None): 
            res.append(self)
        if (self.content is not None): 
            self.content.parent = (self)
            self.content.get_all_items(res, lev + 1)
        for d in self.inner_documents: 
            d.parent = (self)
            d.get_all_items(res, lev + 1)
        tmp = None
        if (res is not None): 
            tmp = list()
        for s in self.sections: 
            s.parent = (self)
            s.get_all_items(tmp, 0)
        if (lev == 0 and res is not None): 
            for it in res: 
                if (it.parent is not None and it.page_section_id is not None): 
                    if (it.page_section == it.parent.page_section): 
                        it.page_section_id = (None)
        if (tmp is not None): 
            for it in tmp: 
                if (it.parent is not None and it.page_section_id is not None): 
                    if (it.page_section == it.page_section.page_section): 
                        it.page_section_id = (None)
    
    def correct(self, corr_pars : 'CorrectDocumentParam') -> bool:
        # Откорректировать документ
        from UnitextPython.pullenti.unitext.internal.uni.UnitextCorrHelper import UnitextCorrHelper
        if (corr_pars is None): 
            corr_pars = CorrectDocumentParam()
        ret = False
        if (corr_pars.restore_tables): 
            if (UnitextCorrHelper.restore_tables(self)): 
                ret = True
        if (corr_pars.remove_page_break_numeration): 
            fty = FileFormatsHelper.get_format_class(self.source_format)
            if (self.source_format == FileFormat.TXT or fty == FileFormatClass.PAGELAYOUT or fty == FileFormatClass.IMAGE): 
                UnitextCorrHelper.remove_page_break_numeration(self)
        if (corr_pars.remove_false_new_lines): 
            UnitextCorrHelper.remove_false_new_lines(self, corr_pars.replace_nbsp_by_space)
        if (corr_pars.restore_text_footnotes): 
            UnitextCorrHelper.restore_text_footnotes(self)
        if (corr_pars.optimize_structure): 
            self.optimize(False, CreateDocumentParam())
        return ret
    
    def get_styled_fragment(self, text_pos : int=-1) -> 'UnitextStyledFragment':
        if (self.content is not None): 
            if (self.content._m_styled_frag is None): 
                return None
            return self.content.get_styled_fragment(text_pos)
        return None
    
    def implantate(self, cnt : 'UnitextContainer', plaintext : str, parent_ : 'UnitextDocblock'=None) -> bool:
        """ Встроить контейнер в дерево элементов.
        ВНИМАНИЕ! Встраивание возможно только после вызова GetPlaintext(),
        когда значения BeginChar и EndChar установлены у всех элементов, и встраивание происходит относительно этих значений.
        Идентификатор у встраиваемого контейнера устанавливать самим, если нужно потом производить к нему навигацию в Html.
        
        Args:
            cnt(UnitextContainer): встраиваемый контейнер (любой наследный от контейнера класс) с установленными значениями BeginChar и EndChar
            plaintext(str): сгенерированный плоский текст, относительно которого идёт позиционирование
            parent_(UnitextDocblock): возможный контейнерный блок (если известен), может быть null
        
        Returns:
            bool: получилось ли встроить
        
        """
        from UnitextPython.pullenti.unitext.internal.uni.UnitextImplantateHelper import UnitextImplantateHelper
        if (self.content is None or cnt is None): 
            return False
        if ((cnt.begin_char < 0) or (cnt.end_char < cnt.begin_char) or cnt.end_char >= len(plaintext)): 
            return False
        if (parent_ is not None): 
            UnitextImplantateHelper.implantate(parent_, cnt, plaintext, None)
            return cnt.parent is not None
        res = UnitextImplantateHelper.implantate(self.content, cnt, plaintext, None)
        if (res is None): 
            return False
        self.content = res
        return cnt.parent is not None
    
    def implantate_hyperlink(self, hl : 'UnitextHyperlink', plaintext : str, parent_ : 'UnitextDocblock'=None) -> bool:
        """ Встроить гиперссылку в дерево элементов.
        ВНИМАНИЕ! Встраивание возможно только после вызова GetPlaintext(),
        когда значения BeginChar и EndChar установлены у всех элементов, и встраивание происходит относительно этих значений.
        Идентификатор у встраиваемого контейнера устанавливать самим, если нужно потом производить к нему навигацию в Html.
        
        Args:
            hl(UnitextHyperlink): встраиваемая гиперссылка с установленными значениями BeginChar и EndChar
            plaintext(str): сгенерированный плоский текст, относительно которого идёт позиционирование
            parent_(UnitextDocblock): возможный контейнерный блок (если известен), может быть null
        
        Returns:
            bool: получилось ли встроить
        """
        if (self.content is None): 
            return False
        cnt = UnitextContainer()
        cnt.begin_char = hl.begin_char
        cnt.end_char = hl.end_char
        if (not self.implantate(cnt, plaintext, parent_)): 
            return False
        if (cnt.parent is None): 
            return False
        if (not cnt.parent._replace_child(cnt, hl)): 
            return False
        hl.content = cnt.optimize(True, None)
        if (hl.content is not None): 
            hl.content.parent = (hl)
        return True
    
    def implantate_block(self, begin_head : int, begin_body : int, begin_tail : int, begin_appendix : int, end : int, plaintext : str, parent_ : 'UnitextDocblock'=None) -> 'UnitextDocblock':
        """ Встроить в дерево структурирующий блок UnitextDocblock.
        Его идентификатор Id нужно устанавливать самим, если нужно.
        
        Args:
            begin_head(int): начальная позиция заголовка блока
            begin_body(int): начальная позиция тела блока
            begin_tail(int): начальная позиция подписи (если = beginBody, то отсутствует)
            begin_appendix(int): начальная позиция приложения (если = end, то отсутствует)
            end(int): конечная позиция
            plaintext(str): сгенерированный плоский текст, относительно которого идёт позиционирование
            parent_(UnitextDocblock): возможный вышележащий блок
        
        Returns:
            UnitextDocblock: в случае успеха вернёт указатель встроенный блок, null - если не получилось
        """
        from UnitextPython.pullenti.unitext.internal.uni.UnitextImplantateHelper import UnitextImplantateHelper
        res = None
        if ((parent_ is not None and parent_.appendix is not None and begin_head >= parent_.appendix.begin_char) and end <= parent_.appendix.end_char): 
            wrapres555 = RefOutArgWrapper(res)
            cnt = UnitextImplantateHelper.implantate_block(parent_.appendix, begin_head, begin_body, begin_tail, begin_appendix, end, plaintext, None, wrapres555)
            res = wrapres555.value
            if (cnt is not None): 
                parent_.appendix = cnt
        elif ((parent_ is not None and parent_.body is not None and begin_head >= parent_.begin_char) and end <= parent_.end_char): 
            wrapres556 = RefOutArgWrapper(res)
            cnt = UnitextImplantateHelper.implantate_block(parent_.body, begin_head, begin_body, begin_tail, begin_appendix, end, plaintext, None, wrapres556)
            res = wrapres556.value
            if (cnt is not None): 
                parent_.body = cnt
        else: 
            wrapres557 = RefOutArgWrapper(res)
            cnt = UnitextImplantateHelper.implantate_block(self.content, begin_head, begin_body, begin_tail, begin_appendix, end, plaintext, None, wrapres557)
            res = wrapres557.value
            if (cnt is not None): 
                self.content = cnt
        return res
    
    def remove_item_by_id(self, id0__ : str) -> bool:
        """ Удалить элемент по его идентификатору Id.
        Сейчас работает только для тех элементов, которые были встроены через Implantate
        
        Args:
            id0__(str): идентификатор удаляемого элемента
        
        Returns:
            bool: удалось ли удалить
        """
        from UnitextPython.pullenti.unitext.internal.uni.UnitextImplantateHelper import UnitextImplantateHelper
        if (self.content is None): 
            return False
        cou = 0
        wrapcou558 = RefOutArgWrapper(cou)
        self.content = UnitextImplantateHelper.clear(self.content, id0__, None, UnitextContainerType.UNDEFINED, None, wrapcou558)
        cou = wrapcou558.value
        return cou > 0
    
    def remove_all_hyperlinks(self, sub_string : str=None) -> int:
        """ Удалить все гиперссылки, сделав их обычными текстами
        
        Args:
            sub_string(str): если задан, то url должен содержать эту подстроку. Подстрок м.б. несколько, разделитель - точка с запятой.
        
        Returns:
            int: количество удалённых гиперссылок
        """
        from UnitextPython.pullenti.unitext.UnitextHyperlink import UnitextHyperlink
        its = list()
        self.get_all_items(its, 0)
        change = 0
        substrs = list()
        if (sub_string is not None): 
            substrs.extend(Utils.splitString(sub_string.upper(), ';', False))
        for it in its: 
            hl = Utils.asObjectOrNull(it, UnitextHyperlink)
            if (hl is None): 
                continue
            if (len(substrs) > 0): 
                if (hl.href is None): 
                    if (not "" in substrs): 
                        continue
                else: 
                    k = 0
                    k = 0
                    while k < len(substrs): 
                        if (not Utils.isNullOrEmpty(substrs[k]) and substrs[k] in hl.href.upper()): 
                            break
                        k += 1
                    if (k >= len(substrs)): 
                        if (((hl.href.find(' ') < 0) and hl.href.find('.') > 0) or hl.is_internal): 
                            continue
            if (hl.parent is not None and hl.content is not None): 
                if (hl.parent._replace_child(hl, hl.content)): 
                    change += 1
        if (change > 0): 
            self.optimize(False, CreateDocumentParam())
        return change
    
    def generate_ids(self) -> None:
        """ Сгенерировать внутренние идентификаторы у элементов.
        Если у элемента Id установлен, то он не меняется.
        У колонтитулов Id не устанавливается. По умолчанию, Id генерируются при создании документа. """
        ids = dict()
        all0_ = list()
        self.get_all_items(all0_, 0)
        for it in all0_: 
            if (it._inner_tag is not None and it.id0_ is not None and it.id0_.startswith(it._inner_tag)): 
                n = 0
                wrapn559 = RefOutArgWrapper(0)
                inoutres560 = Utils.tryParseInt(it.id0_[len(it._inner_tag):], wrapn559)
                n = wrapn559.value
                if (inoutres560): 
                    if (not it._inner_tag in ids): 
                        ids[it._inner_tag] = n
                    elif (ids[it._inner_tag] < n): 
                        ids[it._inner_tag] = n
        for it in all0_: 
            if (it._inner_tag is not None and it != self and it.id0_ is None): 
                id0__ = 0
                wrapid561 = RefOutArgWrapper(0)
                inoutres562 = Utils.tryGetValue(ids, it._inner_tag, wrapid561)
                id0__ = wrapid561.value
                if (not inoutres562): 
                    id0__ = 1
                    ids[it._inner_tag] = id0__
                else: 
                    id0__ += 1
                    ids[it._inner_tag] = id0__
                it.id0_ = "{0}{1}".format(it._inner_tag, id0__)
    
    def merge_with(self, doc : 'UnitextDocument') -> None:
        """ Объединить содержимое с содержимым другого документа
        
        Args:
            doc(UnitextDocument): другой документ
        """
        cnt = Utils.asObjectOrNull(self.content, UnitextContainer)
        cnt2 = Utils.asObjectOrNull(doc.content, UnitextContainer)
        if (cnt is None): 
            cnt = UnitextContainer()
            if (self.content is not None): 
                cnt.children.append(self.content)
            self.content = (cnt)
        cnt.children.append(UnitextPagebreak())
        if (cnt2 is not None): 
            cnt.children.extend(cnt2.children)
        elif (doc.content is not None): 
            cnt.children.append(doc.content)
        self.sections.extend(doc.sections)
    
    def serialize(self) -> bytearray:
        """ Преобразовать в байтовый поток (со сжатием). Восстанавливать потом функцией Deserialize().
        
        Returns:
            bytearray: результат
        """
        from UnitextPython.pullenti.util.ArchiveHelper import ArchiveHelper
        tmp = io.StringIO()
        with XmlWriter.create_string(tmp, UnitextDocument._new_xml_writer_settings_563("UTF-8", False)) as xml0_: 
            self.get_xml(xml0_)
        str0_ = Utils.toStringStringIO(tmp)
        dat = MiscHelper.encode_string_utf8(str0_, False)
        return ArchiveHelper.compress_gzip(dat)
    
    def deserialize(self, dat : bytearray) -> None:
        """ Восстановить документ из байтового потока, полученного функцией Serialize().
        Если что не так, то выдаст Exception.
        
        Args:
            dat(bytearray): массив байт
        """
        from UnitextPython.pullenti.util.ArchiveHelper import ArchiveHelper
        if (dat is None or len(dat) == 0): 
            return
        dat = ArchiveHelper.decompress_gzip(dat)
        txt = MiscHelper.decode_string_utf8(dat, 0, -1)
        if (Utils.isNullOrEmpty(txt)): 
            return
        xml0_ = None # new XmlDocument
        xml0_ = Utils.parseXmlFromString(txt)
        self.from_xml(xml0_.getroot())
    
    @property
    def _inner_tag(self) -> str:
        return "doc"
    
    def find_by_id(self, id0__ : str) -> 'UnitextItem':
        """ Найти элемент по его идентификатору
        
        Args:
            id0__(str): идентификатор элемента
        
        Returns:
            UnitextItem: результат или null
        """
        if (self.id0_ == id0__): 
            return self
        res = None
        if (self.content is not None): 
            res = self.content.find_by_id(id0__)
            if ((res) is not None): 
                return res
        for doc in self.inner_documents: 
            res = doc.find_by_id(id0__)
            if ((res) is not None): 
                return res
        return None
    
    @staticmethod
    def _new41(_arg1 : 'FileFormat') -> 'UnitextDocument':
        res = UnitextDocument()
        res.source_format = _arg1
        return res
    
    @staticmethod
    def _new63(_arg1 : str, _arg2 : 'FileFormat') -> 'UnitextDocument':
        res = UnitextDocument()
        res.source_file_name = _arg1
        res.source_format = _arg2
        return res
    
    @staticmethod
    def _new361(_arg1 : 'FileFormat', _arg2 : str) -> 'UnitextDocument':
        res = UnitextDocument()
        res.source_format = _arg1
        res.error_message = _arg2
        return res
    
    @staticmethod
    def _new373(_arg1 : 'FileFormat', _arg2 : str) -> 'UnitextDocument':
        res = UnitextDocument()
        res.source_format = _arg1
        res.source_file_name = _arg2
        return res
    
    @staticmethod
    def _new375(_arg1 : str) -> 'UnitextDocument':
        res = UnitextDocument()
        res.source_plain_text = _arg1
        return res
    
    @staticmethod
    def _new456(_arg1 : 'FileFormat', _arg2 : typing.List[tuple]) -> 'UnitextDocument':
        res = UnitextDocument()
        res.source_format = _arg1
        res.attrs = _arg2
        return res
    
    @staticmethod
    def _new_xml_writer_settings_563(_arg1 : str, _arg2 : bool) -> XmlWriterSettings:
        res = XmlWriterSettings()
        res.encoding = _arg1
        res.indent = _arg2
        return res