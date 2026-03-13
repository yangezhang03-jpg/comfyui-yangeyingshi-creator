# ComfyUI Moyin Creator Nodes

将魔因漫创 (Moyin Creator) 的核心功能转换为 ComfyUI 自定义节点。

## 功能特性

节点按功能分组，使用更简单清晰：

### 👤 Character (角色)

#### 🪄 Create Character (创建角色)
定义角色的基本属性和视觉特征。
- **输入**:
  - `name`: 角色名称 (默认: "Character")
  - `character_type`: 角色类型 (human, cat, dog, etc.)
  - `visual_traits`: 视觉特征描述 (如: blonde hair, blue eyes)
  - `style_tokens` (可选): 风格提示词 (如: anime style)
  - `personality` (可选): 性格描述
- **输出**:
  - `character_json`: 角色的完整 JSON 数据
  - `character_id`: 角色唯一 ID

#### ✨ Character to Prompt (角色转提示词)
将角色 JSON 数据转换为用于图像生成的提示词字符串。
- **输入**:
  - `character_json`: 来自 Create Character 节点的输出
- **输出**:
  - `character_prompt`: 组合好的角色提示词

### 🎬 Scene (场景)

#### 🎬 Create Scene (创建场景)
定义单个场景的详细信息。
- **输入**:
  - `scene_id`: 场景编号
  - `narration`: 中文旁白
  - `visual_content` (可选): 画面内容的英文描述
  - `action` (可选): 角色动作的英文描述
  - `camera` (可选): 镜头类型 (Close-up, Medium Shot, etc.)
  - `character_description` (可选): 当前场景中角色的具体外观
  - `mood` (可选): 场景氛围
- **输出**:
  - `scene_json`: 场景的完整 JSON 数据

#### 📚 Combine Scenes (组合场景)
将多个场景 JSON 组合成一个列表，用于剧本创建。
- **输入**:
  - `scene_1` 到 `scene_5` (可选): 各个场景的 JSON 输出
- **输出**:
  - `scenes_json`: 包含所有输入场景的 JSON 列表

### ✨ Prompt (提示词)

#### 🖼️ Build Image Prompt (构建图像提示词)
手动构建用于文生图的完整提示词。
- **输入**:
  - `style_tokens` (可选): 风格词
  - `character_prompt` (可选): 角色描述
  - `visual_content` (可选): 场景描述
  - `camera` (可选): 镜头描述
  - `quality_tokens` (可选): 质量词 (默认: high quality, 4k...)
- **输出**:
  - `image_prompt`: 组合后的完整提示词

#### 🎥 Build Video Prompt (构建视频提示词)
构建用于文生视频的提示词。
- **输入**:
  - `character_prompt` (可选)
  - `visual_content` (可选)
  - `action` (可选)
  - `camera` (可选)
- **输出**:
  - `video_prompt`: 组合后的视频提示词

#### 🚫 Build Negative Prompt (构建负面提示词)
生成通用的负面提示词，支持添加额外词汇。
- **输入**:
  - `additional_terms` (可选): 额外的负面词汇
- **输出**:
  - `negative_prompt`: 包含基础负面词和额外词的完整字符串

#### 🎨 Scene to Image Prompt (场景转图像提示词)
智能地将场景 JSON 转换为图像生成提示词。
- **输入**:
  - `scene_json`: 场景数据
  - `style_tokens` (可选): 全局风格
  - `character_prompt` (可选): 角色描述（覆盖场景中的角色描述）
  - `quality_tokens` (可选): 质量词
- **输出**:
  - `image_prompt`: 针对该场景的优化提示词

### 📖 Screenplay (剧本)

#### 📖 Create Screenplay (创建剧本)
将多个场景组合成完整的剧本结构。
- **输入**:
  - `title`: 剧本标题
  - `genre` (可选): 类型
  - `aspect_ratio`: 画幅比例 (16:9 或 9:16)
  - `scenes_json` (可选): 场景列表 JSON
- **输出**:
  - `screenplay_json`: 完整的剧本 JSON 对象

### 🔧 API (接口)

#### 🔧 API Config (API 配置)
配置用于 AI 生成的 API 连接信息。
- **输入**:
  - `api_provider`: 服务提供商 (OpenAI, Anthropic, Google, Custom)
  - `api_key` (可选): API 密钥
  - `api_url` (可选): 自定义 API 地址
  - `model` (可选): 模型名称 (默认: gpt-4o)
  - `temperature`: 温度参数 (默认: 0.7)
  - `max_tokens`: 最大生成长度 (默认: 2000)
- **输出**:
  - `api_config_json`: API 配置数据

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

## 使用说明

### 快速开始

1. 将 `example_workflow.json` 拖拽到 ComfyUI 中
2. 查看示例工作流
3. 根据需要修改参数
4. 连接到 CLIP、KSampler、VAE 等节点生成图像
