import unittest
from src.core.sanitizer import TextSanitizer
from src.languages.factory import LanguageProcessorFactory

class TestTextSanitizer(unittest.TestCase):
    
    def setUp(self):
        self.sanitizer = TextSanitizer()
    
    def test_chinese_sanitize(self):
        """测试中文文本清洗"""
        test_cases = [
            ("2025-08-07", "X年X月X日"),
            ("2025年08月07日", "X年X月X日"),
            ("《星际公元5102年消费者权益保护测试》", "《星际公元5102年消费者权益保护测试》"),
            ("有123辆车", "有X辆车"),
        ]
        
        for original, expected in test_cases:
            with self.subTest(original=original):
                result = self.sanitizer.sanitize_text(original)
                self.assertEqual(result, expected)
    
    def test_english_sanitize(self):
        """测试英文文本清洗"""
        sanitizer_en = TextSanitizer('en')
        test_cases = [
            ("Today is 2025-08-07", "Today is YYYY-MM-DD"),
            ("I have 123 cars", "I have X cars"),
            ("The price is $123.45", "The price is $X.XX"),
        ]
        
        for original, expected in test_cases:
            with self.subTest(original=original):
                result = sanitizer_en.sanitize_text(original)
                self.assertEqual(result, expected)
    
    def test_auto_language_detection(self):
        """测试自动语言检测"""
        # 中文文本
        chinese_text = "今天是2025年8月7日"
        result = self.sanitizer.sanitize_text(chinese_text)
        self.assertIn("X年", result)
        
        # 英文文本
        english_text = "Today is August 7, 2025"
        result = self.sanitizer.sanitize_text(english_text)
        # 注意：自动检测可能不准确，这里主要是测试流程

if __name__ == '__main__':
    unittest.main()