import re
import uuid
from typing import List, Tuple
from .base import BaseLanguageProcessor

class EnglishLanguageProcessor(BaseLanguageProcessor):
    """英文语言处理器"""
    
    def protect_special_content(self, text: str) -> Tuple[str, List[Tuple[str, str, str]]]:
        """保护引号内的内容"""
        quote_pattern = re.compile(r'"([^"]*)"|\'([^\']*)\'')
        bookmarks = []
        protected_text = text
        
        for match in quote_pattern.finditer(text):
            content = match.group(1) if match.group(1) else match.group(2)
            quote_type = '"' if match.group(1) else "'"
            placeholder = f'__BOOKMARK_{uuid.uuid4().hex}__'
            bookmarks.append((placeholder, content, quote_type))
            protected_text = protected_text.replace(match.group(0), placeholder)
        
        return protected_text, bookmarks
    
    def restore_special_content(self, text: str, bookmarks: List[Tuple[str, str, str]]) -> str:
        """恢复引号内的内容"""
        restored_text = text
        for placeholder, content, quote_type in bookmarks:
            restored_text = restored_text.replace(placeholder, f'{quote_type}{content}{quote_type}')
        return restored_text
    
    def replace_dates(self, text: str) -> str:
        """替换英文日期格式"""
        patterns = [
            (r'\d{1,2}/\d{1,2}/\d{4}', 'MM/DD/YYYY'),
            (r'\d{4}-\d{1,2}-\d{1,2}', 'YYYY-MM-DD'),
            (r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}', 'Month DD, YYYY'),
            (r'\d{1,2}/\d{4}', 'MM/YYYY'),
            (r'\d{4}', 'YYYY'),
        ]
        
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text
    
    def replace_numbers(self, text: str) -> str:
        """替换英文数字"""
        if text is None:
            return ""
        
        # 替换单位数字（英文常见单位）
        units = r'(cars?|vehicles?|people|items?|units?|dollars?|USD|%|percent)'
        text = re.sub(r'(\d+\.?\d*)\s*' + units, r'X \2', text, flags=re.IGNORECASE)
        
        # 替换独立数字
        text = re.sub(
            r'\b(\d+\.?\d*)\b',
            lambda x: 'X' * len(x.group(1)) if x.group(1) is not None else x.group(0),
            text
        )
        
        return text