"""
EnhancedFileSelectorUI.py - 增强型文件选择器UI组件
支持键盘导航、多选、确认取消按钮
"""

import os
import sys
from typing import List, Optional, Set


class EnhancedFileSelectorUI:
    """
    独立的增强文件选择器组件
    支持键盘导航、多选、确认取消按钮
    """
    
    def __init__(self, title: str = "Select Files", items: List[str] = None, multi_select: bool = False): # type: ignore
        """
        初始化文件选择器
        Args:
            title: 选择器标题
            items: 可选项目列表
            multi_select: 是否支持多选
        """
        self.title = title
        self.items = items or []
        self.multi_select = multi_select
        self.selected_indices: Set[int] = set()
        self.current_index = 0
        self.finished = False
        self.cancelled = False
    
    def show(self) -> Optional[List[str]]:
        """
        显示选择器并返回选择结果
        Returns:
            list: 选择的项目列表
            None: 用户取消
        """
        if not self.items:
            print("No items to select.")
            return None if not self.multi_select else []
        
        # 重置状态
        self.selected_indices.clear()
        self.current_index = 0
        self.finished = False
        self.cancelled = False
        
        # 主循环
        while not self.finished:
            self._draw_ui()
            self._process_input()
        
        # 返回结果
        if self.cancelled:
            return None
        
        selected_items = [self.items[i] for i in sorted(self.selected_indices)]
        
        # 单选模式下，确保只返回一个项目
        if not self.multi_select and selected_items:
            return [selected_items[0]]
        
        return selected_items
    
    def _draw_ui(self) -> None:
        """
        绘制UI界面
        """
        # 清屏（跨平台）
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 绘制标题和边框
        print("=" + "=" * 48 + "=")
        title_line = f"  {self.title:^46}  "
        print(title_line)
        print("=" + "=" * 48 + "=")
        
        # 绘制说明
        print("  Instructions:                               ")
        print("    ↑/↓ : Navigate items                     ")
        if self.multi_select:
            print("    Space : Select/Deselect current item      ")
            print("    A     : Select All / Deselect All         ")
        else:
            print("    Space/Enter : Select current item         ")
        print("    Enter : Confirm selection                 ")
        print("    ESC   : Cancel                            ")
        print("=" + "=" * 48 + "=")
        
        # 绘制项目列表
        if not self.items:
            print("  No items available.                          ")
        else:
            for i, item in enumerate(self.items):
                # 处理长文件名
                display_item = item
                if len(display_item) > 35:
                    display_item = display_item[:32] + "..."
                
                # 构建前缀
                if i == self.current_index:
                    prefix = "→ "
                else:
                    prefix = "  "
                
                # 构建复选框
                if self.multi_select:
                    checkbox = "[✓]" if i in self.selected_indices else "[ ]"
                else:
                    checkbox = "[●]" if i in self.selected_indices else "[○]"
                
                # 构建显示行
                line = f"{prefix}{checkbox} {display_item}"
                line = line.ljust(46)
                print(f"  {line}  ")
        
        print("=" + "=" * 48 + "=")
        
        # 绘制状态信息
        if self.multi_select:
            selected_count = len(self.selected_indices)
            status = f"Selected: {selected_count}/{len(self.items)}"
            print(f"  {status:^46}  ")
        else:
            if self.selected_indices:
                status = "Item selected"
            else:
                status = "No item selected"
            print(f"  {status:^46}  ")
        
        print("=" + "=" * 48 + "=")
        
        # 绘制按钮
        print("  [Enter: Confirm]        [ESC: Cancel]       ")
        print("=" + "=" * 48 + "=")
    
    def _process_input(self) -> None:
        """
        处理用户输入
        """
        try:
            # 获取单个字符输入（跨平台）
            if os.name == 'nt':  # Windows
                import msvcrt
                key = msvcrt.getch().decode('utf-8', errors='ignore')
            else:  # Unix/Linux/Mac
                import tty
                import termios
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except (ImportError, Exception):
            # 回退到标准输入
            key = input("").lower()
            if len(key) > 0:
                key = key[0]
            else:
                key = ''
        
        # 处理特殊键
        if key == '\x1b':  # ESC
            self.cancelled = True
            self.finished = True
            return
        
        elif key == '\r' or key == '\n':  # Enter
            # 在单选模式下，如果没有选择任何项目，选择当前项目
            if not self.multi_select and not self.selected_indices:
                self.selected_indices.add(self.current_index)
            self.finished = True
            return
        
        elif key in ['w', 'W', '\x48']:  # Up arrow or W
            if self.current_index > 0:
                self.current_index -= 1
        
        elif key in ['s', 'S', '\x50']:  # Down arrow or S
            if self.current_index < len(self.items) - 1:
                self.current_index += 1
        
        elif key == ' ':  # Space
            if self.multi_select:
                # 多选模式：切换选择状态
                if self.current_index in self.selected_indices:
                    self.selected_indices.remove(self.current_index)
                else:
                    self.selected_indices.add(self.current_index)
            else:
                # 单选模式：选择当前项目，取消其他选择
                self.selected_indices.clear()
                self.selected_indices.add(self.current_index)
        
        elif key in ['a', 'A'] and self.multi_select:  # A (全选/取消全选)
            if len(self.selected_indices) == len(self.items):
                # 如果已经全选，则取消全选
                self.selected_indices.clear()
            else:
                # 否则全选
                self.selected_indices = set(range(len(self.items)))
    
    def _get_key(self) -> str:
        """
        获取键盘输入（兼容性方法）
        Returns:
            str: 按键字符
        """
        # 简化版本，用于测试
        try:
            import msvcrt
            return msvcrt.getch().decode('utf-8', errors='ignore')
        except (ImportError, Exception):
            return input("")[0] if input("") else ''


if __name__ == "__main__":
    # 测试代码
    print("Testing EnhancedFileSelectorUI...")
    
    # 测试数据
    test_items = [
        "config1.zip",
        "config2.zip",
        "very_long_configuration_file_name_example.zip",
        "test_config.zip",
        "another_config.zip"
    ]
    
    # 测试单选模式
    print("\n1. Testing single selection mode:")
    selector1 = EnhancedFileSelectorUI(
        title="Select a Configuration File",
        items=test_items,
        multi_select=False
    )
    result1 = selector1.show()
    print(f"Selected: {result1}")
    
    # 测试多选模式
    print("\n2. Testing multi-selection mode:")
    selector2 = EnhancedFileSelectorUI(
        title="Select Multiple Configuration Files",
        items=test_items,
        multi_select=True
    )
    result2 = selector2.show()
    print(f"Selected: {result2}")
    
    # 测试空列表
    print("\n3. Testing empty list:")
    selector3 = EnhancedFileSelectorUI(
        title="Select Files",
        items=[],
        multi_select=True
    )
    result3 = selector3.show()
    print(f"Selected: {result3}")