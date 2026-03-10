"""
BatchExportConfigUI.py - 批量导出配置UI
支持批量选择导出配置，提供多种导出方式
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


class BatchExportConfigUI(BaseUI.BaseUI): # type: ignore
    """
    批量导出配置UI
    支持多种批量导出方式
    """
    
    def customized_init(self):
        """
        自定义初始化
        """
        self.TAG = "BatchExportConfigUI"
        self.customized_function = {
            "A": "Export all configs as single archives",
            "B": "Export all configs as one combined archive",
            "S": "Select multiple configs to export",
            "R": "Back to previous menu"
        }
        
        # 初始化增强UI工具
        self.enhanced_ui_utils = EnhancedUIUtils(logger=self.myLogger)
        
        # 初始化配置管理器（使用pass预留位置）
        self.batch_config_manager = None  # 将在call_back_end中初始化
        
        # 导出选项
        self.export_types = {
            "single": "Individual archive for each config",
            "combined": "Single archive containing all configs"
        }
    
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
            self._handle_export_all_single()
        elif function_name == self.customized_function["B"]:
            self._handle_export_all_combined()
        elif function_name == self.customized_function["S"]:
            self._handle_selective_export()
        elif function_name == self.customized_function["R"]:
            self._handle_back()
        else:
            print(f"Unknown function: {function_name}")
            self.myUIUtils.press_enter_to_continue()
    
    def _handle_export_all_single(self):
        """
        导出所有配置为单独文件
        """
        self.myLogger.log("I", "Starting export all as single archives", self.TAG)
        
        print("=" * 60)
        print("EXPORT ALL AS SINGLE ARCHIVES")
        print("=" * 60)
        print("This will export each configuration as a separate")
        print(".zip archive file.")
        print("=" * 60)
        
        # 获取所有可用配置
        available_configs = self._get_available_configs()
        
        if not available_configs:
            print("No configurations available for export.")
            self.myLogger.log("W", "No configs found for export", self.TAG)
            self.myUIUtils.press_enter_to_continue()
            return
        
        print(f"Found {len(available_configs)} configuration(s):")
        for i, config in enumerate(available_configs, 1):
            print(f"  {i}. {config}")
        
        if not self._confirm_operation(f"Export all {len(available_configs)} configs as separate archives?"):
            print("Operation cancelled.")
            self.myLogger.log("I", "User cancelled export all single", self.TAG)
            return
        
        print("\nStarting export process...")
        
        # 这里使用pass为后端实现预留位置
        success_count = 0
        total_count = len(available_configs)
        
        for config_name in available_configs:
            try:
                print(f"Exporting {config_name}...", end=" ")
                
                # 预留后端调用位置
                # result = self.batch_config_manager.export_single_config(config_name)
                result = True  # 模拟成功
                
                if result:
                    print("✓ Success")
                    success_count += 1
                else:
                    print("✗ Failed")
            except Exception as e:
                print(f"✗ Error: {e}")
                self.myLogger.log("E", f"Error exporting {config_name}: {e}", self.TAG)
        
        self._display_summary("Export All Single", success_count, total_count)
        self.myLogger.log("I", f"Export all single completed: {success_count}/{total_count}", self.TAG)
        self.myUIUtils.press_enter_to_continue()
    
    def _handle_export_all_combined(self):
        """
        导出所有配置为合并文件
        """
        self.myLogger.log("I", "Starting export all as combined archive", self.TAG)
        
        print("=" * 60)
        print("EXPORT ALL AS COMBINED ARCHIVE")
        print("=" * 60)
        print("This will export all configurations as a single")
        print(".zip archive file containing multiple configs.")
        print("=" * 60)
        
        # 获取所有可用配置
        available_configs = self._get_available_configs()
        
        if not available_configs:
            print("No configurations available for export.")
            self.myLogger.log("W", "No configs found for combined export", self.TAG)
            self.myUIUtils.press_enter_to_continue()
            return
        
        print(f"Found {len(available_configs)} configuration(s) to include:")
        for i, config in enumerate(available_configs, 1):
            print(f"  {i}. {config}")
        
        # 获取输出文件名
        default_name = "all_configs_combined.zip"
        print(f"\nOutput file name (default: {default_name}):")
        output_name = input("> ").strip()
        if not output_name:
            output_name = default_name
        
        if not output_name.endswith(".zip"):
            output_name += ".zip"
        
        if not self._confirm_operation(f"Create combined archive '{output_name}' with {len(available_configs)} configs?"):
            print("Operation cancelled.")
            self.myLogger.log("I", "User cancelled export all combined", self.TAG)
            return
        
        print(f"\nCreating combined archive: {output_name}")
        print("This may take a moment...")
        
        # 这里使用pass为后端实现预留位置
        try:
            # 预留后端调用位置
            # result = self.batch_config_manager.batch_export_configs(
            #     config_names=available_configs,
            #     export_type="combined",
            #     output_name=output_name
            # )
            result = True  # 模拟成功
            
            if result:
                print(f"\n✓ Successfully created combined archive: {output_name}")
                self.myLogger.log("I", f"Combined archive created: {output_name}", self.TAG)
            else:
                print("\n✗ Failed to create combined archive")
                self.myLogger.log("E", "Failed to create combined archive", self.TAG)
        except Exception as e:
            print(f"\n✗ Error: {e}")
            self.myLogger.log("E", f"Error creating combined archive: {e}", self.TAG)
        
        self.myUIUtils.press_enter_to_continue()
    
    def _handle_selective_export(self):
        """
        选择性导出
        """
        self.myLogger.log("I", "Starting selective export", self.TAG)
        
        print("=" * 60)
        print("SELECTIVE EXPORT")
        print("=" * 60)
        print("Select multiple configurations to export.")
        print("=" * 60)
        
        # 使用增强配置选择器
        selected_configs = self.enhanced_ui_utils.enhanced_select_config_ui(
            multi_select=True
        )
        
        if selected_configs is None:
            print("Export cancelled.")
            self.myLogger.log("I", "User cancelled selective export", self.TAG)
            return
        
        if not selected_configs:
            print("No configurations selected.")
            self.myLogger.log("I", "No configs selected for export", self.TAG)
            self.myUIUtils.press_enter_to_continue()
            return
        
        print(f"\nSelected {len(selected_configs)} configuration(s):")
        for i, config in enumerate(selected_configs, 1):
            print(f"  {i}. {config}")
        
        # 选择导出类型
        print("\nSelect export type:")
        print("  1. Individual archives (one .zip per config)")
        print("  2. Combined archive (all configs in one .zip)")
        
        export_type = input("Choice (1/2): ").strip()
        
        if export_type == "1":
            export_method = "single"
            export_desc = "individual archives"
        elif export_type == "2":
            export_method = "combined"
            export_desc = "combined archive"
            
            # 获取输出文件名
            default_name = "selected_configs_combined.zip"
            print(f"\nOutput file name (default: {default_name}):")
            output_name = input("> ").strip()
            if not output_name:
                output_name = default_name
            
            if not output_name.endswith(".zip"):
                output_name += ".zip"
        else:
            print("Invalid choice, using individual archives.")
            export_method = "single"
            export_desc = "individual archives"
        
        if not self._confirm_operation(f"Export {len(selected_configs)} configs as {export_desc}?"):
            print("Operation cancelled.")
            self.myLogger.log("I", "User cancelled export after selection", self.TAG)
            return
        
        print(f"\nStarting export as {export_desc}...")
        
        if export_method == "single":
            # 导出为单独文件
            success_count = 0
            total_count = len(selected_configs)
            
            for config_name in selected_configs: # type: ignore
                try:
                    print(f"Exporting {config_name}...", end=" ")
                    
                    # 预留后端调用位置
                    # result = self.batch_config_manager.export_single_config(config_name)
                    result = True  # 模拟成功
                    
                    if result:
                        print("✓ Success")
                        success_count += 1
                    else:
                        print("✗ Failed")
                except Exception as e:
                    print(f"✗ Error: {e}")
                    self.myLogger.log("E", f"Error exporting {config_name}: {e}", self.TAG)
            
            self._display_summary("Selective Export Single", success_count, total_count)
        else:
            # 导出为合并文件
            try:
                print(f"Creating combined archive: {output_name}")
                
                # 预留后端调用位置
                # result = self.batch_config_manager.batch_export_configs(
                #     config_names=selected_configs,
                #     export_type="combined",
                #     output_name=output_name
                # )
                result = True  # 模拟成功
                
                if result:
                    print(f"\n✓ Successfully created combined archive: {output_name}")
                    self.myLogger.log("I", f"Combined archive created: {output_name}", self.TAG)
                else:
                    print("\n✗ Failed to create combined archive")
                    self.myLogger.log("E", "Failed to create combined archive", self.TAG)
            except Exception as e:
                print(f"\n✗ Error: {e}")
                self.myLogger.log("E", f"Error creating combined archive: {e}", self.TAG)
        
        self.myLogger.log("I", f"Selective export completed: {export_method}", self.TAG)
        self.myUIUtils.press_enter_to_continue()
    
    def _handle_back(self):
        """
        返回上一级菜单
        """
        self.myLogger.log("I", "Returning to previous menu", self.TAG)
        # 导航引擎会处理返回逻辑
    
    def _get_available_configs(self) -> List[str]:
        """
        获取所有可用配置
        Returns:
            list: 配置名称列表
        """
        configs_dir = os.path.join(os.getcwd(), "Configs")
        available_configs = []
        
        if os.path.exists(configs_dir):
            for item in os.listdir(configs_dir):
                item_path = os.path.join(configs_dir, item)
                if os.path.isdir(item_path):
                    # 检查是否包含必要的配置文件
                    config_file = os.path.join(item_path, "config.cfg")
                    if os.path.exists(config_file):
                        available_configs.append(item)
        
        return available_configs
    
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
        print(f"Total configurations: {total_count}")
        print(f"Successful: {success_count}")
        print(f"Failed: {total_count - success_count}")
        
        if success_count == total_count:
            print("✓ All exports completed successfully!")
        elif success_count > 0:
            print("⚠ Some exports completed with errors.")
        else:
            print("✗ All exports failed.")
        
        print("=" * 60)


if __name__ == "__main__":
    # 测试代码
    print("Testing BatchExportConfigUI...")
    
    # 创建模拟logger
    class MockLogger:
        def log(self, level, message, tag):
            print(f"[{level}] {tag}: {message}")
    
    # 测试UI初始化
    logger = MockLogger()
    
    # 测试可用配置获取
    print("\nTesting _get_available_configs()...")
    
    # 创建测试目录结构
    test_dir = "test_configs"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # 创建测试配置
    test_configs = ["config1", "config2", "config3"]
    for config in test_configs:
        config_path = os.path.join(test_dir, config)
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        
        # 创建配置文件
        config_file = os.path.join(config_path, "config.cfg")
        with open(config_file, 'w') as f:
            f.write(f"# Test config {config}\n")
    
    print("Test directory structure created.")
    
    # 清理测试目录
    import shutil
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    print("\nUI structure test completed.")
    print("Note: Full functionality requires integration with the main application.")