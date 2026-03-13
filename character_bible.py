import time
import uuid
import sys
import os
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from moyin_types import CharacterBible, ReferenceImage, ThreeViewImages, AICharacter


class CharacterBibleManager:
    def __init__(self):
        self.characters: Dict[str, CharacterBible] = {}
    
    def add_character(self, character: Dict[str, Any]) -> CharacterBible:
        char_id = f"char_{int(time.time() * 1000)}_{uuid.uuid4().hex[:9]}"
        now = int(time.time() * 1000)
        
        reference_images = []
        if "reference_images" in character:
            for ref in character["reference_images"]:
                reference_images.append(ReferenceImage(**ref))
        
        three_view_images = None
        if "three_view_images" in character and character["three_view_images"]:
            three_view_images = ThreeViewImages(**character["three_view_images"])
        
        new_char = CharacterBible(
            id=char_id,
            screenplay_id=character.get("screenplay_id", ""),
            name=character.get("name", "Unknown"),
            type=character.get("type", "other"),
            visual_traits=character.get("visual_traits", ""),
            style_tokens=character.get("style_tokens", []),
            color_palette=character.get("color_palette", []),
            personality=character.get("personality", ""),
            reference_images=reference_images,
            three_view_images=three_view_images,
            created_at=now,
            updated_at=now,
        )
        
        self.characters[char_id] = new_char
        return new_char
    
    def update_character(self, char_id: str, updates: Dict[str, Any]) -> Optional[CharacterBible]:
        existing = self.characters.get(char_id)
        if not existing:
            return None
        
        update_dict = {k: v for k, v in updates.items() if k != "id" and k != "created_at"}
        update_dict["updated_at"] = int(time.time() * 1000)
        
        for key, value in update_dict.items():
            if hasattr(existing, key):
                setattr(existing, key, value)
        
        self.characters[char_id] = existing
        return existing
    
    def get_character(self, char_id: str) -> Optional[CharacterBible]:
        return self.characters.get(char_id)
    
    def get_characters_for_screenplay(self, screenplay_id: str) -> List[CharacterBible]:
        return [c for c in self.characters.values() if c.screenplay_id == screenplay_id]
    
    def delete_character(self, char_id: str) -> bool:
        if char_id in self.characters:
            del self.characters[char_id]
            return True
        return False
    
    def build_character_prompt(self, character_ids: List[str]) -> str:
        characters = [self.characters.get(cid) for cid in character_ids if self.characters.get(cid)]
        if not characters:
            return ""
        return "; ".join([f"[{c.name}]: {c.visual_traits}" for c in characters])
    
    def build_style_tokens(self, character_ids: List[str]) -> List[str]:
        characters = [self.characters.get(cid) for cid in character_ids if self.characters.get(cid)]
        token_set = set()
        for c in characters:
            for token in c.style_tokens:
                token_set.add(token)
        return list(token_set)
    
    def create_from_analysis(
        self,
        screenplay_id: str,
        analysis_result: Dict[str, Any],
        reference_image_url: Optional[str] = None
    ) -> CharacterBible:
        reference_images = []
        if reference_image_url:
            reference_images.append(ReferenceImage(
                id=f"ref_{int(time.time() * 1000)}",
                url=reference_image_url,
                analysis_result=analysis_result,
                is_primary=True
            ))
        
        return self.add_character({
            "screenplay_id": screenplay_id,
            "name": analysis_result.get("name", "Unknown"),
            "type": analysis_result.get("type", "other"),
            "visual_traits": analysis_result.get("visual_traits", ""),
            "style_tokens": analysis_result.get("style_tokens", []),
            "color_palette": analysis_result.get("color_palette", []),
            "personality": analysis_result.get("personality", ""),
            "reference_images": [asdict(r) for r in reference_images]
        })
    
    def export_all(self) -> List[Dict[str, Any]]:
        result = []
        for char in self.characters.values():
            char_dict = asdict(char)
            result.append(char_dict)
        return result
    
    def import_all(self, characters: List[Dict[str, Any]]) -> None:
        self.characters.clear()
        for char_data in characters:
            char_id = char_data.get("id")
            if char_id:
                char = CharacterBible(**char_data)
                self.characters[char_id] = char
    
    def clear(self) -> None:
        self.characters.clear()


_manager_instance: Optional[CharacterBibleManager] = None


def get_character_bible_manager() -> CharacterBibleManager:
    global _manager_instance
    if not _manager_instance:
        _manager_instance = CharacterBibleManager()
    return _manager_instance


character_bible_manager = get_character_bible_manager()


def generate_consistency_prompt(character: CharacterBible) -> str:
    parts: List[str] = []
    
    if character.visual_traits:
        parts.append(character.visual_traits)
    
    if character.style_tokens:
        parts.append(", ".join(character.style_tokens))
    
    parts.append(f"character: {character.name}")
    
    return ", ".join(parts)


def merge_character_analyses(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not analyses:
        return {}
    
    if len(analyses) == 1:
        return {
            "visual_traits": analyses[0].get("visual_traits", ""),
            "style_tokens": analyses[0].get("style_tokens", []),
            "color_palette": analyses[0].get("color_palette", []),
            "personality": analyses[0].get("personality", ""),
        }
    
    visual_traits = sorted(
        [a.get("visual_traits", "") for a in analyses if a.get("visual_traits")],
        key=lambda x: len(x),
        reverse=True
    )[0] if any(a.get("visual_traits") for a in analyses) else ""
    
    style_token_set = set()
    for a in analyses:
        for token in a.get("style_tokens", []):
            style_token_set.add(token)
    
    color_set = set()
    for a in analyses:
        for color in a.get("color_palette", []):
            color_set.add(color)
    
    personality = next((a.get("personality", "") for a in analyses if a.get("personality")), "")
    
    return {
        "visual_traits": visual_traits,
        "style_tokens": list(style_token_set),
        "color_palette": list(color_set),
        "personality": personality,
    }
