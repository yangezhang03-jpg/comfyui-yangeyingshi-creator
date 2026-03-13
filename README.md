# ComfyUI Moyin Creator Nodes

将魔因漫创 (Moyin Creator) 的核心功能转换为 ComfyUI 自定义节点。

## 功能特性

节点按功能分组，使用更简单清晰：

### 👤 Character (角色)
- **🪄 Create Character** - 创建角色
- **✨ Character to Prompt** - 角色转提示词

### 🎬 Scene (场景)
- **🎬 Create Scene** - 创建场景
- **📚 Combine Scenes** - 组合场景

### ✨ Prompt (提示词)
- **🖼️ Build Image Prompt** - 构建图像提示词
- **🎥 Build Video Prompt** - 构建视频提示词
- **🚫 Build Negative Prompt** - 构建负面提示词
- **🎨 Scene to Image Prompt** - 场景转图像提示词

### 📖 Screenplay (剧本)
- **📖 Create Screenplay** - 创建剧本

### 🔧 API (接口)
- **🔧 API Config** - API 配置

## 安装方法

### 方法 1: 手动安装（推荐）

1. 将 `comfyui-moyin-nodes` 文件夹复制到 ComfyUI 的 `custom_nodes` 目录下：
   ```
   ComfyUI/
   └── custom_nodes/
       └── comfyui-moyin-nodes/
           ├── __init__.py
           ├── moyin_nodes.py    <-- 注意：原 nodes.py 已重命名
           ├── moyin_types.py
           ├── prompt_compiler.py
           ├── character_bible.py
           ├── example_workflow.json
           └── README.md
   ```

2. **重启 ComfyUI**（必须完全重启，不是刷新页面）

3. 在 ComfyUI 中搜索节点：
   - 右键点击画布 → Add Node → Moyin Creator
   - 或直接在搜索框输入 "Moyin" 或节点名称

### 方法 2: Git 安装

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/yangezhang03-jpg/comfyui-yangeyingshi-creator.git
```

然后重启 ComfyUI。

## 常见问题

### 启动报错 `ImportError: cannot import name ... from 'nodes'`

这是因为旧版本的 `nodes.py` 与 ComfyUI 核心文件冲突。
**解决方案**：
1. 删除旧的插件文件夹
2. 重新下载最新代码（确保包含 `moyin_nodes.py` 而不是 `nodes.py`）
3. 重启 ComfyUI

### 搜索不到节点？

1. **确认文件夹位置正确**：必须在 `ComfyUI/custom_nodes/` 下
2. **确认已重启 ComfyUI**：不是刷新浏览器，是完全关闭再打开
3. **检查 ComfyUI 控制台**：看是否有错误信息
4. **确认文件名**：`moyin_nodes.py`（不是 `nodes.py`）

### 节点在哪里？

节点在以下分组中：
- `Moyin Creator/Character` - 角色相关节点
- `Moyin Creator/Scene` - 场景相关节点
- `Moyin Creator/Prompt` - 提示词相关节点
- `Moyin Creator/Screenplay` - 剧本相关节点
- `Moyin Creator/API` - API 相关节点

或者直接搜索：
- "Create Character"
- "Create Scene"
- "Build Image Prompt"
- 等等...

## 使用说明

### 快速开始

1. 将 `example_workflow.json` 拖拽到 ComfyUI 中
2. 查看示例工作流
3. 根据需要修改参数
4. 连接到 CLIP、KSampler、VAE 等节点生成图像
