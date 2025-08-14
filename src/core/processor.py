import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List
from tqdm import tqdm
from ..utils.file_handler import load_json_file, save_json_file, select_files
from ..utils.logger import logger
from .sanitizer import TextSanitizer

class BatchProcessor:
    """批量处理JSON文件"""
    
    def __init__(self, language_code: str = 'auto', max_workers: int = 10):
        self.language_code = language_code
        self.max_workers = max_workers
        self.sanitizer = TextSanitizer(language_code)
        self.logger = logger
    
    def process_single_file(self, input_path: Path, output_path: Path) -> bool:
        """处理单个文件"""
        try:
            # 加载数据
            data = load_json_file(input_path)
            
            # 清洗数据
            processed_data = self.sanitizer.sanitize_json_data(data)
            
            # 保存数据
            save_json_file(processed_data, output_path)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to process file {input_path}: {str(e)}")
            return False
    
    def process_files(self, input_path: str, selected_indices: List[int] = None) -> int:
        """批量处理文件"""
        try:
            files = select_files(input_path, selected_indices)
            if not files:
                self.logger.warning("No files to process")
                return 0
            
            success_count = 0
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # 创建任务
                futures = {}
                for json_file in files:
                    output_file = json_file.with_name(f"{json_file.stem}_p.json")
                    future = executor.submit(self.process_single_file, json_file, output_file)
                    futures[future] = json_file
                
                # 执行任务并显示进度
                with tqdm(total=len(futures), desc="Processing files") as pbar:
                    for future in as_completed(futures):
                        json_file = futures[future]
                        try:
                            if future.result():
                                success_count += 1
                                self.logger.info(f"Successfully processed: {json_file}")
                            else:
                                self.logger.error(f"Failed to process: {json_file}")
                        except Exception as e:
                            self.logger.error(f"Exception processing {json_file}: {str(e)}")
                        finally:
                            pbar.update(1)
            
            self.logger.info(f"Batch processing completed. Success: {success_count}/{len(files)}")
            return success_count
            
        except Exception as e:
            self.logger.error(f"Batch processing failed: {str(e)}")
            return 0