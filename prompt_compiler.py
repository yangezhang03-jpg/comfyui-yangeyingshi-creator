import re
import sys
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from moyin_types import AIScene, AICharacter, GenerationConfig


@dataclass
class PromptTemplateConfig:
    scene_image: str
    scene_video: str
    negative: str
    screenplay: str


DEFAULT_TEMPLATES: PromptTemplateConfig = PromptTemplateConfig(
    scene_image="{{style_tokens}}, {{character_description}}, {{visual_content}}, {{camera}}, {{quality_tokens}}",
    scene_video="{{character_description}}, {{visual_content}}, {{action}}, {{camera}}",
    negative="blurry, low quality, watermark, text, logo, signature, bad anatomy, deformed, mutated",
    screenplay="""你是一个专业的视频剧本创作者。请根据以下描述创作一个短视频剧本：

描述：{{prompt}}

要求：
1. 创作 {{scene_count}} 个场景
2. 每个场景包含：场景编号、旁白、视觉内容描述、角色动作、镜头类型、角色外观描述
3. visualContent/action/camera/characterDescription 用英文描述
4. narration 用中文
5. 不要输出 mood/情绪 字段（前端不需要）

输出格式为 JSON：
{
  "title": "视频标题",
  "scenes": [
    {
      "sceneId": 1,
      "narration": "中文旁白",
      "visualContent": "English visual description",
      "action": "English character action",
      "camera": "Camera type in English (Close-up/Medium Shot/Wide Shot/etc.)",
      "characterDescription": "English character appearance description"
    }
  ]
}"""
)


class PromptCompiler:
    def __init__(self, custom_templates: Optional[Dict[str, str]] = None):
        self.templates = {
            "scene_image": DEFAULT_TEMPLATES.scene_image,
            "scene_video": DEFAULT_TEMPLATES.scene_video,
            "negative": DEFAULT_TEMPLATES.negative,
            "screenplay": DEFAULT_TEMPLATES.screenplay,
        }
        if custom_templates:
            self.templates.update(custom_templates)
    
    def compile(self, template_id: str, variables: Dict[str, Any]) -> str:
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template '{template_id}' not found")
        return self._interpolate(template, variables)
    
    def _interpolate(self, template: str, variables: Dict[str, Any]) -> str:
        def replace(match):
            key = match.group(1)
            value = variables.get(key)
            if value is None or value == "":
                return ""
            return str(value)
        
        return re.sub(r'\{\{(\w+)\}\}', replace, template)
    
    def compile_scene_image_prompt(
        self,
        scene: AIScene,
        characters: List[AICharacter],
        config: GenerationConfig
    ) -> str:
        character_desc = scene.character_description or ", ".join([c.visual_traits for c in characters])
        
        return self.compile("scene_image", {
            "style_tokens": ", ".join(config.style_tokens),
            "character_description": character_desc,
            "visual_content": scene.visual_content,
            "camera": scene.camera,
            "quality_tokens": ", ".join(config.quality_tokens),
        })
    
    def compile_scene_video_prompt(
        self,
        scene: AIScene,
        characters: List[AICharacter]
    ) -> str:
        character_desc = scene.character_description or ", ".join([c.visual_traits for c in characters])
        
        return self.compile("scene_video", {
            "character_description": character_desc,
            "visual_content": scene.visual_content,
            "action": scene.action,
            "camera": scene.camera,
        })
    
    def compile_screenplay_prompt(self, user_prompt: str, scene_count: int = 5) -> str:
        return self.compile("screenplay", {
            "prompt": user_prompt,
            "scene_count": scene_count,
        })
    
    def get_negative_prompt(self, additional_terms: Optional[List[str]] = None) -> str:
        negative = self.templates["negative"]
        if additional_terms and len(additional_terms) > 0:
            negative += ", " + ", ".join(additional_terms)
        return negative
    
    def update_templates(self, updates: Dict[str, str]) -> None:
        self.templates.update(updates)
    
    def get_templates(self) -> Dict[str, str]:
        return self.templates.copy()


prompt_compiler = PromptCompiler()
