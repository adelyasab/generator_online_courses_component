# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from UnitextPython.pullenti.unisharp.Utils import Utils

from UnitextPython.pullenti.unitext.UnitextPlaintextType import UnitextPlaintextType
from UnitextPython.pullenti.unitext.internal.uni.CorrLine import CorrLine

class UnitextCorrPdfLine:
    
    def __init__(self) -> None:
        self.texts = list()
        self.newlines = list()
        self.ref_line = None;
        self.ref_text = None;
        self.ref_pos = 0
        self.ref_len = 0
        self.res_foot = None;
    
    def remove_all(self) -> None:
        for txt in self.texts: 
            txt.tag = None
        for nl in self.newlines: 
            nl.tag = None
    
    @property
    def is_pure_number(self) -> bool:
        if (len(self.texts) > 1): 
            return False
        num = 0
        for ch in self.texts[0].text: 
            if (str.isdigit(ch)): 
                num += 1
            elif (ch != ' ' and ch != '.'): 
                return False
        return num > 0
    
    @property
    def head_text_without_numbers(self) -> str:
        tmp = io.StringIO()
        for t in self.texts: 
            print(t.text.strip(), end="", file=tmp)
        i = 0
        while i < tmp.tell(): 
            if (not str.isdigit(Utils.getCharAtStringIO(tmp, i))): 
                if (i > 0): 
                    Utils.removeStringIO(tmp, 0, i)
                break
            i += 1
        for i in range(tmp.tell() - 1, -1, -1):
            if (not str.isdigit(Utils.getCharAtStringIO(tmp, i))): 
                Utils.setLengthStringIO(tmp, i + 1)
                break
        if (tmp.tell() == 0): 
            return None
        if (str.isdigit(Utils.getCharAtStringIO(tmp, 0))): 
            return None
        return Utils.toStringStringIO(tmp).strip()
    
    @property
    def last_char(self) -> 'char':
        for i in range(len(self.texts) - 1, -1, -1):
            for j in range(len(self.texts[i].text) - 1, -1, -1):
                ch = self.texts[i].text[j]
                if (not Utils.isWhitespace(ch)): 
                    return ch
        return ' '
    
    @property
    def is_last_char_hiphen(self) -> bool:
        return CorrLine.is_hiphen(self.last_char)
    
    def remove_last_hiph(self) -> None:
        for i in range(len(self.texts) - 1, -1, -1):
            for j in range(len(self.texts[i].text) - 1, -1, -1):
                ch = self.texts[i].text[j]
                if (CorrLine.is_hiphen(ch)): 
                    self.texts[i].text = self.texts[i].text[0:0+j]
                    return
                if (not Utils.isWhitespace(ch)): 
                    return
    
    @property
    def first_char(self) -> 'char':
        i = 0
        while i < len(self.texts): 
            for ch in self.texts[i].text: 
                if (not Utils.isWhitespace(ch)): 
                    return ch
            i += 1
        return ' '
    
    @property
    def second_char(self) -> 'char':
        cou = 0
        i = 0
        while i < len(self.texts): 
            for ch in self.texts[i].text: 
                if (not Utils.isWhitespace(ch)): 
                    cou += 1
                    if (cou > 1): 
                        return ch
            i += 1
        return ' '
    
    @property
    def text_length(self) -> int:
        len0_ = 0
        for t in self.texts: 
            for ch in t.text: 
                if (not Utils.isWhitespace(ch)): 
                    len0_ += 1
        return len0_
    
    @property
    def newlines_count(self) -> int:
        cou = 0
        for nl in self.newlines: 
            cou += nl.count
        return cou
    
    @staticmethod
    def __is_open_bracket(ch : 'char') -> bool:
        return "\"'`’<{([«“„”".find(ch) >= 0
    
    @staticmethod
    def __is_close_bracket(ch : 'char') -> bool:
        return "\"'`’>})]»”“".find(ch) >= 0
    
    @property
    def footnote_head_num(self) -> int:
        txt = self.texts[0].text
        i = 0
        while i < len(txt): 
            if (not Utils.isWhitespace(txt[i])): 
                if (not str.isdigit(txt[i])): 
                    return 0
                num = ((ord(txt[i])) - (ord('0')))
                i = (i + 1)
                while i < len(txt): 
                    if (str.isdigit(txt[i])): 
                        num = ((num * 10) + (((ord(txt[i])) - (ord('0')))))
                    else: 
                        break
                    i += 1
                if (num > 900): 
                    return 0
                if (i < len(txt)): 
                    while i < len(txt): 
                        if (not Utils.isWhitespace(txt[i])): 
                            break
                        i += 1
                    if (i >= len(txt)): 
                        if (len(self.texts) > 1 and self.texts[0].typ != UnitextPlaintextType.SIMPLE): 
                            return num
                        return 0
                    if (str.isalpha(txt[i])): 
                        if (not str.isupper(txt[i])): 
                            return 0
                    elif (not UnitextCorrPdfLine.__is_open_bracket(txt[i])): 
                        return 0
                    if (self.text_length < 8): 
                        return 0
                    return num
                if (self.texts[0].typ != UnitextPlaintextType.SIMPLE and len(self.texts) > 1): 
                    if (self.text_length < 8): 
                        return 0
                    return num
                break
            i += 1
        return 0
    
    def can_union(self, next0_ : 'UnitextCorrPdfLine') -> bool:
        if (self.text_length < 30): 
            return False
        last = self.last_char
        first = next0_.first_char
        if (CorrLine.is_hiphen(last) or last == ','): 
            return True
        if (last == '.' or last == ';' or last == ':'): 
            return False
        if (str.isalpha(first) and str.islower(first)): 
            if (str.isalpha(last) and str.isupper(last)): 
                return False
            ch1 = next0_.second_char
            if (ch1 == ')' or ch1 == '.'): 
                return False
            return True
        if (UnitextCorrPdfLine.__is_open_bracket(first)): 
            if (first == '('): 
                return True
            sec = next0_.second_char
            if (str.isalpha(sec) and str.islower(sec)): 
                return True
        return False
    
    def attach_foot(self, foot : 'UnitextCorrPdfLine') -> bool:
        num = str(foot.footnote_head_num)
        if (num == "17"): 
            pass
        i = 0
        while i < len(self.texts): 
            txt = self.texts[i].text
            j = 0
            first_pass692 = True
            while True:
                if first_pass692: first_pass692 = False
                else: j += 1
                if (not (j < len(txt))): break
                if (txt[j] == num[0]): 
                    k = 0
                    k = 0
                    while (k < len(num)) and ((k + j) < len(txt)): 
                        if (num[k] != txt[j + k]): 
                            break
                        k += 1
                    if (k < len(num)): 
                        continue
                    j1 = (j + k) - 1
                    ch0 = ' '
                    ch00 = ' '
                    doubt = False
                    if (j == 0): 
                        if (i == 0): 
                            continue
                        txt0 = self.texts[i - 1].text
                        ch0 = txt0[len(txt0) - 1]
                        if (len(txt0) > 1): 
                            ch00 = txt0[len(txt0) - 2]
                    else: 
                        ch0 = txt[j - 1]
                        if (j > 1): 
                            ch00 = txt[j - 2]
                    if (Utils.isWhitespace(ch0) or str.isdigit(ch0)): 
                        continue
                    if (str.isalpha(ch0)): 
                        pass
                    elif (ch0 == '.' or ch0 == ';' or UnitextCorrPdfLine.__is_close_bracket(ch0)): 
                        if (not str.isalpha(ch00)): 
                            continue
                    elif (ch0 == ','): 
                        doubt = True
                    else: 
                        continue
                    ch0 = ' '
                    if (j1 == (len(txt) - 1)): 
                        if (i == (len(self.texts) - 1)): 
                            ch0 = ' '
                        else: 
                            ch0 = self.texts[i + 1].text[0]
                    else: 
                        ch0 = txt[j1 + 1]
                    if (str.isalnum(ch0)): 
                        continue
                    if (doubt and ch0 != ' ' and self.texts[i].typ == UnitextPlaintextType.SIMPLE): 
                        continue
                    foot.ref_line = self
                    foot.ref_text = self.texts[i]
                    foot.ref_pos = j
                    foot.ref_len = ((j1 + 1) - j)
                    return True
            i += 1
        return False
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        num = self.footnote_head_num
        if (num > 0): 
            print("[{0}] ".format(num), end="", file=tmp, flush=True)
        if (self.ref_text is not None): 
            print(" -> ({0})[{1}] ".format(self.ref_text.text, self.ref_pos), end="", file=tmp, flush=True)
        for t in self.texts: 
            print(t.text, end="", file=tmp)
        return Utils.toStringStringIO(tmp)