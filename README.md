# Text-Sanitizer    文本日期、数字信息脱敏处理器
A powerful, multilingual text sanitization tool that removes sensitive information while preserving text structure and format. Perfect for data anonymization, privacy protection, and content preprocessing.
一个强大的、支持多语言的文本脱敏处理工具，可以去除文本中的敏感信息且保持原文本结构与内容。完美设计用于数据脱敏化，隐私保护与文本预处理（AIGC处理前）

<p align="center">
    <img src="https://raw.githubusercontent.com/TonyLu786/text-sanitizer/main/assets/logo.png" width="400"/>
<p>
<br>
<p align="center">
        🧹 <a href="#features">Features</a>&nbsp&nbsp | &nbsp&nbsp🚀 <a href="#quickstart">Quickstart</a>&nbsp&nbsp | &nbsp&nbsp📘 <a href="#usage">Usage</a>&nbsp&nbsp ｜ &nbsp&nbsp🛠️ <a href="#extending">Extending</a> ｜ &nbsp&nbsp🤝 <a href="#contributing">Contributing</a>
<br>
</p>
<br><br>

# Text Sanitizer

A powerful, multilingual text sanitization tool that removes sensitive information while preserving text structure and format. Perfect for data anonymization, privacy protection, and content preprocessing.

<p align="center">
    <img src="https://raw.githubusercontent.com/TonyLu786/text-sanitizer/main/assets/demo.gif" width="600"/>
<p>

---

## 🌟 Features

* **Multilingual Support**: Chinese, English, easily extensible to other languages.
* **Automatic Language Detection**: Smart language recognition for mixed-content processing.
* **Concurrent Processing**: Multi-threaded file processing for high performance.
* **Configurable Rules**: Customizable sanitization patterns and rules.
* **CLI Interface**: User-friendly command-line interface with progress bar.
* **VSCode Compatible**: Full debugging support in Visual Studio Code.
* **Enterprise-Grade**: Comprehensive logging and error handling.

---

## 📋 Prerequisites

* Python 3.8 or higher
* pip package manager

---

## 🚀 Quickstart

### Installation

```bash
# Clone the repository
git clone https://github.com/TonyLu786/text-sanitizer.git
cd text-sanitizer

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run with Sample Data

```bash
# Create sample data and run interactively
python src/main.py
# Choose option 3 to create sample data, then option 2 to test.
```

---

## 📖 Usage

### Command Line Interface

```bash
# Process all JSON files in current directory
python src/main.py --input .

# Process files with specific language
python src/main.py --input ./data --language zh

# Process specific files by index
python src/main.py --input ./data --files "1,3,5"

# Custom worker threads for faster processing
python src/main.py --input ./data --workers 20

# Show help
python src/main.py --help
```

#### Command Line Options

```bash
Options:
  -i, --input TEXT        Input directory or file path [required]
  -l, --language [auto|zh|en]
                          Language code (auto, zh, en, etc.) [default: auto]
  -w, --workers INTEGER   Number of worker threads (1-50) [default: 10]
  -f, --files TEXT        Comma-separated file indices to process (e.g., "1,3,5")
  -h, --help              Show this message and exit.
```

### Python API

```python
from src.core.sanitizer import TextSanitizer

# Create sanitizer with automatic language detection
sanitizer = TextSanitizer(language_code='auto')

# Sanitize text
clean_text = sanitizer.sanitize_text("Today is 2025-08-07")
print(clean_text)  # Output: Today is YYYY-MM-DD

# Sanitize JSON data recursively
import json
with open('data.json', 'r') as f:
    data = json.load(f)
    
clean_data = sanitizer.sanitize_json_data(data)
```

---

## 🛠 Extending to New Languages

1. **Create Language Processor**
```python
# src/languages/fr.py
from .base import BaseLanguageProcessor

class FrenchLanguageProcessor(BaseLanguageProcessor):
    def protect_special_content(self, text):
        # Implement French-specific content protection
        pass
    
    def replace_dates(self, text):
        # Implement French date patterns
        pass
    
    def replace_numbers(self, text):
        # Implement French number patterns
        pass
```

2. **Register in Factory**
```python
# src/languages/factory.py
from .fr import FrenchLanguageProcessor

class LanguageProcessorFactory:
    _processors = {
        'zh': ChineseLanguageProcessor,
        'en': EnglishLanguageProcessor,
        'fr': FrenchLanguageProcessor,  # Add new language
    }
```

---

## 📁 Project Structure

```
text-sanitizer/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── sanitizer.py        # Core sanitization logic
│   │   └── processor.py        # Batch processing
│   ├── languages/
│   │   ├── __init__.py
│   │   ├── base.py             # Base language processor
│   │   ├── zh.py               # Chinese processor
│   │   ├── en.py               # English processor
│   │   └── factory.py          # Language factory
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_handler.py     # File operations
│   │   └── logger.py           # Logging utilities
│   └── cli/
│       ├── __init__.py
│       └── cli.py              # Command line interface
├── tests/
│   ├── __init__.py
│   ├── test_sanitizer.py
│   └── test_languages.py
├── config/
│   └── language_configs.json
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_sanitizer.py

# Run with coverage
python -m pytest --cov=src tests/
```

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

---

## 📄 License

This project is licensed under the Apache License 2.0 License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

* Create an issue for bug reports
* Submit a pull request for improvements
* Contact maintainers for questions

---

*Made with ❤️ by Tony Lu | Tony Lu倾力打造*
