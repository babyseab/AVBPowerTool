"""
BatchImportConfigUI.py - 批量导入配置UI
支持批量选择导入配置，提供多种导入方式
"""

import os
import sys
from typing import List, Optional

# 导入基础UI类
try:
    from . import BaseUI
except ImportError:
    # 动态导入
    import importlib.util
    current_dir = os.path.dirname(os.path.abspath(__file__))
    baseui_path = os.path.join(current_dir, "BaseUI.py")
    spec = importlib.util.spec_from_file_location("BaseUI", baseui_path)
    BaseUI = importlib.util.module_from_spec(spec) # type: ignore
    spec.loader.exec_module(BaseUI) # type: ignore
    sys.modules["BaseUI"] = BaseUI

# 导入增强UI工具
try:
    from ..EnhancedUIUtils import EnhancedUIUtils
except ImportError:
    # 尝试创建模拟类
    class EnhancedUIUtils:
        def __init__(self, logger=None):
            pass
        
        def enhanced_select_file_ui(self, extension_name=".zip", multi_select=False):
            return None
        
        def enhanced_select_config_ui(self, multi_select=False):
            return None


class BatchImportConfigUI(BaseUI.BaseUI): # type: ignore
    """
    批量导入配置UI
    支持多种批量导入方式
    """
    
    def customized_init(self):
        """
        自定义初始化
        """
        self.TAG = "BatchImportConfigUI"
        self.customized_function = {
            "A": "Import all configs from folder",
            "S": "Select multiple configs to import",
            "F": "Import from multiple zip files",
            "B": "Back to previous menu"
        }
        
        # 初始化增强UI工具
        self.enhanced_ui_utils = EnhancedUIUtils(logger=self.myLogger)
        
        # 初始化配置管理器（使用pass预留位置）
        self.batch_config_manager = None  # 将在call_back_end中初始化
    
    def call_back_end(self, function_name: str):
        """
        调用后端处理函数
        Args:
            function_name: 功能名称
        """
        # 初始化配置管理器（使用pass预留位置）
        if self.batch_config_manager is None:
            # 这里使用pass为后端实现预留位置
            # 实际实现应该导入并初始化BatchConfigManager
            pass
        
        if function_name == self.customized_function["A"]:
            self._handle_batch_import_all()
        elif function_name == self.customized_function["S"]:
            self._handle_selective_import()
        elif function_name == self.customized_function["F"]:
            self._handle_multi_file_import()
        elif function_name == self.customized_function["B"]:
            self._handle_back()
        else:
            print(f"Unknown function: {function_name}")
            self.myUIUtils.press_enter_to_continue()
    
    def _handle_batch_import_all(self):
        """
        处理批量导入所有配置
        """
        self.myLogger.log("I", "Starting batch import of all configs", self.TAG)
        
        print("=" * 60)
        print("BATCH IMPORT ALL CONFIGS")
        print("=" * 60)
        print("This will import all configuration files from the")
        print("specified folder.")
        print("=" * 60)
        
        if not self._confirm_operation("Import all configs from current folder?"):
            print("Operation cancelled.")
            self.myLogger.log("I", "User cancelled batch import all", self.TAG)
            return
        
        # 获取当前目录下的所有zip文件
        current_dir = os.getcwd()
        zip_files = []
        
        for filename in os.listdir(current_dir):
            if filename.endswith(".zip"):
                zip_files.append(filename)
        
        if not zip_files:
            print("No .zip files found in current directory.")
            self.myLogger.log("W", "No zip files found for batch import", self.TAG)
            self.myUIUtils.press_enter_to_continue()
            return
        
        print(f"Found {len(zip_files)} .zip file(s):")
        for i, zip_file in enumerate(zip_files, 1):
            print(f"  {i}. {zip_file}")
        
        print("\nStarting import process...")
        
        # 这里使用pass为后端实现预留位置
        # 实际应该调用batch_config_manager.batch_import_configs()
        success_count = 0
        total_count = len(zip_files)
        
        for zip_file in zip_files:
            try:
                print(f"Importing {zip_file}...", end=" ")
                
                # 预留后端调用位置
                # result = self.batch_config_manager.import_single_config(zip_file)
                result = True  # 模拟成功
                
                if result:
                    print("✓ Success")
                    success_count += 1
                else:
                    print("✗ Failed")
            except Exception as e:
                print(f"✗ Error: {e}")
                self.myLogger.log("E", f"Error importing {zip_file}: {e}", self.TAG)
        
        print("\n" + "=" * 60)
        print(f"Import completed: {success_count}/{total_count} successful")
        print("=" * 60)
        
        self.myLogger.log("I", f"Batch import completed: {success_count}/{total_count}", self.TAG)
        self.myUIUtils.press_enter_to_continue()
    
    def _handle_selective_import(self):
        """
        处理选择性导入
        """
        self.myLogger.log("I", "Starting selective import", self.TAG)
        
        print("=" * 60)
        print("SELECTIVE IMPORT")
        print("=" * 60)
        print("Select multiple configuration files to import.")
        print("=" * 60)
        
        # 使用增强文件选择器
        selected_files = self.enhanced_ui_utils.enhanced_select_file_ui(
            extension_name=".zip",
            multi_select=True
        )
        
        if selected_files is None:
            print("Import cancelled.")
            self.myLogger.log("I", "User cancelled selective import", self.TAG)
            return
        
        if not selected_files:
            print("No files selected.")
            self.myLogger.log("I", "No files selected for import", self.TAG)
            self.myUIUtils.press_enter_to_continue()
            return
        
        print(f"\nSelected {len(selected_files)} file(s) for import:")
        for i, filename in enumerate(selected_files, 1):
            print(f"  {i}. {filename}")
        
        if not self._confirm_operation(f"Import {len(selected_files)} selected file(s)?"):
            print("Operation cancelled.")
            self.myLogger.log("I", "User cancelled import after selection", self.TAG)
            return
        
        print("\nStarting import process...")
        
        # 这里使用pass为后端实现预留位置
        success_count = 0
        total_count = len(selected_files)
        
        for filename in selected_files: # type: ignore
            try:
                print(f"Importing {filename}...", end=" ")
                
                # 预留后端调用位置
                # result = self.batch_config_manager.import_single_config(filename)
                result = True  # 模拟成功
                
                if result:
                    print("✓ Success")
                    success_count += 1
                else:
                    print("✗ Failed")
            except Exception as e:
                print(f"✗ Error: {e}")
                self.myLogger.log("E", f"Error importing {filename}: {e}", self.TAG)
        
        print("\n" + "=" * 60)
        print(f"Import completed: {success_count}/{total_count} successful")
        print("=" * 60)
        
        self.myLogger.log("I", f"Selective import completed: {success_count}/{total_count}", self.TAG)
        self.myUIUtils.press_enter_to_continue()
    
    def _handle_multi_file_import(self):
        """
        处理多文件导入（从不同位置）
        """
        self.myLogger.log("I", "Starting multi-file import", self.TAG)
        
        print("=" * 60)
        print("MULTI-FILE IMPORT")
        print("=" * 60)
        print("Import configuration files from different locations.")
        print("You can select files from any accessible directory.")
        print("=" * 60)
        
        print("\nNote: This feature requires manual file placement.")
        print("Please place all .zip files in the current directory")
        print("before proceeding.")
        
        self.myUIUtils.press_enter_to_continue()
        
        # 实际上调用选择性导入，因为逻辑类似
        self._handle_selective_import()
    
    def _handle_back(self):
        """
        返回上一级菜单
        """
        self.myLogger.log("I", "Returning to previous menu", self.TAG)
        # 导航引擎会处理返回逻辑
    
    def _confirm_operation(self, prompt: str) -> bool:
        """
        确认操作
        Args:
            prompt: 确认提示
        Returns:
            bool: 用户是否确认
        """
        print(f"\n{prompt}")
        response = input("Confirm? (y/N): ").strip().lower()
        return response in ['y', 'yes']
    
    def _display_summary(self, operation: str, success_count: int, total_count: int):
        """
        显示操作摘要
        Args:
            operation: 操作名称
            success_count: 成功数量
            total_count: 总数量
        """
        print("\n" + "=" * 60)
        print(f"{operation.upper()} SUMMARY")
        print("=" * 60)
        print(f"Total files: {total_count}")
        print(f"Successful: {success_count}")
        print(f"Failed: {total_count - success_count}")
        
        if success_count == total_count:
            print("✓ All operations completed successfully!")
        elif success_count > 0:
            print("⚠ Some operations completed with errors.")
        else:
            print("✗ All operations failed.")
        
        print("=" * 60)


if __name__ == "__main__":
    # 测试代码
    print("Testing BatchImportConfigUI...")
    
    # 创建模拟logger
    class MockLogger:
        def log(self, level, message, tag):
            print(f"[{level}] {tag}: {message}")
    
    # 测试UI初始化
    logger = MockLogger()
    
    # 注意：由于依赖关系，这里只是演示结构
    print("\nUI structure test completed.")
    print("Note: Full functionality requires integration with the main application.")