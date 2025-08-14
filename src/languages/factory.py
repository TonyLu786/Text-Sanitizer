from typing import Dict, Any, Optional
from .base import BaseLanguageProcessor
from .zh import ChineseLanguageProcessor
from .en import EnglishLanguageProcessor

class LanguageProcessorFactory:
    """语言处理器工厂类"""
    
    _processors = {
        'zh': ChineseLanguageProcessor,
        'en': EnglishLanguageProcessor,
    }
    
    @classmethod
    def register_processor(cls, language_code: str, processor_class):
        """注册新的语言处理器"""
        cls._processors[language_code] = processor_class
    
    @classmethod
    def create_processor(cls, language_code: str, config: Dict[str, Any] = None) -> BaseLanguageProcessor:
        """创建语言处理器实例"""
        if config is None:
            config = {}
            
        processor_class = cls._processors.get(language_code.lower())
        if not processor_class:
            raise ValueError(f"Unsupported language code: {language_code}")
        
        return processor_class(config)
    
    @classmethod
    def get_supported_languages(cls) -> list:
        """获取支持的语言列表"""
        return list(cls._processors.keys())