from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
import re

class BaseLanguageProcessor(ABC):
    """基础语言处理器抽象类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'base')
        self.code = config.get('code', 'base')
        
    @abstractmethod
    def protect_special_content(self, text: str) -> Tuple[str, List[Tuple[str, str, str]]]:
        """保护特殊内容（如书名号、引号等）"""
        pass
    
    @abstractmethod
    def restore_special_content(self, text: str, bookmarks: List[Tuple[str, str, str]]) -> str:
        """恢复特殊内容"""
        pass
    
    @abstractmethod
    def replace_dates(self, text: str) -> str:
        """替换日期格式"""
        pass
    
    @abstractmethod
    def replace_numbers(self, text: str) -> str:
        """替换数字"""
        pass
    
    def sanitize_text(self, text: str) -> str:
        """主处理函数"""
        if text is None:
            return ""
        
        try:
            # 保护特殊内容
            protected_text, bookmarks = self.protect_special_content(text)
            
            # 替换日期和数字
            processed_text = self.replace_dates(protected_text)
            processed_text = self.replace_numbers(processed_text)
            
            # 恢复特殊内容
            final_text = self.restore_special_content(processed_text, bookmarks)
            
            # 去除多余空格
            final_text = re.sub(r'\s+', ' ', final_text).strip()
            
            return final_text
        except Exception as e:
            raise Exception(f"Text sanitization failed for language {self.code}: {str(e)}")