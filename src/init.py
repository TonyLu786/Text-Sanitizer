"""
Text Sanitizer Package
"""
__version__ = "1.0.0"
__author__ = "Tony Lu"

# 导出主要类
from .core.sanitizer import TextSanitizer
from .core.processor import BatchProcessor
from .cli.cli import main as cli_main

__all__ = ['TextSanitizer', 'BatchProcessor', 'cli_main']