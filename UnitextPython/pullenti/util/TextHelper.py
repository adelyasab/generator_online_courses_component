# SDK Pullenti Unitext, version 4.19, may 2023. Copyright (c) 2013, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
import math
import pathlib
from enum import IntEnum
from UnitextPython.pullenti.unisharp.Utils import Utils
from UnitextPython.pullenti.unisharp.Misc import RefOutArgWrapper
from UnitextPython.pullenti.unisharp.Streams import FileStream
from UnitextPython.pullenti.unisharp.Streams import Stream

from UnitextPython.pullenti.util.MiscHelper import MiscHelper
from UnitextPython.pullenti.unitext.FileFormatClass import FileFormatClass
from UnitextPython.pullenti.unitext.CreateDocumentParam import CreateDocumentParam
from UnitextPython.pullenti.unitext.UnitextService import UnitextService
from UnitextPython.pullenti.unitext.UnitextItem import UnitextItem
from UnitextPython.pullenti.unitext.FileFormat import FileFormat
from UnitextPython.pullenti.util.EncodingWrapper import EncodingWrapper
from UnitextPython.pullenti.util.FileFormatsHelper import FileFormatsHelper
from UnitextPython.pullenti.unitext.internal.uni.UnitextHelper import UnitextHelper

class TextHelper:
    """ Различные утилитки работы с текстами """
    
    class ComapreTextsResult(IntEnum):
        NOTEQUAL = 0
        FIRSTSTARTSWITHSECOND = 1
        SECONDSTARTSWITHFIRST = 2
        EQUALS = 3
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    @staticmethod
    def get_words(text : str) -> typing.List[str]:
        """ Преобразовать текст в список слов (разделителем является любой пробельный символ)
        
        Args:
            text(str): 
        
        """
        if (text is None): 
            return None
        res = list()
        i = 0
        first_pass746 = True
        while True:
            if first_pass746: first_pass746 = False
            else: i += 1
            if (not (i < len(text))): break
            if (Utils.isWhitespace(text[i])): 
                continue
            j = 0
            j = i
            while j < len(text): 
                if (Utils.isWhitespace(text[j])): 
                    break
                j += 1
            res.append(text[i:i+j - i])
            i = j
        return res
    
    @staticmethod
    def correct_whitespaces(txt : str) -> str:
        """ Получение текста из текстового файла, при этом автоматически определяется
        кодировка Windows-1251 или DOS и осуществляется соответствующее преобразование
        (английский текст не изменяется).
        Также корректируются переходы на новую строку, чтобы везде были бы \r\n .
        
        Args:
            fileName: имя текстового файла
        
        Returns:
            str: результат
        Корректировка символов перехода на новую строку (одно 0D или 0A преобразуются в 0D0A),
        замена nbsp на обычные пробелы
            txt(str): 
        
        """
        if (txt is None): 
            return None
        i = 0
        i = 0
        while i < len(txt): 
            if ((ord(txt[i])) == 0xD): 
                if ((i + 1) >= len(txt)): 
                    break
                if ((ord(txt[i + 1])) != 0xA): 
                    break
            elif ((ord(txt[i])) == 0xA): 
                if (i == 0): 
                    break
                if ((ord(txt[i - 1])) != 0xD): 
                    break
            elif ((ord(txt[i])) == 0xA0): 
                break
            i += 1
        if (i >= len(txt)): 
            return txt
        res = io.StringIO()
        i = 0
        while i < len(txt): 
            if ((ord(txt[i])) == 0xD): 
                print("\r\n", end="", file=res)
                if (((i + 1) < len(txt)) and (ord(txt[i + 1])) == 0xA): 
                    i += 1
            elif ((ord(txt[i])) == 0xA): 
                print("\r\n", end="", file=res)
            elif ((ord(txt[i])) == 0xA0): 
                print(' ', end="", file=res)
            else: 
                print(txt[i], end="", file=res)
            i += 1
        res_txt = Utils.toStringStringIO(res)
        i = 0
        while i < (len(res_txt) - 1): 
            if ((ord(res_txt[i])) == 0xD and (ord(res_txt[i + 1])) == 0xD): 
                pass
            i += 1
        return res_txt
    
    @staticmethod
    def correct_newlines_for_paragraphs(txt : str, count : int) -> str:
        """ Исправиление ситуации, когда текстографический формат для размещения слитного фрагмента текста
        разбивает его на строки (например, для PDF). Производится анализ таких ситуаций и замена
        переносов на пробелы.
        
        Args:
            txt(str): текст
            count(int): вернёт количество исправлений
        
        Returns:
            str: исправленный или исходный текст
        """
        count.value = 0
        if (Utils.isNullOrEmpty(txt)): 
            return txt
        i = 0
        j = 0
        cou = 0
        total_len = 0
        i = 0
        first_pass747 = True
        while True:
            if first_pass747: first_pass747 = False
            else: i += 1
            if (not (i < len(txt))): break
            ch = txt[i]
            if ((ord(ch)) != 0xD and (ord(ch)) != 0xA and ch != '\f'): 
                continue
            len0_ = 0
            last_char = ch
            j = (i + 1)
            while j < len(txt): 
                ch = txt[j]
                if ((ord(ch)) == 0xD or (ord(ch)) == 0xA or ch == '\f'): 
                    break
                elif ((ord(ch)) == 0x9): 
                    len0_ += 5
                else: 
                    last_char = ch
                    len0_ += 1
                j += 1
            if (j >= len(txt)): 
                break
            if (len0_ < 30): 
                continue
            if (len0_ > 200): 
                return txt
            if (last_char != '.' and last_char != ':' and last_char != ';'): 
                next_is_dig = False
                k = j + 1
                while k < len(txt): 
                    if (not Utils.isWhitespace(txt[k])): 
                        if (str.isdigit(txt[k])): 
                            next_is_dig = True
                        break
                    k += 1
                if (not next_is_dig): 
                    cou += 1
                    total_len += len0_
            i = j
        if (cou < 4): 
            return txt
        total_len = math.floor(total_len / cou)
        if ((total_len < 50) or total_len > 100): 
            return txt
        tmp = Utils.newStringIO(txt)
        i = 0
        while i < tmp.tell(): 
            ch = Utils.getCharAtStringIO(tmp, i)
            jj = 0
            len0_ = 0
            last_char = ch
            j = (i + 1)
            while j < tmp.tell(): 
                ch = Utils.getCharAtStringIO(tmp, j)
                if ((ord(ch)) == 0xD or (ord(ch)) == 0xA or ch == '\f'): 
                    break
                elif ((ord(ch)) == 0x9): 
                    len0_ += 5
                else: 
                    last_char = ch
                    len0_ += 1
                j += 1
            if (j >= tmp.tell()): 
                break
            for jj in range(j - 1, -1, -1):
                last_char = Utils.getCharAtStringIO(tmp, jj)
                if (not Utils.isWhitespace(last_char)): 
                    break
            else: jj = -1
            not_single = False
            jj = (j + 1)
            if ((jj < tmp.tell()) and (ord(Utils.getCharAtStringIO(tmp, j))) == 0xD and (ord(Utils.getCharAtStringIO(tmp, jj))) == 0xA): 
                jj += 1
            while jj < tmp.tell(): 
                ch = Utils.getCharAtStringIO(tmp, jj)
                if (not Utils.isWhitespace(ch)): 
                    break
                if ((ord(ch)) == 0xD or (ord(ch)) == 0xA or ch == '\f'): 
                    not_single = True
                    break
                jj += 1
            if (((not not_single and len0_ > (total_len - 20) and (len0_ < (total_len + 10))) and last_char != '.' and last_char != ':') and last_char != ';'): 
                Utils.setCharAtStringIO(tmp, j, ' ')
                count.value += 1
                if ((j + 1) < tmp.tell()): 
                    ch = Utils.getCharAtStringIO(tmp, j + 1)
                    if ((ord(ch)) == 0xA): 
                        Utils.setCharAtStringIO(tmp, j + 1, ' ')
                        j += 1
            i = (j - 1)
            i += 1
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def read_string_from_file(file_name : str, utf8 : bool=False) -> str:
        """ Считывание текста из текстового файла.
        Кодировка файла определяется префиксом. Поддерживаются такие префиксы:
        EF BB BF - для UTF8
        FF FE или FE FF - для Unicode, младний байт раньше
        
        Если префикс не задан, то подразумевается Windows-1251
        
        Args:
            file_name(str): имя входного файла
        
        Returns:
            str: строка или null при отсутствии
        """
        data = UnitextHelper.load_data_from_file(file_name, 0)
        if (data is None): 
            return None
        return TextHelper.read_string_from_bytes(data, False)
    
    @staticmethod
    def check_encoding(file_name : str) -> 'EncodingWrapper':
        fi = pathlib.Path(file_name)
        if (not fi.is_file() or fi.stat().st_size == (0)): 
            return None
        buf = Utils.newArrayOfBytes((5000 if fi.stat().st_size > (5000) else fi.stat().st_size), 0)
        with FileStream(file_name, "rb") as f: 
            f.read(buf, 0, len(buf))
        i = 0
        wrapi620 = RefOutArgWrapper(0)
        inoutres621 = EncodingWrapper.check_encoding(buf, wrapi620)
        i = wrapi620.value
        return inoutres621
    
    @staticmethod
    def read_string_from_bytes(data : bytearray, utf8 : bool=False) -> str:
        if (utf8): 
            return MiscHelper.decode_string_utf8(data, 0, -1)
        hlen = 0
        wraphlen622 = RefOutArgWrapper(0)
        enc = EncodingWrapper.check_encoding(data, wraphlen622)
        hlen = wraphlen622.value
        if (enc is None): 
            return None
        txt = enc.get_string(data, 0, -1)
        return TextHelper.correct_whitespaces(txt)
    
    @staticmethod
    def write_string_to_file(str0_ : str, file_name : str) -> None:
        """ Сохранение текста в файл. Формат UTF-8, вставляется префикс EF BB BF.
        
        Args:
            str0_(str): 
            file_name(str): 
        """
        if (str0_ is None): 
            str0_ = ""
        data = MiscHelper.encode_string_utf8(str0_, True)
        with FileStream(file_name, "wb") as f: 
            f.write(data, 0, len(data))
    
    @staticmethod
    def write_string1251to_file(str0_ : str, file_name : str) -> None:
        """ Сохранить строку в файле в кодировке Windows-1251
        
        Args:
            str0_(str): 
            file_name(str): 
        """
        if (str0_ is None or file_name is None): 
            return
        with FileStream(file_name, "wb") as f: 
            data = MiscHelper.encode_string1251(str0_)
            f.write(data, 0, len(data))
    
    @staticmethod
    def compare_texts(str1 : str, str2 : str, ignore_case : bool=False, ignore_spec_chars : bool=False) -> 'ComapreTextsResult':
        """ Проверка совпадения строк, пробелы игнорируются
        
        Args:
            str1(str): 
            str2(str): 
            ignore_case(bool): игнорировать регистр букв
            ignore_spec_chars(bool): игнорировать небуквы и нецифры
        
        """
        if (str1 is None or str2 is None): 
            return (TextHelper.ComapreTextsResult.EQUALS if str1 == str2 else TextHelper.ComapreTextsResult.NOTEQUAL)
        i1 = 0
        i2 = 0
        while True:
            first_pass748 = True
            while True:
                if first_pass748: first_pass748 = False
                else: i1 += 1
                if (not (i1 < len(str1))): break
                if (not Utils.isWhitespace(str1[i1])): 
                    if (ignore_spec_chars): 
                        if (not str.isalnum(str1[i1])): 
                            continue
                    break
            first_pass749 = True
            while True:
                if first_pass749: first_pass749 = False
                else: i2 += 1
                if (not (i2 < len(str2))): break
                if (not Utils.isWhitespace(str2[i2])): 
                    if (ignore_spec_chars): 
                        if (not str.isalnum(str2[i2])): 
                            continue
                    break
            if (i1 >= len(str1)): 
                break
            if (i2 >= len(str2)): 
                break
            ch1 = str1[i1]
            ch2 = str2[i2]
            if (ch1 != ch2 and ignore_case): 
                ch1 = str.upper(ch1)
                ch2 = str.upper(ch2)
            if (ch1 == 'ё'): 
                ch1 = 'е'
            if (ch2 == 'ё'): 
                ch2 = 'е'
            if (ch1 == 'Ё'): 
                ch1 = 'Е'
            if (ch2 == 'Ё'): 
                ch2 = 'Е'
            if (ch1 != ch2): 
                return TextHelper.ComapreTextsResult.NOTEQUAL
            i1 += 1
            i2 += 1
        TextHelper.M_COMPARE_TEXTS_END_CHAR1 = i1
        TextHelper.M_COMPARE_TEXTS_END_CHAR2 = i2
        if (i1 >= len(str1) and i2 >= len(str2)): 
            return TextHelper.ComapreTextsResult.EQUALS
        if (i1 >= len(str1)): 
            return TextHelper.ComapreTextsResult.SECONDSTARTSWITHFIRST
        if (i2 >= len(str2)): 
            return TextHelper.ComapreTextsResult.FIRSTSTARTSWITHSECOND
        return TextHelper.ComapreTextsResult.NOTEQUAL
    
    M_COMPARE_TEXTS_END_CHAR1 = None
    
    M_COMPARE_TEXTS_END_CHAR2 = None
    
    @staticmethod
    def extract_text(file_name : str, content : bytearray=None, unzip_archives : bool=True) -> str:
        """ Выделить текст из всех форматов, какие только поддерживаются
        (кроме архивов)
        
        Args:
            file_name(str): имя файла (может быть null)
            content(bytearray): содержимое файла (если null, то fileName есть имя файла в локальной файловой системе)
            unzip_archives(bool): при true будет распаковывать архивы и извлекать тексты из файлов,
        суммарный текст получается конкатенацией
        
        Returns:
            str: плоский текст или null
        """
        frm = FileFormatsHelper.analize_file_format(file_name, content)
        if (frm == FileFormat.UNKNOWN): 
            return None
        frmcl = FileFormatsHelper.get_format_class(frm)
        if (frmcl == FileFormatClass.ARCHIVE and not unzip_archives): 
            return None
        if (frmcl == FileFormatClass.IMAGE): 
            return None
        doc = UnitextService.create_document(file_name, content, CreateDocumentParam._new623(True, not unzip_archives))
        if (doc is None): 
            return None
        return UnitextHelper.get_plaintext(doc, None)