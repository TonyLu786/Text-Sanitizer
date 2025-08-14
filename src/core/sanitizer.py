import logging
from typing import Any, Dict, List, Union
from ..languages.factory import LanguageProcessorFactory
from ..utils.logger import logger

class TextSanitizer:
    """文本清洗器主类"""
    
    def __init__(self, language_code: str = 'auto'):
        self.language_code = language_code
        self.processor = None
        self.logger = logger
    
    def _detect_language(self, text: str) -> str:
        """检测文本语言"""
        try:
            from langdetect import detect
            return detect(text)
        except:
            return 'zh'  # 默认返回中文
    
    def _get_processor(self, text: str = None) -> Any:
        """获取对应的语言处理器"""
        if self.language_code == 'auto' and text:
            detected_lang = self._detect_language(text)
            self.logger.info(f"Detected language: {detected_lang}")
            language_code = detected_lang
        else:
            language_code = self.language_code
        
        if not self.processor or self.processor.code != language_code:
            try:
                self.processor = LanguageProcessorFactory.create_processor(language_code)
                self.logger.info(f"Created processor for language: {language_code}")
            except ValueError as e:
                self.logger.warning(f"{str(e)}, using default Chinese processor")
                self.processor = LanguageProcessorFactory.create_processor('zh')
        
        return self.processor
    
    def sanitize_text(self, text: str) -> str:
        """清洗单个文本"""
        if not text:
            return ""
        
        processor = self._get_processor(text)
        return processor.sanitize_text(text)
    
    def sanitize_json_data(self, data: Any) -> Any:
        """递归清洗JSON数据中的所有字符串"""
        if isinstance(data, dict):
            return {k: self.sanitize_json_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_json_data(item) for item in data]
        elif isinstance(data, str):
            return self.sanitize_text(data)
        else:
            return data