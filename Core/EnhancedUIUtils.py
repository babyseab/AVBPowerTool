"""
EnhancedUIUtils.py - 增强的UI工具类，支持键盘导航的文件选择器
继承自UIUtils，提供增强的交互体验
"""

import os
import sys
from typing import List, Optional, Union

# 导入现有UIUtils
try:
    from .UIUtils import UIUtils as BaseUIUtils
except ImportError:
    # 如果直接导入失败，尝试动态导入
    import importlib.util
    current_dir = os.path.dirname(os.path.abspath(__file__))
    uiutils_path = os.path.join(current_dir, "UIUtils.py")
    spec = importlib.util.spec_from_file_location("UIUtils", uiutils_path)
    UIUtils_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(UIUtils_module)
    sys.modules["UIUtils"] = UIUtils_module
    BaseUIUtils = UIUtils_module.UIUtils


class EnhancedUIUtils(BaseUIUtils):
    """
    增强的UI工具类，支持键盘导航的文件选择器
    继承自UIUtils，提供增强的交互体验
    """
    def __init__(self, logger=None):
        """
        初始化增强UI工具
        Args:
            logger: 日志记录器实例
        """
        super().__init__(logger)
        self.TAG = "EnhancedUIUtils"
        self.myLogger.log("I", "EnhancedUIUtils instance created", self.TAG)
    
    def enhanced_select_file_ui(self, extension_name: str = ".zip", multi_select: bool = False) -> Union[List[str], str, None]:
        """
        增强的文件选择器，支持键盘导航
        Args:
            extension_name: 文件扩展名过滤，默认".zip"
            multi_select: 是否支持多选，默认False
        Returns:
            list: 选择的文件列表（多选模式）
            str: 选择的文件（单选模式）
            None: 用户取消
        """
        self.myLogger.log("I", f"Starting enhanced file selection with extension: {extension_name}, multi_select: {multi_select}", self.TAG)
        
        # 获取当前目录下的文件
        root_dir = os.getcwd()
        available_files = []
        
        for filename in os.listdir(root_dir):
            if filename.endswith(extension_name):
                available_files.append(filename)
        
        if not available_files:
            print(f"No {extension_name} files found in current directory.")
            self.press_enter_to_continue()
            return None if not multi_select else []
        
        # 使用增强选择器
        from .Frontend.EnhancedFileSelectorUI import EnhancedFileSelectorUI
        selector = EnhancedFileSelectorUI(
            title=f"Select {extension_name} files",
            items=available_files,
            multi_select=multi_select
        )
        
        selected_items = selector.show()
        
        if selected_items is None:
            self.myLogger.log("I", "User cancelled file selection", self.TAG)
            return None
        
        if multi_select:
            self.myLogger.log("I", f"Selected {len(selected_items)} files: {selected_items}", self.TAG)
            return selected_items
        else:
            if selected_items:
                self.myLogger.log("I", f"Selected file: {selected_items[0]}", self.TAG)
                return selected_items[0]
            else:
                self.myLogger.log("I", "No file selected", self.TAG)
                return None
    
    def enhanced_select_config_ui(self, multi_select: bool = False) -> Union[List[str], str, None]:
        """
        增强的配置选择器，支持键盘导航
        Args:
            multi_select: 是否支持多选，默认False
        Returns:
            list: 选择的配置列表（多选模式）
            str: 选择的配置（单选模式）
            None: 用户取消
        """
        self.myLogger.log("I", f"Starting enhanced config selection, multi_select: {multi_select}", self.TAG)
        
        # 获取可用的配置列表
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
        
        if not available_configs:
            print("No configurations found in Configs directory.")
            self.press_enter_to_continue()
            return None if not multi_select else []
        
        # 使用增强选择器
        from .Frontend.EnhancedFileSelectorUI import EnhancedFileSelectorUI
        selector = EnhancedFileSelectorUI(
            title="Select Configurations",
            items=available_configs,
            multi_select=multi_select
        )
        
        selected_items = selector.show()
        
        if selected_items is None:
            self.myLogger.log("I", "User cancelled config selection", self.TAG)
            return None
        
        if multi_select:
            self.myLogger.log("I", f"Selected {len(selected_items)} configs: {selected_items}", self.TAG)
            return selected_items
        else:
            if selected_items:
                self.myLogger.log("I", f"Selected config: {selected_items[0]}", self.TAG)
                return selected_items[0]
            else:
                self.myLogger.log("I", "No config selected", self.TAG)
                return None
    
    def _render_file_selector(self, items: List[str], selected_indices: set, current_index: int) -> None:
        """
        渲染文件选择器界面（内部方法）
        Args:
            items: 项目列表
            selected_indices: 已选中的索引集合
            current_index: 当前高亮显示的索引
        """
        # 清屏（跨平台）
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 50)
        print("Enhanced File Selector")
        print("=" * 50)
        print("Instructions:")
        print("  ↑/↓ : Navigate")
        print("  Space : Select/Deselect (multi-select mode)")
        print("  Enter : Confirm selection")
        print("  ESC   : Cancel")
        print("  A     : Select All/Deselect All (multi-select mode)")
        print("=" * 50)
        
        for i, item in enumerate(items):
            prefix = "→ " if i == current_index else "  "
            checkbox = "[✓]" if i in selected_indices else "[ ]"
            print(f"{prefix}{checkbox} {item}")
        
        print("=" * 50)
        print("[Enter: Confirm] [ESC: Cancel]")
    
    def _handle_keyboard_input(self, key: str) -> tuple:
        """
        处理键盘输入（内部方法）
        Args:
            key: 按键字符
        Returns:
            tuple: (action, data)
            action: 'up', 'down', 'select', 'confirm', 'cancel', 'select_all', 'none'
            data: 相关数据
        """
        key = key.lower()
        
        if key in ['w', 'up']:
            return ('up', None)
        elif key in ['s', 'down']:
            return ('down', None)
        elif key == ' ':
            return ('select', None)
        elif key == '\r' or key == '\n':  # Enter
            return ('confirm', None)
        elif key == '\x1b':  # ESC
            return ('cancel', None)
        elif key == 'a':
            return ('select_all', None)
        else:
            return ('none', None)
    
    def press_enter_to_continue(self):
        """
        按Enter继续（重写父类方法，保持一致性）
        """
        input("Press Enter to continue.")


if __name__ == "__main__":
    # 简单测试
    print("Testing EnhancedUIUtils...")
    utils = EnhancedUIUtils()
    
    # 测试文件选择
    print("\n1. Testing file selection (single):")
    result = utils.enhanced_select_file_ui(".zip", False)
    print(f"Result: {result}")
    
    print("\n2. Testing config selection (multi):")
    result = utils.enhanced_select_config_ui(True)
    print(f"Result: {result}")