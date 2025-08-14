import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)

def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON file {file_path}: {str(e)}")
        raise

def save_json_file(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
    """保存JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save JSON file {file_path}: {str(e)}")
        raise

def find_json_files(path: Union[str, Path]) -> List[Path]:
    """查找指定路径下的所有JSON文件"""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    if path.is_file():
        return [path] if path.suffix.lower() == '.json' else []
    
    return list(path.glob('**/*.json'))

def select_files(path: Union[str, Path], selected_indices: List[int] = None) -> List[Path]:
    """选择要处理的文件"""
    files = find_json_files(path)
    
    if not files:
        logger.warning("No JSON files found")
        return []
    
    if selected_indices is None:
        return [f for f in files if not f.name.endswith('_p.json')]
    
    # 过滤已处理的文件并根据索引选择
    valid_files = [f for f in files if not f.name.endswith('_p.json')]
    selected_files = [valid_files[i-1] for i in selected_indices if 1 <= i <= len(valid_files)]
    
    return selected_files