import re
import uuid
from typing import List, Tuple
from .base import BaseLanguageProcessor

class ChineseLanguageProcessor(BaseLanguageProcessor):
    """中文语言处理器"""
    
    def protect_special_content(self, text: str) -> Tuple[str, List[Tuple[str, str, str]]]:
        """保护书名号和双引号内的内容"""
        bookmark_pattern = re.compile(r'《(.*?)》|“(.*?)”')
        bookmarks = []
        protected_text = text
        
        for match in bookmark_pattern.finditer(text):
            content = match.group(1) if match.group(1) else match.group(2)
            quote_type = '《' if match.group(1) else '“'
            placeholder = f'__BOOKMARK_{uuid.uuid4().hex}__'
            bookmarks.append((placeholder, content, quote_type))
            protected_text = protected_text.replace(match.group(0), placeholder)
        
        return protected_text, bookmarks
    
    def restore_special_content(self, text: str, bookmarks: List[Tuple[str, str, str]]) -> str:
        """恢复书名号和双引号内的内容"""
        restored_text = text
        for placeholder, content, quote_type in bookmarks:
            if quote_type == '《':
                restored_text = restored_text.replace(placeholder, f'《{content}》')
            else:
                restored_text = restored_text.replace(placeholder, f'“{content}”')
        return restored_text
    
    def replace_dates(self, text: str) -> str:
        """替换中文日期格式"""
        patterns = [
            (r'\d{4}年\d{1,2}月\d{1,2}日', 'X年X月X日'),
            (r'\d{4}-\d{1,2}-\d{1,2}', 'X年X月X日'),
            (r'\d{4}年\d{1,2}月', 'X年X月'),
            (r'\d{1,2}月\d{1,2}日', 'X月X日'),
            (r'\d{1,2}-\d{1,2}月', 'X-X月'),
            (r'\d{1,2} 月\d{1,2} 日', 'X月X日'),
            (r'\d{4}年', 'X年'),
            (r'\d{1,2}月', 'X月'),
            (r'\d{1,2}日', 'X日'),
            (r'\d{4}/\d{1,2}/\d{1,2}', 'X年X月X日'),
        ]
        
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)
        return text
    
    def replace_numbers(self, text: str) -> str:
        """替换中文数字"""
        if text is None:
            return ""
        
        # 替换带单位的数字
        units = r'(辆|个|所|家|车|只|队|位|笔|头|楼|层|多|条|张|片|块|类|万|道|封|百|-|届|和|亿|千|根|本|台|架|扇|朵|堆|队|名|厘|分|种|场|余|人|项|期|件|本|篇|%|份|次|X)'
        text = re.sub(r'(\d+\.?\d*)' + units, r'X\2', text)
        
        # 定义中文标点符号
        chinese_quotes = r'(《|》|“|”|『|』|「|」|〈|〉|「|」)'
        
        # 替换独立数字，排除中文标点符号内的内容
        text = re.sub(
            rf'(?<!{chinese_quotes})\b(\d+\.?\d*)\b(?![{chinese_quotes}])',
            lambda x: 'X' * len(x.group(1)) if x.group(1) is not None else x.group(0),
            text
        )
        
        # 替换特定汉字后的数字
        specific_words = r'(量|如|例|和|率|到|达|获)'
        text = re.sub(
            rf'(?<!{chinese_quotes})({specific_words})(\s*)(\d+\.?\d*)',
            lambda m: f"{m.group(1)}{m.group(2)}{'X' * len(m.group(3))}",
            text
        )
        
        # 清理异常情况
        text = re.sub(r'XNone', 'X', text)
        text = re.sub(r'量None', '量X', text)
        text = re.sub(r'None', '', text)
        
        return text