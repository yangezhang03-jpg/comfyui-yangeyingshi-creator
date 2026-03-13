import os
import sys

# Add current directory to sys.path to ensure local imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from moyin_nodes import (
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
