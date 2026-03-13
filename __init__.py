import os
import sys

# 添加当前目录到系统路径，确保可以导入本地的 nodes 模块
yan_dir = os.path.dirname(os.path.abspath(__file__))
if yan_dir not in sys.path:
    sys.path.insert(0, yan_dir)

try:
    from nodes import (
        MoyinCreateCharacter,
        MoyinCharacterToPrompt,
        MoyinCreateScene,
        MoyinBuildImagePrompt,
        MoyinBuildVideoPrompt,
        MoyinBuildNegativePrompt,
        MoyinCombineScenes,
        MoyinCreateScreenplay,
        MoyinSceneToImagePrompt,
        MoyinAPIConfig,
    )
except ImportError:
    # 直接导入，不使用相对路径
    import nodes
    MoyinCreateCharacter = nodes.MoyinCreateCharacter
    MoyinCharacterToPrompt = nodes.MoyinCharacterToPrompt
    MoyinCreateScene = nodes.MoyinCreateScene
    MoyinBuildImagePrompt = nodes.MoyinBuildImagePrompt
    MoyinBuildVideoPrompt = nodes.MoyinBuildVideoPrompt
    MoyinBuildNegativePrompt = nodes.MoyinBuildNegativePrompt
    MoyinCombineScenes = nodes.MoyinCombineScenes
    MoyinCreateScreenplay = nodes.MoyinCreateScreenplay
    MoyinSceneToImagePrompt = nodes.MoyinSceneToImagePrompt
    MoyinAPIConfig = nodes.MoyinAPIConfig

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
