import click
import sys
import os
from pathlib import Path

# 设置项目路径
def setup_project_path():
    """设置项目路径"""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent
    
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    return project_root

setup_project_path()

# 多种导入方式确保兼容性
def import_modules():
    """导入所需模块，支持多种导入方式"""
    modules = {}
    
    try:
        # 方式1: 绝对导入
        from src.core.processor import BatchProcessor
        from src.languages.factory import LanguageProcessorFactory
        from src.utils.logger import logger
        modules.update({
            'BatchProcessor': BatchProcessor,
            'LanguageProcessorFactory': LanguageProcessorFactory,
            'logger': logger
        })
        print("✅ 使用绝对导入")
    except ImportError as e1:
        print(f"绝对导入失败: {e1}")
        try:
            # 方式2: 相对导入
            from ..core.processor import BatchProcessor
            from ..languages.factory import LanguageProcessorFactory
            from ..utils.logger import logger
            modules.update({
                'BatchProcessor': BatchProcessor,
                'LanguageProcessorFactory': LanguageProcessorFactory,
                'logger': logger
            })
            print("✅ 使用相对导入")
        except ImportError as e2:
            print(f"相对导入也失败: {e2}")
            raise ImportError("无法导入所需模块，请检查项目结构")
    
    return modules

# 导入模块
try:
    modules = import_modules()
    BatchProcessor = modules['BatchProcessor']
    LanguageProcessorFactory = modules['LanguageProcessorFactory']
    logger = modules['logger']
except ImportError as e:
    print(f"模块导入失败: {e}")
    raise

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--input', '-i', 
              default=None,  # 允许None，稍后验证
              help='Input directory or file path')
@click.option('--language', '-l', default='auto', 
              type=click.Choice(['auto'] + LanguageProcessorFactory.get_supported_languages()),
              help='Language code (auto, zh, en, etc.)')
@click.option('--workers', '-w', default=10, type=click.IntRange(1, 50), 
              help='Number of worker threads (1-50)')
@click.option('--files', '-f', help='Comma-separated file indices to process (e.g., "1,3,5")')
def main(input: str, language: str, workers: int, files: str):
    """Text Sanitizer CLI - Process JSON files with multilingual support"""
    
    # 参数验证和处理
    if input is None:
        # 如果没有提供input参数，使用当前目录
        input = '.'
        print("⚠️  未指定输入路径，使用当前目录")
    
    input_path = Path(input).resolve()
    if not input_path.exists():
        print(f"❌ 输入路径不存在: {input_path}")
        raise click.BadParameter(f"Input path does not exist: {input_path}")
    
    print(f"📁 处理路径: {input_path}")
    print(f"🌐 语言设置: {language}")
    print(f"⚙️  工作线程: {workers}")
    
    # 解析文件索引
    selected_indices = None
    if files:
        try:
            selected_indices = [int(x.strip()) for x in files.split(',')]
            print(f"📄 指定文件索引: {selected_indices}")
        except ValueError:
            print(f"❌ 文件索引格式错误: {files}")
            raise click.BadParameter("Invalid file indices format")
    
    try:
        # 创建批量处理器
        processor = BatchProcessor(language_code=language, max_workers=workers)
        
        # 处理文件
        print("🚀 开始处理文件...")
        success_count = processor.process_files(str(input_path), selected_indices)
        
        print(f"\n✅ 处理完成!")
        print(f"   成功处理: {success_count} 个文件")
        
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {e}")
        logger.error(f"Processing failed: {e}")
        raise click.ClickException(f"Processing failed: {e}")

# VSCode调试用的函数
def run_with_args(args_list):
    """使用指定参数列表运行CLI"""
    original_argv = sys.argv[:]
    try:
        sys.argv = [sys.argv[0]] + args_list
        main()
    finally:
        sys.argv = original_argv

if __name__ == '__main__':
    main()