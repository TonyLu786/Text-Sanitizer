"""
Utils Module
"""
import os
from pathlib import Path

def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent.parent

# 设置Python路径
import sys
project_root = get_project_root()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))