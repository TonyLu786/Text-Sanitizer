import unittest
from src.languages.factory import LanguageProcessorFactory

class TestLanguageProcessors(unittest.TestCase):
    
    def test_supported_languages(self):
        """测试支持的语言"""
        supported = LanguageProcessorFactory.get_supported_languages()
        self.assertIn('zh', supported)
        self.assertIn('en', supported)
    
    def test_processor_creation(self):
        """测试处理器创建"""
        # 中文处理器
        zh_processor = LanguageProcessorFactory.create_processor('zh')
        self.assertIsNotNone(zh_processor)
        self.assertEqual(zh_processor.code, 'zh')
        
        # 英文处理器
        en_processor = LanguageProcessorFactory.create_processor('en')
        self.assertIsNotNone(en_processor)
        self.assertEqual(en_processor.code, 'en')
    
    def test_unsupported_language(self):
        """测试不支持的语言"""
        with self.assertRaises(ValueError):
            LanguageProcessorFactory.create_processor('xx')

if __name__ == '__main__':
    unittest.main()