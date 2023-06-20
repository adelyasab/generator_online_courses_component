# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import math
from UnitextPython.pullenti.unisharp.Utils import Utils
from UnitextPython.pullenti.unisharp.Misc import RefOutArgWrapper

from UnitextPython.pullenti.unitext.internal.uni.CorrLine import CorrLine
from UnitextPython.pullenti.unitext.UnitextContainer import UnitextContainer
from UnitextPython.pullenti.unitext.UnitextItem import UnitextItem
from UnitextPython.pullenti.unitext.WhitespaceType import WhitespaceType
from UnitextPython.pullenti.unitext.UnitextPlaintext import UnitextPlaintext
from UnitextPython.pullenti.unitext.UnitextFootnote import UnitextFootnote
from UnitextPython.pullenti.unitext.internal.uni.UnitextCorrPdfLine import UnitextCorrPdfLine
from UnitextPython.pullenti.unitext.UnitextPagebreak import UnitextPagebreak
from UnitextPython.pullenti.unitext.UnitextNewline import UnitextNewline

class UnitextCorrPdfPage:
    
    def __init__(self) -> None:
        self.num = 0
        self.lines = list()
        self.page_break = None;
        self.footnotes = list()
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print("№{0} ".format(self.num), end="", file=tmp, flush=True)
        if (len(self.footnotes) > 0): 
            print("Foots:{0} ".format(len(self.footnotes)), end="", file=tmp, flush=True)
        print(str(self.lines[0]), end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def __create_pages(cnt : 'UnitextContainer') -> typing.List['UnitextCorrPdfPage']:
        pages = list()
        page = None
        line = None
        i = 0
        first_pass693 = True
        while True:
            if first_pass693: first_pass693 = False
            else: i += 1
            if (not (i < len(cnt.children))): break
            it = cnt.children[i]
            it.tag = (i)
            if (isinstance(it, UnitextPlaintext)): 
                if (Utils.isNullOrEmpty(it.text)): 
                    continue
                if (page is None): 
                    page = UnitextCorrPdfPage()
                    pages.append(page)
                    page.num = len(pages)
                    line = (None)
                    if (page.num == 19): 
                        pass
                if (line is None): 
                    line = UnitextCorrPdfLine()
                    page.lines.append(line)
                line.texts.append(Utils.asObjectOrNull(it, UnitextPlaintext))
                continue
            if (isinstance(it, UnitextNewline)): 
                if (line is not None): 
                    line.newlines.append(Utils.asObjectOrNull(it, UnitextNewline))
                line = (None)
                continue
            if (isinstance(it, UnitextPagebreak)): 
                if (page is not None): 
                    page.page_break = (Utils.asObjectOrNull(it, UnitextPagebreak))
                page = (None)
                continue
            if (isinstance(it, UnitextFootnote)): 
                continue
            line = (None)
        return pages
    
    @staticmethod
    def correct(cnt : 'UnitextContainer') -> None:
        pages = UnitextCorrPdfPage.__create_pages(cnt)
        if (len(pages) == 0): 
            return
        titles = dict()
        for p in pages: 
            for k in range(2):
                line = p.lines[(0 if k == 0 else (len(p.lines) - 1))]
                tit = line.head_text_without_numbers
                if (tit is not None): 
                    if (not tit in titles): 
                        titles[tit] = 1
                    else: 
                        titles[tit] += 1
                if (k == 0 and len(p.lines) == 1): 
                    break
        changes = False
        min_cou = math.floor(len(pages) / 4)
        if (min_cou < 2): 
            min_cou = 2
        for p in pages: 
            k = 0
            first_pass694 = True
            while True:
                if first_pass694: first_pass694 = False
                else: k += 1
                if (not (k < 2)): break
                if (len(p.lines) == 0): 
                    break
                line = p.lines[(0 if k == 0 else (len(p.lines) - 1))]
                tit = line.head_text_without_numbers
                if (tit is not None): 
                    cou = 0
                    wrapcou345 = RefOutArgWrapper(0)
                    Utils.tryGetValue(titles, tit, wrapcou345)
                    cou = wrapcou345.value
                    if (cou > min_cou or ((cou == min_cou and len(pages) == min_cou))): 
                        line.remove_all()
                        p.lines.remove(line)
                        changes = True
                        k -= 1
                        continue
                if (line.is_pure_number): 
                    line.remove_all()
                    p.lines.remove(line)
                    changes = True
                    k -= 1
                    continue
                if (k == 0 and len(p.lines) == 1): 
                    break
        if (changes): 
            for i in range(len(cnt.children) - 1, -1, -1):
                if (cnt.children[i].tag is None): 
                    del cnt.children[i]
            for i in range(len(cnt.children) - 1, -1, -1):
                cnt.children[i].tag = (i)
        for p in pages: 
            if (p.num == 57): 
                pass
            p.process_footnotes()
        changes = False
        for i in range(len(pages) - 1, -1, -1):
            if (i == 17): 
                pass
            if (pages[i].create_footnotes(cnt)): 
                changes = True
        i = 0
        while i < len(cnt.children): 
            cnt.children[i].tag = (i)
            i += 1
        total = 0
        hiphens = 0
        for p in pages: 
            for l_ in p.lines: 
                if (l_.text_length < 40): 
                    continue
                total += 1
                if (CorrLine.is_hiphen(l_.last_char)): 
                    hiphens += 1
        has_hiph = False
        if (hiphens > 0 and ((math.floor((hiphens * 100) / total))) > 10): 
            has_hiph = True
        for i in range(len(pages) - 1, -1, -1):
            page = pages[i]
            if (len(page.lines) == 0): 
                continue
            if (i == 2): 
                pass
            if (((i + 1) < len(pages)) and len(pages[i + 1].lines) > 0): 
                last = page.lines[len(page.lines) - 1]
                if (last.can_union(pages[i + 1].lines[0])): 
                    page.page_break.typ = WhitespaceType.ONESPACE
                    if (has_hiph and last.is_last_char_hiphen): 
                        page.page_break.typ = WhitespaceType.IGNORABLE
                        last.remove_last_hiph()
                    for k in range(len(last.newlines) - 1, -1, -1):
                        del cnt.children[last.newlines[k].tag]
            for j in range(len(page.lines) - 2, -1, -1):
                line = page.lines[j]
                if (line.can_union(page.lines[j + 1])): 
                    i0 = -1
                    if (len(line.newlines) > 0): 
                        i0 = (line.newlines[0].tag)
                    for k in range(len(line.newlines) - 1, -1, -1):
                        del cnt.children[line.newlines[k].tag]
                    if (has_hiph and line.is_last_char_hiphen): 
                        line.remove_last_hiph()
                    else: 
                        if (i0 < 0): 
                            i0 = ((line.texts[len(line.texts) - 1].tag) + 1)
                        cnt.children.insert(i0, UnitextPlaintext._new51(" "))
        i = 0
        first_pass695 = True
        while True:
            if first_pass695: first_pass695 = False
            else: i += 1
            if (not (i < (len(cnt.children) - 1))): break
            if ((isinstance(cnt.children[i], UnitextPagebreak)) and (isinstance(cnt.children[i + 1], UnitextNewline))): 
                del cnt.children[i + 1]
                i -= 1
                continue
            elif ((isinstance(cnt.children[i + 1], UnitextPagebreak)) and (isinstance(cnt.children[i], UnitextNewline))): 
                del cnt.children[i]
                i -= 1
                continue
    
    def process_footnotes(self) -> None:
        foots = list()
        max0_ = 0
        for i in range(len(self.lines) - 1, -1, -1):
            num_ = self.lines[i].footnote_head_num
            if (num_ > 0): 
                foots.insert(0, self.lines[i])
                max0_ = 0
            else: 
                max0_ += 1
            if (max0_ > 5): 
                break
        if (len(foots) == 0): 
            return
        i = 0
        while i < (len(foots) - 1): 
            if ((foots[i].footnote_head_num + 1) != foots[i + 1].footnote_head_num): 
                if (foots[i].footnote_head_num != (i + 1)): 
                    return
                if ((i + 2) == len(foots)): 
                    pass
                elif ((foots[i].footnote_head_num + 1) == foots[i + 2].footnote_head_num): 
                    pass
                else: 
                    return
                del foots[i + 1]
                i -= 1
            i += 1
        fi = 0
        j = 0
        max0_ = Utils.indexOfList(self.lines, foots[0], 0)
        while fi < len(foots): 
            foot = foots[fi]
            while j < max0_: 
                li = self.lines[j]
                if (j == 18): 
                    pass
                if (li.attach_foot(foot)): 
                    break
                j += 1
            if (j >= max0_): 
                break
            fi += 1
        if (fi < len(foots)): 
            return
        self.footnotes.extend(foots)
    
    def create_footnotes(self, cnt : 'UnitextContainer') -> bool:
        if (len(self.footnotes) == 0): 
            return False
        i0 = 0
        i1 = 0
        for f in range(len(self.footnotes) - 1, -1, -1):
            foot = self.footnotes[f]
            i0 = (foot.texts[0].tag)
            i1 = (i0 + 100)
            if ((f + 1) < len(self.footnotes)): 
                i1 = (self.footnotes[f + 1].texts[0].tag)
            fn = UnitextFootnote()
            fn.custom_mark = "{0}".format(foot.footnote_head_num)
            foot.res_foot = fn
            fn.content = (UnitextContainer())
            need_sp = False
            need_truct = True
            i = i0
            while (i < i1) and (i < len(cnt.children)): 
                it = cnt.children[i]
                it.parent = fn.content
                if (isinstance(it, UnitextPlaintext)): 
                    if (need_truct): 
                        need_truct = False
                        pt0 = Utils.asObjectOrNull(it, UnitextPlaintext)
                        pt0.text = pt0.text[len(fn.custom_mark):].strip()
                    if (need_sp): 
                        fn.content.children.append(UnitextPlaintext._new51(" "))
                    need_sp = False
                    fn.content.children.append(it)
                elif (isinstance(it, UnitextNewline)): 
                    need_sp = True
                else: 
                    break
                i += 1
        i1 = i0
        while i1 < len(cnt.children): 
            it = cnt.children[i1]
            if (isinstance(it, UnitextPagebreak)): 
                break
            i1 += 1
        del cnt.children[i0:i0+i1 - i0]
        for f in range(len(self.footnotes) - 1, -1, -1):
            foot = self.footnotes[f]
            i0 = (foot.ref_text.tag)
            if (foot.ref_pos == 0): 
                if (len(foot.ref_text.text) == foot.ref_len): 
                    cnt.children[i0] = (foot.res_foot)
                else: 
                    foot.ref_text.text = Utils.trimStartString(foot.ref_text.text[foot.ref_len:])
                    cnt.children.insert(i0, foot.res_foot)
            elif ((foot.ref_pos + foot.ref_len) == len(foot.ref_text.text)): 
                foot.ref_text.text = foot.ref_text.text[0:0+foot.ref_pos]
                cnt.children.insert(i0 + 1, foot.res_foot)
            else: 
                txt_tail = foot.ref_text.text[foot.ref_pos + foot.ref_len:foot.ref_pos + foot.ref_len+len(foot.ref_text.text) - foot.ref_pos - foot.ref_len]
                foot.ref_text.text = foot.ref_text.text[0:0+foot.ref_pos]
                cnt.children.insert(i0 + 1, foot.res_foot)
                cnt.children.insert(i0 + 2, UnitextPlaintext._new51(txt_tail))
        i0 = Utils.indexOfList(self.lines, self.footnotes[0], 0)
        if (i0 > 0): 
            del self.lines[i0:i0+len(self.lines) - i0]
        return True