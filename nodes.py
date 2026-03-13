import json
import uuid
import sys
import os
from typing import Dict, List, Any, Optional, Tuple

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from moyin_types import (
    AIScene, AICharacter, AIScreenplay, GenerationConfig,
    CharacterBible, SceneStatus, CameraType
)
from prompt_compiler import PromptCompiler, prompt_compiler
from character_bible import (
    CharacterBibleManager, character_bible_manager,
    generate_consistency_prompt, merge_character_analyses
)


class MoyinCreateCharacter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {"default": "Character"}),
                "character_type": (["human", "cat", "dog", "rabbit", "bear", "bird", "other"],),
                "visual_traits": ("STRING", {"default": "", "multiline": True, "placeholder": "e.g., blonde hair, blue eyes, red dress"}),
            },
            "optional": {
                "style_tokens": ("STRING", {"default": "", "multiline": True, "placeholder": "e.g., anime style, soft shading"}),
                "personality": ("STRING", {"default": "", "multiline": True, "placeholder": "e.g., kind, gentle"}),
                "screenplay_id": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("character_json", "character_id")
    FUNCTION = "create_character"
    CATEGORY = "Moyin Creator/Character"
    
    def create_character(
        self,
        name: str,
        character_type: str,
        visual_traits: str,
        style_tokens: str = "",
        personality: str = "",
        screenplay_id: str = "",
    ) -> Tuple[str, str]:
        style_tokens_list = [t.strip() for t in style_tokens.split(",") if t.strip()]
        char = character_bible_manager.add_character({
            "name": name,
            "type": character_type,
            "visual_traits": visual_traits,
            "style_tokens": style_tokens_list,
            "personality": personality,
            "screenplay_id": screenplay_id,
        })
        char_json = json.dumps({
            "id": char.id,
            "name": char.name,
            "type": char.type,
            "visual_traits": char.visual_traits,
            "style_tokens": char.style_tokens,
            "personality": char.personality,
        }, ensure_ascii=False, indent=2)
        return (char_json, char.id)


class MoyinCharacterToPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character_json": ("STRING", {"default": "", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("character_prompt",)
    FUNCTION = "character_to_prompt"
    CATEGORY = "Moyin Creator/Character"
    
    def character_to_prompt(self, character_json: str) -> Tuple[str]:
        try:
            char_data = json.loads(character_json)
            visual_traits = char_data.get("visual_traits", "")
            style_tokens = char_data.get("style_tokens", [])
            name = char_data.get("name", "Character")
            
            parts = []
            if visual_traits:
                parts.append(visual_traits)
            if style_tokens:
                parts.append(", ".join(style_tokens))
            parts.append(f"character: {name}")
            
            return (", ".join(parts),)
        except:
            return ("",)


class MoyinCreateScene:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "scene_id": ("INT", {"default": 1, "min": 1, "max": 999}),
                "narration": ("STRING", {"default": "", "multiline": True, "placeholder": "中文旁白"}),
            },
            "optional": {
                "visual_content": ("STRING", {"default": "", "multiline": True, "placeholder": "English visual description"}),
                "action": ("STRING", {"default": "", "multiline": True, "placeholder": "English character action"}),
                "camera": (["Close-up", "Medium Shot", "Wide Shot", "Two-Shot", "Over-the-shoulder", "Tracking", "POV", "Low Angle", "High Angle", "Profile Shot", "Dutch Angle"],),
                "character_description": ("STRING", {"default": "", "multiline": True, "placeholder": "Character appearance"}),
                "mood": ("STRING", {"default": "", "placeholder": "e.g., peaceful, romantic"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("scene_json",)
    FUNCTION = "create_scene"
    CATEGORY = "Moyin Creator/Scene"
    
    def create_scene(
        self,
        scene_id: int,
        narration: str,
        visual_content: str = "",
        action: str = "",
        camera: str = "Medium Shot",
        character_description: str = "",
        mood: str = "",
    ) -> Tuple[str]:
        scene = {
            "scene_id": scene_id,
            "narration": narration,
            "visual_content": visual_content,
            "action": action,
            "camera": camera,
            "character_description": character_description,
            "mood": mood,
            "status": "pending",
        }
        return (json.dumps(scene, ensure_ascii=False, indent=2),)


class MoyinBuildImagePrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "style_tokens": ("STRING", {"default": "", "multiline": True, "placeholder": "e.g., anime style, vibrant colors"}),
                "character_prompt": ("STRING", {"default": "", "multiline": True, "placeholder": "Character description"}),
                "visual_content": ("STRING", {"default": "", "multiline": True, "placeholder": "Scene visual description"}),
                "camera": (["Close-up", "Medium Shot", "Wide Shot", "Two-Shot", "Over-the-shoulder", "Tracking", "POV", "Low Angle", "High Angle", "Profile Shot", "Dutch Angle"],),
                "quality_tokens": ("STRING", {"default": "high quality, 4k, detailed", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_prompt",)
    FUNCTION = "build_image_prompt"
    CATEGORY = "Moyin Creator/Prompt"
    
    def build_image_prompt(
        self,
        style_tokens: str = "",
        character_prompt: str = "",
        visual_content: str = "",
        camera: str = "Medium Shot",
        quality_tokens: str = "high quality, 4k, detailed",
    ) -> Tuple[str]:
        parts = []
        if style_tokens:
            parts.append(style_tokens)
        if character_prompt:
            parts.append(character_prompt)
        if visual_content:
            parts.append(visual_content)
        if camera:
            parts.append(camera)
        if quality_tokens:
            parts.append(quality_tokens)
        
        return (", ".join([p for p in parts if p]),)


class MoyinBuildVideoPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "character_prompt": ("STRING", {"default": "", "multiline": True}),
                "visual_content": ("STRING", {"default": "", "multiline": True}),
                "action": ("STRING", {"default": "", "multiline": True, "placeholder": "Character action description"}),
                "camera": (["Close-up", "Medium Shot", "Wide Shot", "Two-Shot", "Over-the-shoulder", "Tracking", "POV", "Low Angle", "High Angle", "Profile Shot", "Dutch Angle"],),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_prompt",)
    FUNCTION = "build_video_prompt"
    CATEGORY = "Moyin Creator/Prompt"
    
    def build_video_prompt(
        self,
        character_prompt: str = "",
        visual_content: str = "",
        action: str = "",
        camera: str = "Medium Shot",
    ) -> Tuple[str]:
        parts = []
        if character_prompt:
            parts.append(character_prompt)
        if visual_content:
            parts.append(visual_content)
        if action:
            parts.append(action)
        if camera:
            parts.append(camera)
        
        return (", ".join([p for p in parts if p]),)


class MoyinBuildNegativePrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "additional_terms": ("STRING", {"default": "", "multiline": True, "placeholder": "e.g., extra fingers, bad hands"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("negative_prompt",)
    FUNCTION = "build_negative_prompt"
    CATEGORY = "Moyin Creator/Prompt"
    
    def build_negative_prompt(self, additional_terms: str = "") -> Tuple[str]:
        base = "blurry, low quality, watermark, text, logo, signature, bad anatomy, deformed, mutated"
        if additional_terms:
            terms = [t.strip() for t in additional_terms.split(",") if t.strip()]
            if terms:
                base += ", " + ", ".join(terms)
        return (base,)


class MoyinCombineScenes:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "scene_1": ("STRING", {"default": "", "multiline": True}),
                "scene_2": ("STRING", {"default": "", "multiline": True}),
                "scene_3": ("STRING", {"default": "", "multiline": True}),
                "scene_4": ("STRING", {"default": "", "multiline": True}),
                "scene_5": ("STRING", {"default": "", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("scenes_json",)
    FUNCTION = "combine_scenes"
    CATEGORY = "Moyin Creator/Scene"
    
    def combine_scenes(
        self,
        scene_1: str = "",
        scene_2: str = "",
        scene_3: str = "",
        scene_4: str = "",
        scene_5: str = "",
    ) -> Tuple[str]:
        scenes = []
        for s in [scene_1, scene_2, scene_3, scene_4, scene_5]:
            if s and s.strip():
                try:
                    scenes.append(json.loads(s))
                except:
                    pass
        return (json.dumps(scenes, ensure_ascii=False, indent=2),)


class MoyinCreateScreenplay:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "title": ("STRING", {"default": "My Video"}),
            },
            "optional": {
                "genre": ("STRING", {"default": "", "placeholder": "e.g., romance, action"}),
                "aspect_ratio": (["16:9", "9:16"],),
                "scenes_json": ("STRING", {"default": "[]", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("screenplay_json",)
    FUNCTION = "create_screenplay"
    CATEGORY = "Moyin Creator/Screenplay"
    
    def create_screenplay(
        self,
        title: str,
        genre: str = "",
        aspect_ratio: str = "16:9",
        scenes_json: str = "[]",
    ) -> Tuple[str]:
        try:
            scenes = json.loads(scenes_json)
        except:
            scenes = []
        
        screenplay = {
            "id": str(uuid.uuid4()),
            "title": title,
            "genre": genre,
            "aspect_ratio": aspect_ratio,
            "orientation": "landscape" if aspect_ratio == "16:9" else "portrait",
            "scenes": scenes,
        }
        return (json.dumps(screenplay, ensure_ascii=False, indent=2),)


class MoyinSceneToImagePrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "scene_json": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "style_tokens": ("STRING", {"default": "", "multiline": True}),
                "character_prompt": ("STRING", {"default": "", "multiline": True}),
                "quality_tokens": ("STRING", {"default": "high quality, 4k, detailed", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_prompt",)
    FUNCTION = "scene_to_image_prompt"
    CATEGORY = "Moyin Creator/Prompt"
    
    def scene_to_image_prompt(
        self,
        scene_json: str,
        style_tokens: str = "",
        character_prompt: str = "",
        quality_tokens: str = "high quality, 4k, detailed",
    ) -> Tuple[str]:
        try:
            scene = json.loads(scene_json)
            visual_content = scene.get("visual_content", "")
            camera = scene.get("camera", "Medium Shot")
            char_desc = scene.get("character_description", "")
            
            parts = []
            if style_tokens:
                parts.append(style_tokens)
            if character_prompt:
                parts.append(character_prompt)
            elif char_desc:
                parts.append(char_desc)
            if visual_content:
                parts.append(visual_content)
            if camera:
                parts.append(camera)
            if quality_tokens:
                parts.append(quality_tokens)
            
            return (", ".join([p for p in parts if p]),)
        except:
            return ("",)


class MoyinAPIConfig:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_provider": (["OpenAI", "Anthropic", "Google", "Custom"],),
            },
            "optional": {
                "api_key": ("STRING", {"default": "", "multiline": False, "placeholder": "API Key"}),
                "api_url": ("STRING", {"default": "", "multiline": False, "placeholder": "Custom API URL (if needed)"}),
                "model": ("STRING", {"default": "gpt-4o", "placeholder": "Model name"}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 2000, "min": 100, "max": 10000, "step": 100}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("api_config_json",)
    FUNCTION = "create_api_config"
    CATEGORY = "Moyin Creator/API"
    
    def create_api_config(
        self,
        api_provider: str,
        api_key: str = "",
        api_url: str = "",
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Tuple[str]:
        config = {
            "api_provider": api_provider,
            "api_key": api_key,
            "api_url": api_url,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        return (json.dumps(config, ensure_ascii=False, indent=2),)
