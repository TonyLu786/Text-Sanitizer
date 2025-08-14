#!/usr/bin/env python3
"""
Text Sanitizer - A multilingual text sanitization tool
Supports Chinese, English and more languages
"""

import sys
import os
from pathlib import Path

# 设置项目路径 - 兼容VSCode运行环境
def setup_project_path():
    """设置项目路径，确保在VSCode中能正确导入模块"""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    
    # 添加项目根目录到Python路径
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"✅ Added to PYTHONPATH: {project_root}")
    
    return project_root

# 设置路径
project_root = setup_project_path()

def main():
    """主函数 - VSCode友好的入口"""
    try:
        # 动态导入CLI模块
        from src.cli.cli import main as cli_main
        print("✅ Successfully imported CLI module")
        cli_main()
        
    except SystemExit as e:
        # 处理Click的SystemExit异常
        if e.code == 2:
            print("\n💡 使用说明:")
            print("   请提供必需的 --input 参数")
            print("   示例命令:")
            print("     python src/main.py --input ./data")
            print("     python src/main.py --input . --language zh")
            print("     python src/main.py --input ./test_data --workers 5")
        elif e.code == 0:
            print("✅ 程序正常退出")
        else:
            print(f"⚠️  程序退出，代码: {e.code}")
            
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在项目根目录运行此脚本")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"项目根目录: {project_root}")
        
    except Exception as e:
        print(f"❌ 发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()

# VSCode调试友好的运行方式
def debug_run(input_path="./test_data", language="auto", workers=10, files=None):
    """
    调试运行函数 - 用于VSCode中快速测试
    
    Args:
        input_path: 输入路径，默认为./test_data
        language: 语言代码，默认为auto
        workers: 工作线程数，默认为10
        files: 文件索引列表，默认为None
    """
    print("🔧 调试模式运行...")
    print(f"   输入路径: {input_path}")
    print(f"   语言: {language}")
    print(f"   工作线程: {workers}")
    
    try:
        # 构造命令行参数
        args = ['--input', input_path, '--language', language, '--workers', str(workers)]
        if files:
            args.extend(['--files', ','.join(map(str, files))])
        
        # 设置sys.argv
        original_argv = sys.argv[:]
        sys.argv = [sys.argv[0]] + args
        
        # 运行CLI
        from src.cli.cli import main as cli_main
        cli_main()
        
        # 恢复原始参数
        sys.argv = original_argv
        
    except Exception as e:
        print(f"❌ 调试运行出错: {e}")
        import traceback
        traceback.print_exc()

# 创建测试数据的辅助函数
def create_sample_data():
    """创建示例测试数据"""
    test_dir = project_root / "test_data"
    test_dir.mkdir(exist_ok=True)
    
    # 中文测试数据
    zh_sample = {
        "title": "《星际公元5102年消费者权益保护测试》",
        "content": "今天是5102年18月27日，共有231架个人SSTO参与测试，参与率为98.5%",
        "details": {
            "date_range": "5102年1月-16月",
            "count": "共计456个测试案例"
        }
    }
    
    # 英文测试数据
    en_sample = {
        "title": "Insurance Test Report 5102",
        "content": "Today is August 17, 5102, with 231 personal SSTO tested, participation rate 98.5%",
        "details": {
            "date_range": "January-June 5102",
            "count": "Total 456 test cases"
        }
    }
    
    import json
    
    # 保存中文测试数据
    zh_file = test_dir / "chinese_sample.json"
    with open(zh_file, 'w', encoding='utf-8') as f:
        json.dump(zh_sample, f, ensure_ascii=False, indent=2)
    
    # 保存英文测试数据
    en_file = test_dir / "english_sample.json"
    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(en_sample, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建测试数据:")
    print(f"   {zh_file}")
    print(f"   {en_file}")
    
    return str(test_dir)

if __name__ == '__main__':
    # 检查是否提供了命令行参数
    if len(sys.argv) == 1:
        # 没有参数时，提供交互式选择
        print("=== Text Sanitizer ===")
        print("1. 正常运行 (需要提供参数)")
        print("2. 调试运行 (使用测试数据)")
        print("3. 创建测试数据")
        print("4. 显示帮助")
        
        choice = input("请选择 (1-4, 默认: 2): ").strip()
        
        if choice == '1':
            main()
        elif choice == '3':
            test_path = create_sample_data()
            print(f"\n创建完成！可以使用以下命令测试:")
            print(f"python src/main.py --input {test_path}")
        elif choice == '4':
            # 显示帮助
            try:
                from src.cli.cli import main as cli_main
                original_argv = sys.argv[:]
                sys.argv = [sys.argv[0], '--help']
                cli_main()
                sys.argv = original_argv
            except SystemExit:
                pass
        else:
            # 默认调试运行
            test_path = create_sample_data()
            debug_run(input_path=test_path, language="auto", workers=5)
    else:
        # 有参数时正常运行
        main()