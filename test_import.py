#!/usr/bin/env python3
"""
测试 yan 目录的导入
"""

import os
import sys

# 添加当前目录到系统路径
yan_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, yan_dir)

print("测试导入...")
try:
    import __init__ as init
    print(f"✓ __init__.py 导入成功")
    print(f"✓ 节点数量: {len(init.NODE_CLASS_MAPPINGS)}")
    for node_name in init.NODE_CLASS_MAPPINGS:
        print(f"  - {node_name}")
    print("\n✓ 所有测试通过！")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()
