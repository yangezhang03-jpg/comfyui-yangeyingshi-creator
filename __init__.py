import os
import sys
import importlib.util

# 获取当前目录的绝对路径
node_dir = os.path.dirname(os.path.abspath(__file__))

# 直接从文件路径导入 nodes 模块
nodes_path = os.path.join(node_dir, 'nodes.py')
spec = importlib.util.spec_from_file_location('yan_nodes', nodes_path)
yan_nodes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(yan_nodes)

# 从导入的模块中获取所有节点类
MoyinCreateCharacter = yan_nodes.MoyinCreateCharacter
MoyinCharacterToPrompt = yan_nodes.MoyinCharacterToPrompt
MoyinCreateScene = yan_nodes.MoyinCreateScene
MoyinBuildImagePrompt = yan_nodes.MoyinBuildImagePrompt
MoyinBuildVideoPrompt = yan_nodes.MoyinBuildVideoPrompt
MoyinBuildNegativePrompt = yan_nodes.MoyinBuildNegativePrompt
MoyinCombineScenes = yan_nodes.MoyinCombineScenes
MoyinCreateScreenplay = yan_nodes.MoyinCreateScreenplay
MoyinSceneToImagePrompt = yan_nodes.MoyinSceneToImagePrompt
MoyinAPIConfig = yan_nodes.MoyinAPIConfig

NODE_CLASS_MAPPINGS = {
    "MoyinCreateCharacter": MoyinCreateCharacter,
    "MoyinCharacterToPrompt": MoyinCharacterToPrompt,
    "MoyinCreateScene": MoyinCreateScene,
    "MoyinBuildImagePrompt": MoyinBuildImagePrompt,
    "MoyinBuildVideoPrompt": MoyinBuildVideoPrompt,
    "MoyinBuildNegativePrompt": MoyinBuildNegativePrompt,
    "MoyinCombineScenes": MoyinCombineScenes,
    "MoyinCreateScreenplay": MoyinCreateScreenplay,
    "MoyinSceneToImagePrompt": MoyinSceneToImagePrompt,
    "MoyinAPIConfig": MoyinAPIConfig,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MoyinCreateCharacter": "🪄 Create Character",
    "MoyinCharacterToPrompt": "✨ Character to Prompt",
    "MoyinCreateScene": "🎬 Create Scene",
    "MoyinBuildImagePrompt": "🖼️ Build Image Prompt",
    "MoyinBuildVideoPrompt": "🎥 Build Video Prompt",
    "MoyinBuildNegativePrompt": "🚫 Build Negative Prompt",
    "MoyinCombineScenes": "📚 Combine Scenes",
    "MoyinCreateScreenplay": "📖 Create Screenplay",
    "MoyinSceneToImagePrompt": "🎨 Scene to Image Prompt",
    "MoyinAPIConfig": "🔧 API Config",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
