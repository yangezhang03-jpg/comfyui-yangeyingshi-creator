#!/usr/bin/env python3
"""
Moyin Creator 节点诊断工具
运行这个脚本来检查节点是否可以被正确导入
"""

import sys
import os

print("="*60)
print("Moyin Creator 节点诊断工具")
print("="*60)

# 检查目录结构
print("\n1. 检查文件和目录...")
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"   当前目录: {current_dir}")

required_files = [
    "__init__.py",
    "moyin_nodes.py",  # Updated from nodes.py
    "moyin_types.py",
    "character_bible.py",
    "prompt_compiler.py",
]

all_exist = True
for file in required_files:
    file_path = os.path.join(current_dir, file)
    exists = os.path.exists(file_path)
    status = "✓" if exists else "✗"
    print(f"   {status} {file}")
    if not exists:
        all_exist = False

if not all_exist:
    print("\n✗ 错误：缺少必要文件！")
    sys.exit(1)

# 测试导入
print("\n2. 测试节点导入...")
try:
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # 导入 __init__
    import __init__ as init_module
    
    print("   ✓ __init__.py 导入成功")
    
    # 检查节点映射
    if hasattr(init_module, 'NODE_CLASS_MAPPINGS'):
        print(f"   ✓ NODE_CLASS_MAPPINGS 存在，包含 {len(init_module.NODE_CLASS_MAPPINGS)} 个节点")
        for key, value in init_module.NODE_CLASS_MAPPINGS.items():
            print(f"      - {key}")
    else:
        print("   ✗ NODE_CLASS_MAPPINGS 不存在！")
        
    if hasattr(init_module, 'NODE_DISPLAY_NAME_MAPPINGS'):
        print(f"   ✓ NODE_DISPLAY_NAME_MAPPINGS 存在")
    else:
        print("   ✗ NODE_DISPLAY_NAME_MAPPINGS 不存在！")
        
    print("\n" + "="*60)
    print("✓ 所有诊断通过！节点应该可以正常工作。")
    print("="*60)
    print("\n如果 ComfyUI 中仍然看不到节点，请：")
    print("1. 确保文件夹在 ComfyUI/custom_nodes/comfyui-moyin-nodes/")
    print("2. 完全重启 ComfyUI（不是刷新页面）")
    print("3. 检查 ComfyUI 控制台是否有错误信息")
    
except Exception as e:
    print(f"\n✗ 导入错误: {type(e).__name__}: {e}")
    import traceback
    print("\n详细错误信息:")
    print(traceback.format_exc())
    sys.exit(1)
