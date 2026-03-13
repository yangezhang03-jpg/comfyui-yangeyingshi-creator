from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class CameraType(str, Enum):
    CLOSE_UP = "Close-up"
    MEDIUM_SHOT = "Medium Shot"
    WIDE_SHOT = "Wide Shot"
    TWO_SHOT = "Two-Shot"
    OVER_THE_SHOULDER = "Over-the-shoulder"
    TRACKING = "Tracking"
    POV = "POV"
    LOW_ANGLE = "Low Angle"
    HIGH_ANGLE = "High Angle"
    PROFILE_SHOT = "Profile Shot"
    DUTCH_ANGLE = "Dutch Angle"


class SceneStatus(str, Enum):
    PENDING = "pending"
    GENERATING_IMAGE = "generating_image"
    GENERATING_VIDEO = "generating_video"
    COMPLETED = "completed"
    FAILED = "failed"


class ProviderId(str, Enum):
    MEMEFAST = "memefast"
    RUNNINGHUB = "runninghub"
    OPENAI = "openai"
    CUSTOM = "custom"


class ServiceType(str, Enum):
    CHAT = "chat"
    IMAGE = "image"
    VIDEO = "video"
    VISION = "vision"


@dataclass
class AICharacter:
    id: str
    name: str
    type: str  # 'human', 'cat', 'dog', 'rabbit', 'bear', 'bird', 'other'
    visual_traits: str
    personality: str


@dataclass
class ReferenceImage:
    id: str
    url: str
    analysis_result: Optional[Dict[str, Any]] = None
    is_primary: bool = False


@dataclass
class ThreeViewImages:
    front: Optional[str] = None
    side: Optional[str] = None
    back: Optional[str] = None


@dataclass
class CharacterBible:
    id: str
    screenplay_id: str
    name: str
    type: str
    visual_traits: str
    style_tokens: List[str] = field(default_factory=list)
    color_palette: List[str] = field(default_factory=list)
    personality: str = ""
    reference_images: List[ReferenceImage] = field(default_factory=list)
    three_view_images: Optional[ThreeViewImages] = None
    created_at: int = field(default_factory=lambda: int(__import__("time").time() * 1000))
    updated_at: int = field(default_factory=lambda: int(__import__("time").time() * 1000))


@dataclass
class AIScene:
    scene_id: int
    narration: str
    mood: Optional[str] = None
    emotional_hook: Optional[str] = None
    visual_content: str = ""
    action: str = ""
    camera: CameraType = CameraType.MEDIUM_SHOT
    character_description: str = ""
    image_prompt: Optional[str] = None
    video_prompt: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    status: SceneStatus = SceneStatus.PENDING


@dataclass
class AIScreenplay:
    id: str
    title: str
    genre: Optional[str] = None
    estimated_duration_seconds: int = 0
    emotional_arc: List[str] = field(default_factory=list)
    aspect_ratio: str = "16:9"  # '16:9' or '9:16'
    orientation: str = "landscape"  # 'landscape' or 'portrait'
    characters: List[AICharacter] = field(default_factory=list)
    scenes: List[AIScene] = field(default_factory=list)
    created_at: int = field(default_factory=lambda: int(__import__("time").time() * 1000))
    updated_at: int = field(default_factory=lambda: int(__import__("time").time() * 1000))


@dataclass
class GenerationConfig:
    style_tokens: List[str] = field(default_factory=list)
    quality_tokens: List[str] = field(default_factory=list)
    negative_prompt: str = ""
    aspect_ratio: str = "16:9"
    image_size: str = "2K"  # '1K', '2K', '4K'
    video_size: str = "720p"  # '480p', '720p', '1080p'
    scene_count: int = 5
    concurrency: int = 1
    image_provider: str = "memefast"
    video_provider: str = "memefast"
    chat_provider: str = "memefast"


@dataclass
class SceneProgress:
    scene_id: int
    status: str = "pending"
    stage: str = "idle"
    progress: float = 0.0
    media_id: Optional[str] = None
    ghost_element_id: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[int] = None
    completed_at: Optional[int] = None


@dataclass
class AsyncTaskResult:
    status: str = "pending"
    progress: Optional[float] = None
    result_url: Optional[str] = None
    error: Optional[str] = None
    estimated_time: Optional[float] = None
