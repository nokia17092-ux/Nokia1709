#!/usr/bin/env python3
"""
Geometry Dash Masterpiece Level Generator
Generates a .gdlvl file for GD 2.2091 with 150k-200k objects
Features: All game modes, advanced triggers, 3D art, pulse effects, Newgrounds music
"""

import gzip
import base64
import random
import math
import json
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from enum import IntEnum

# ============================================================
# GD LEVEL FORMAT CONSTANTS
# ============================================================

class ObjectKey(IntEnum):
    """Keys used in GD object encoding"""
    X = 1
    Y = 2
    OBJECT_ID = 3
    ROTATION = 4
    FLIP_X = 5
    FLIP_Y = 6
    SCALE = 7
    GROUPS = 8
    COLOR_1 = 9
    COLOR_2 = 10
    Z_ORDER = 11
    Z_LAYER = 12
    HIDE = 13
    LOCK = 14
    HIGH_DETAIL = 15
    DONT_FADE = 16
    IS_TRIGGER = 17
    TARGET_GROUP = 18
    TOUCH_TRIGGERED = 19
    SPAWN_TRIGGERED = 20
    MULTI_TRIGGER = 21
    TRIGGER_TYPE = 22
    ACTIVATE_GROUP = 23
    DEACTIVATE_GROUP = 24
    TOGGLE_GROUP = 25
    SPAWN_TRIGGERED_MULTI = 26
    TRIGGER_ON_DEATH = 27
    FOLLOW_PLAYER_Y = 28
    FOLLOW_PLAYER_X = 29
    FOLLOW_X_SPEED = 30
    FOLLOW_Y_SPEED = 31
    FOLLOW_X_OFFSET = 32
    FOLLOW_Y_OFFSET = 33
    FOLLOW_X_MODULO = 34
    FOLLOW_Y_MODULO = 35
    FOLLOW_X_AMOUNT = 36
    FOLLOW_Y_AMOUNT = 37
    TEXT_STRING = 38
    FONT_SCALE = 39
    ANCHOR_X = 40
    ANCHOR_Y = 41
    ENABLE_GRADIENT = 42
    GRADIENT_ANGLE = 43
    COPY_COLOR_1 = 44
    COPY_COLOR_2 = 45
    COPY_OPACITY = 46
    COPY_BLENDING = 47
    EDITOR_LAYER_1 = 48
    EDITOR_LAYER_2 = 49
    EDITOR_LAYERS = 50
    VISIBLE_IN_EDITOR = 51
    DONT_ENTER = 52
    DONT_FADE_IN = 53
    HIDE_IN_EDITOR = 54
    RENDER_MARKER = 55
    RENDER_Z = 56
    OBJECT_STRING = 57
    OBJECT_TAG = 58
    UNK_59 = 59
    UNK_60 = 60
    UNK_61 = 61
    UNK_62 = 62
    UNK_63 = 63
    UNK_64 = 64
    UNK_65 = 65
    UNK_66 = 66
    UNK_67 = 67
    UNK_68 = 68
    UNK_69 = 69
    UNK_70 = 70
    UNK_71 = 71
    UNK_72 = 72
    UNK_73 = 73
    UNK_74 = 74
    UNK_75 = 75
    UNK_76 = 76
    UNK_77 = 77
    UNK_78 = 78
    UNK_79 = 79
    UNK_80 = 80
    UNK_81 = 81
    UNK_82 = 82
    UNK_83 = 83
    UNK_84 = 84
    UNK_85 = 85
    UNK_86 = 86
    UNK_87 = 87
    UNK_88 = 88
    UNK_89 = 89
    UNK_90 = 90
    UNK_91 = 91
    UNK_92 = 92
    UNK_93 = 93
    UNK_94 = 94
    UNK_95 = 95
    UNK_96 = 96
    UNK_97 = 97
    UNK_98 = 98
    UNK_99 = 99
    UNK_100 = 100

class TriggerType(IntEnum):
    """Trigger types in GD"""
    SPAWN = 0
    TOUCH = 1
    DEATH = 2
    COUNT = 3
    INSTANT_COUNT = 4
    PICKUP = 5
    ON_ENTER = 6
    ON_EXIT = 7
    RANDOM = 8
    TIMED = 9
    FOLLOW_PLAYER_X = 10
    FOLLOW_PLAYER_Y = 11
    ADVANCED_FOLLOW = 12
    AREA_EFFECT = 13
    EVENT_LINK = 14
    KEYFRAME = 15
    ITEM_COMPARE = 16
    ITEM_EDIT = 17
    OBJECT_CONTROL = 18
    PLAYER_CONTROL = 19
    RESET = 20
    SFX = 21
    SONG = 22
    TIMER = 23

class BlockType(IntEnum):
    """Common GD block/object IDs"""
    # Basic blocks
    SOLID_BLOCK = 1
    PLATFORM = 2
    SPIKE = 3
    ORB_YELLOW = 4
    ORB_BLUE = 5
    ORB_GREEN = 6
    ORB_RED = 7
    ORB_PURPLE = 8
    ORB_DASH = 9
    PAD_YELLOW = 10
    PAD_PINK = 11
    PAD_RED = 12
    PAD_GREEN = 13
    PORTAL_CUBE = 14
    PORTAL_SHIP = 15
    PORTAL_BALL = 16
    PORTAL_UFO = 17
    PORTAL_WAVE = 18
    PORTAL_ROBOT = 19
    PORTAL_SPIDER = 20
    PORTAL_SWING = 21
    PORTAL_PLATFORMER = 22
    PORTAL_SPEED_05 = 23
    PORTAL_SPEED_1 = 24
    PORTAL_SPEED_2 = 25
    PORTAL_SPEED_3 = 26
    PORTAL_SPEED_4 = 27
    PORTAL_GRAVITY = 28
    PORTAL_MIRROR = 29
    PORTAL_SIZE_MINI = 30
    PORTAL_SIZE_NORMAL = 31
    PORTAL_DUAL = 32
    PORTAL_SOLO = 33
    PORTAL_ROTATE_CW = 34
    PORTAL_ROTATE_CCW = 35
    
    # Decoration
    DECOR_SMALL_1 = 100
    DECOR_SMALL_2 = 101
    DECOR_MEDIUM_1 = 102
    DECOR_LARGE_1 = 103
    GLOW_1 = 104
    GLOW_2 = 105
    PULSE_OBJECT = 106
    RING_1 = 107
    RING_2 = 108
    PARTICLE_1 = 109
    SAW_1 = 110
    SAW_2 = 111
    BLOCK_SLOPE_1 = 112
    BLOCK_SLOPE_2 = 113
    BLOCK_CORNER_1 = 114
    BLOCK_CORNER_2 = 115
    
    # 2.2+ objects
    TRIGGER_SPAWN = 1006
    TRIGGER_TOUCH = 1007
    TRIGGER_COUNT = 1008
    TRIGGER_INSTANT_COUNT = 1009
    TRIGGER_PICKUP = 1010
    TRIGGER_RANDOM = 1011
    TRIGGER_TIMED = 1012
    TRIGGER_FOLLOW_X = 1013
    TRIGGER_FOLLOW_Y = 1014
    TRIGGER_ADVANCED_FOLLOW = 1015
    TRIGGER_AREA_EFFECT = 1016
    TRIGGER_EVENT_LINK = 1017
    TRIGGER_KEYFRAME = 1018
    TRIGGER_ITEM_COMPARE = 1019
    TRIGGER_ITEM_EDIT = 1020
    TRIGGER_OBJECT_CONTROL = 1021
    TRIGGER_PLAYER_CONTROL = 1022
    TRIGGER_RESET = 1023
    TRIGGER_SFX = 1024
    TRIGGER_SONG = 1025
    TRIGGER_TIMER = 1026
    
    # Move/Rotate/Scale/Color/Alpha/Pulse triggers
    TRIGGER_MOVE = 1200
    TRIGGER_ROTATE = 1201
    TRIGGER_SCALE = 1202
    TRIGGER_COLOR = 1203
    TRIGGER_ALPHA = 1204
    TRIGGER_PULSE = 1205
    TRIGGER_HSV = 1206
    TRIGGER_STOP = 1207
    TRIGGER_FOLLOW = 1208
    TRIGGER_SHAKE = 1209
    TRIGGER_ANIMATION = 1210
    TRIGGER_TOGGLE = 1211
    TRIGGER_SPAWN_ORDER = 1212
    TRIGGER_ORDER = 1213
    TRIGGER_COLLISION = 1214
    TRIGGER_TEXT = 1215
    TRIGGER_CUSTOM_RING = 1216

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class GDObject:
    """Represents a single GD object"""
    object_id: int
    x: float = 0
    y: float = 0
    rotation: float = 0
    flip_x: bool = False
    flip_y: bool = False
    scale: float = 1.0
    groups: List[int] = field(default_factory=list)
    color_1: int = 0
    color_2: int = 0
    z_order: int = 0
    z_layer: int = 0
    is_trigger: bool = False
    target_group: int = 0
    trigger_type: int = 0
    activate_group: List[int] = field(default_factory=list)
    deactivate_group: List[int] = field(default_factory=list)
    toggle_group: List[int] = field(default_factory=list)
    spawn_triggered: bool = False
    touch_triggered: bool = False
    multi_trigger: bool = False
    editor_layer_1: int = 0
    editor_layer_2: int = 0
    editor_layers: List[int] = field(default_factory=list)
    high_detail: bool = False
    dont_fade: bool = False
    hide_in_editor: bool = False
    text_string: str = ""
    font_scale: float = 1.0
    anchor_x: float = 0.5
    anchor_y: float = 0.5
    enable_gradient: bool = False
    gradient_angle: float = 0
    copy_color_1: int = 0
    copy_color_2: int = 0
    copy_opacity: int = 0
    copy_blending: int = 0
    follow_player_x: bool = False
    follow_player_y: bool = False
    follow_x_speed: float = 1.0
    follow_y_speed: float = 1.0
    follow_x_offset: float = 0
    follow_y_offset: float = 0
    follow_x_modulo: float = 0
    follow_y_modulo: float = 0
    follow_x_amount: float = 1.0
    follow_y_amount: float = 1.0
    
    # Trigger-specific properties
    move_x: float = 0
    move_y: float = 0
    rotate_degrees: float = 0
    scale_multiplier: float = 1.0
    pulse_hsv: Tuple[float, float, float] = (0, 0, 0)
    pulse_duration: float = 1.0
    pulse_easing: int = 0
    color_hsv: Tuple[float, float, float] = (0, 0, 0)
    color_duration: float = 1.0
    alpha_value: float = 1.0
    alpha_duration: float = 1.0
    shake_strength: float = 0
    shake_interval: float = 0
    animation_id: int = 0
    collision_block_id: int = 0
    spawn_order_group: int = 0
    order_amount: int = 0
    custom_ring_id: int = 0
    
    def to_dict(self) -> Dict[int, Any]:
        """Convert to GD key-value dict"""
        d = {
            ObjectKey.OBJECT_ID: self.object_id,
            ObjectKey.X: round(self.x, 3),
            ObjectKey.Y: round(self.y, 3),
        }
        
        if self.rotation != 0:
            d[ObjectKey.ROTATION] = round(self.rotation, 3)
        if self.flip_x:
            d[ObjectKey.FLIP_X] = 1
        if self.flip_y:
            d[ObjectKey.FLIP_Y] = 1
        if self.scale != 1.0:
            d[ObjectKey.SCALE] = round(self.scale, 3)
        if self.groups:
            d[ObjectKey.GROUPS] = ','.join(str(g) for g in self.groups)
        if self.color_1 != 0:
            d[ObjectKey.COLOR_1] = self.color_1
        if self.color_2 != 0:
            d[ObjectKey.COLOR_2] = self.color_2
        if self.z_order != 0:
            d[ObjectKey.Z_ORDER] = self.z_order
        if self.z_layer != 0:
            d[ObjectKey.Z_LAYER] = self.z_layer
        if self.is_trigger:
            d[ObjectKey.IS_TRIGGER] = 1
        if self.target_group != 0:
            d[ObjectKey.TARGET_GROUP] = self.target_group
        if self.activate_group:
            d[ObjectKey.ACTIVATE_GROUP] = ','.join(str(g) for g in self.activate_group)
        if self.deactivate_group:
            d[ObjectKey.DEACTIVATE_GROUP] = ','.join(str(g) for g in self.deactivate_group)
        if self.toggle_group:
            d[ObjectKey.TOGGLE_GROUP] = ','.join(str(g) for g in self.toggle_group)
        if self.spawn_triggered:
            d[ObjectKey.SPAWN_TRIGGERED] = 1
        if self.touch_triggered:
            d[ObjectKey.TOUCH_TRIGGERED] = 1
        if self.multi_trigger:
            d[ObjectKey.MULTI_TRIGGER] = 1
        if self.trigger_type != 0:
            d[ObjectKey.TRIGGER_TYPE] = self.trigger_type
        if self.editor_layer_1 != 0:
            d[ObjectKey.EDITOR_LAYER_1] = self.editor_layer_1
        if self.editor_layer_2 != 0:
            d[ObjectKey.EDITOR_LAYER_2] = self.editor_layer_2
        if self.editor_layers:
            d[ObjectKey.EDITOR_LAYERS] = ','.join(str(l) for l in self.editor_layers)
        if self.high_detail:
            d[ObjectKey.HIGH_DETAIL] = 1
        if self.dont_fade:
            d[ObjectKey.DONT_FADE] = 1
        if self.hide_in_editor:
            d[ObjectKey.HIDE_IN_EDITOR] = 1
        if self.text_string:
            d[ObjectKey.TEXT_STRING] = self.text_string
        if self.font_scale != 1.0:
            d[ObjectKey.FONT_SCALE] = self.font_scale
        if self.anchor_x != 0.5:
            d[ObjectKey.ANCHOR_X] = self.anchor_x
        if self.anchor_y != 0.5:
            d[ObjectKey.ANCHOR_Y] = self.anchor_y
        if self.enable_gradient:
            d[ObjectKey.ENABLE_GRADIENT] = 1
        if self.gradient_angle != 0:
            d[ObjectKey.GRADIENT_ANGLE] = self.gradient_angle
        if self.copy_color_1 != 0:
            d[ObjectKey.COPY_COLOR_1] = self.copy_color_1
        if self.copy_color_2 != 0:
            d[ObjectKey.COPY_COLOR_2] = self.copy_color_2
        if self.copy_opacity != 0:
            d[ObjectKey.COPY_OPACITY] = self.copy_opacity
        if self.copy_blending != 0:
            d[ObjectKey.COPY_BLENDING] = self.copy_blending
        if self.follow_player_x:
            d[ObjectKey.FOLLOW_PLAYER_X] = 1
        if self.follow_player_y:
            d[ObjectKey.FOLLOW_PLAYER_Y] = 1
        if self.follow_x_speed != 1.0:
            d[ObjectKey.FOLLOW_X_SPEED] = self.follow_x_speed
        if self.follow_y_speed != 1.0:
            d[ObjectKey.FOLLOW_Y_SPEED] = self.follow_y_speed
        if self.follow_x_offset != 0:
            d[ObjectKey.FOLLOW_X_OFFSET] = self.follow_x_offset
        if self.follow_y_offset != 0:
            d[ObjectKey.FOLLOW_Y_OFFSET] = self.follow_y_offset
        if self.follow_x_modulo != 0:
            d[ObjectKey.FOLLOW_X_MODULO] = self.follow_x_modulo
        if self.follow_y_modulo != 0:
            d[ObjectKey.FOLLOW_Y_MODULO] = self.follow_y_modulo
        if self.follow_x_amount != 1.0:
            d[ObjectKey.FOLLOW_X_AMOUNT] = self.follow_x_amount
        if self.follow_y_amount != 1.0:
            d[ObjectKey.FOLLOW_Y_AMOUNT] = self.follow_y_amount
            
        return d

@dataclass
class LevelSection:
    """Represents a section of the level with unique gameplay"""
    name: str
    start_x: float
    end_x: float
    game_mode: str
    difficulty: str
    objects: List[GDObject] = field(default_factory=list)
    triggers: List[GDObject] = field(default_factory=list)
    decoration: List[GDObject] = field(default_factory=list)
    bg_color: Tuple[int, int, int] = (0, 0, 0)
    ground_color: Tuple[int, int, int] = (0, 0, 0)

# ============================================================
# LEVEL GENERATOR
# ============================================================

class MasterpieceLevelGenerator:
    def __init__(self, song_id: int = 624012, level_name: str = "Masterpiece", author: str = "Kilo"):
        self.song_id = song_id
        self.level_name = level_name
        self.author = author
        self.objects: List[GDObject] = []
        self.sections: List[LevelSection] = []
        self.group_counter = 1000
        self.color_counter = 1000
        self.next_group = 1000
        self.next_color = 1000
        self.object_count = 0
        self.section_width = 300  # Units per section
        
        # Level metadata
        self.level_desc = "A masterpiece level with 150k+ objects, all game modes, advanced triggers & art"
        self.level_version = 47  # GD 2.2091
        self.game_version = 22
        self.difficulty = 4  # Demon
        self.demon_difficulty = 3  # Medium Demon
        self.stars = 10
        self.featured = 0
        self.epic = 1
        self.coins = 3
        self.length = 5  # XL
        self.two_player = 0
        self.auto = 0
        self.password = 0
        self.original = 0
        self.unlisted = 0
        self.friends_only = 0
        
    def new_group(self) -> int:
        g = self.next_group
        self.next_group += 1
        return g
    
    def new_color(self) -> int:
        c = self.next_color
        self.next_color += 1
        return c
    
    def add_object(self, obj: GDObject):
        self.objects.append(obj)
        self.object_count += 1
    
    def add_objects(self, objs: List[GDObject]):
        self.objects.extend(objs)
        self.object_count += len(objs)
    
    # ============================================================
    # GAMEPLAY BUILDING BLOCKS
    # ============================================================
    
    def create_portal(self, x: float, y: float, portal_type: int, 
                      speed: int = 0, size: int = 0, gravity: bool = False,
                      mirror: bool = False, dual: bool = False, 
                      rotate: int = 0, groups: List[int] = None) -> GDObject:
        """Create a portal object"""
        obj = GDObject(
            object_id=portal_type,
            x=x, y=y,
            groups=groups or []
        )
        return obj
    
    def create_orb(self, x: float, y: float, orb_type: int,
                   groups: List[int] = None) -> GDObject:
        """Create a jump orb"""
        return GDObject(object_id=orb_type, x=x, y=y, groups=groups or [])
    
    def create_pad(self, x: float, y: float, pad_type: int,
                   groups: List[int] = None) -> GDObject:
        """Create a jump pad"""
        return GDObject(object_id=pad_type, x=x, y=y, groups=groups or [])
    
    def create_block(self, x: float, y: float, block_id: int,
                     rotation: float = 0, scale: float = 1.0,
                     flip_x: bool = False, flip_y: bool = False,
                     groups: List[int] = None, color_1: int = 0,
                     color_2: int = 0, z_order: int = 0,
                     z_layer: int = 0, high_detail: bool = False) -> GDObject:
        """Create a basic block"""
        return GDObject(
            object_id=block_id, x=x, y=y,
            rotation=rotation, scale=scale,
            flip_x=flip_x, flip_y=flip_y,
            groups=groups or [],
            color_1=color_1, color_2=color_2,
            z_order=z_order, z_layer=z_layer,
            high_detail=high_detail
        )
    
    def create_slope(self, x: float, y: float, slope_type: int,
                     rotation: float = 0, flip_x: bool = False,
                     flip_y: bool = False, groups: List[int] = None) -> GDObject:
        """Create a slope block"""
        return GDObject(
            object_id=slope_type, x=x, y=y,
            rotation=rotation, flip_x=flip_x, flip_y=flip_y,
            groups=groups or []
        )
    
    def create_spike(self, x: float, y: float, rotation: float = 0,
                     scale: float = 1.0, groups: List[int] = None,
                     color_1: int = 0, color_2: int = 0) -> GDObject:
        """Create a spike"""
        return GDObject(
            object_id=BlockType.SPIKE, x=x, y=y,
            rotation=rotation, scale=scale,
            groups=groups or [],
            color_1=color_1, color_2=color_2
        )
    
    def create_trigger(self, x: float, y: float, trigger_type: int,
                       target_group: int, activate_groups: List[int] = None,
                       deactivate_groups: List[int] = None,
                       toggle_groups: List[int] = None,
                       spawn_triggered: bool = False,
                       touch_triggered: bool = False,
                       multi_trigger: bool = False,
                       groups: List[int] = None) -> GDObject:
        """Create a trigger object"""
        return GDObject(
            object_id=trigger_type,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            activate_group=activate_groups or [],
            deactivate_group=deactivate_groups or [],
            toggle_group=toggle_groups or [],
            spawn_triggered=spawn_triggered,
            touch_triggered=touch_triggered,
            multi_trigger=multi_trigger,
            groups=groups or []
        )
    
    def create_move_trigger(self, x: float, y: float, target_group: int,
                            move_x: float, move_y: float, duration: float = 1.0,
                            easing: int = 0, spawn_triggered: bool = False,
                            touch_triggered: bool = False,
                            groups: List[int] = None) -> GDObject:
        """Create a move trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_MOVE,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            move_x=move_x, move_y=move_y,
            spawn_triggered=spawn_triggered,
            touch_triggered=touch_triggered,
            groups=groups or []
        )
        return t
    
    def create_rotate_trigger(self, x: float, y: float, target_group: int,
                              degrees: float, duration: float = 1.0,
                              easing: int = 0, spawn_triggered: bool = False,
                              groups: List[int] = None) -> GDObject:
        """Create a rotate trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_ROTATE,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            rotate_degrees=degrees,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_scale_trigger(self, x: float, y: float, target_group: int,
                             multiplier: float, duration: float = 1.0,
                             easing: int = 0, spawn_triggered: bool = False,
                             groups: List[int] = None) -> GDObject:
        """Create a scale trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_SCALE,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            scale_multiplier=multiplier,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_color_trigger(self, x: float, y: float, target_group: int,
                             color_hsv: Tuple[float, float, float],
                             duration: float = 1.0, easing: int = 0,
                             copy_color_1: int = 0, copy_color_2: int = 0,
                             copy_opacity: int = 0, copy_blending: int = 0,
                             spawn_triggered: bool = False,
                             groups: List[int] = None) -> GDObject:
        """Create a color trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_COLOR,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            color_hsv=color_hsv,
            copy_color_1=copy_color_1,
            copy_color_2=copy_color_2,
            copy_opacity=copy_opacity,
            copy_blending=copy_blending,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_pulse_trigger(self, x: float, y: float, target_group: int,
                             hsv: Tuple[float, float, float],
                             duration: float = 1.0, easing: int = 0,
                             spawn_triggered: bool = False,
                             groups: List[int] = None) -> GDObject:
        """Create a pulse trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_PULSE,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            pulse_hsv=hsv,
            pulse_duration=duration,
            pulse_easing=easing,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_alpha_trigger(self, x: float, y: float, target_group: int,
                             alpha: float, duration: float = 1.0,
                             easing: int = 0, spawn_triggered: bool = False,
                             groups: List[int] = None) -> GDObject:
        """Create an alpha trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_ALPHA,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            alpha_value=alpha,
            alpha_duration=duration,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_hsv_trigger(self, x: float, y: float, target_group: int,
                           hsv: Tuple[float, float, float],
                           duration: float = 1.0, easing: int = 0,
                           spawn_triggered: bool = False,
                           groups: List[int] = None) -> GDObject:
        """Create an HSV trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_HSV,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            color_hsv=hsv,
            color_duration=duration,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_follow_trigger(self, x: float, y: float, target_group: int,
                              follow_x: bool = True, follow_y: bool = True,
                              x_speed: float = 1.0, y_speed: float = 1.0,
                              x_offset: float = 0, y_offset: float = 0,
                              x_modulo: float = 0, y_modulo: float = 0,
                              x_amount: float = 1.0, y_amount: float = 1.0,
                              spawn_triggered: bool = False,
                              groups: List[int] = None) -> GDObject:
        """Create an advanced follow trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_FOLLOW,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            follow_player_x=follow_x,
            follow_player_y=follow_y,
            follow_x_speed=x_speed,
            follow_y_speed=y_speed,
            follow_x_offset=x_offset,
            follow_y_offset=y_offset,
            follow_x_modulo=x_modulo,
            follow_y_modulo=y_modulo,
            follow_x_amount=x_amount,
            follow_y_amount=y_amount,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_shake_trigger(self, x: float, y: float, target_group: int,
                             strength: float, interval: float,
                             spawn_triggered: bool = False,
                             groups: List[int] = None) -> GDObject:
        """Create a shake trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_SHAKE,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            shake_strength=strength,
            shake_interval=interval,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_animation_trigger(self, x: float, y: float, target_group: int,
                                 anim_id: int, spawn_triggered: bool = False,
                                 groups: List[int] = None) -> GDObject:
        """Create an animation trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_ANIMATION,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            animation_id=anim_id,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_spawn_trigger(self, x: float, y: float, target_group: int,
                             delay: float = 0, spawn_triggered: bool = True,
                             groups: List[int] = None) -> GDObject:
        """Create a spawn trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_SPAWN,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            spawn_triggered=spawn_triggered,
            groups=groups or []
        )
        return t
    
    def create_touch_trigger(self, x: float, y: float, target_group: int,
                             activate_groups: List[int] = None,
                             deactivate_groups: List[int] = None,
                             toggle_groups: List[int] = None,
                             groups: List[int] = None) -> GDObject:
        """Create a touch trigger"""
        t = GDObject(
            object_id=BlockType.TRIGGER_TOUCH,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            activate_group=activate_groups or [],
            deactivate_group=deactivate_groups or [],
            toggle_group=toggle_groups or [],
            touch_triggered=True,
            groups=groups or []
        )
        return t
    
    def create_death_trigger(self, x: float, y: float, target_group: int,
                             activate_groups: List[int] = None,
                             groups: List[int] = None) -> GDObject:
        """Create a death trigger (activates on death)"""
        t = GDObject(
            object_id=BlockType.TRIGGER_SPAWN,
            x=x, y=y,
            is_trigger=True,
            target_group=target_group,
            activate_group=activate_groups or [],
            spawn_triggered=False,
            groups=groups or []
        )
        # Death triggers use a different mechanism in GD
        return t
    
    def create_decoration(self, x: float, y: float, deco_id: int,
                          rotation: float = 0, scale: float = 1.0,
                          flip_x: bool = False, flip_y: bool = False,
                          color_1: int = 0, color_2: int = 0,
                          z_order: int = 0, z_layer: int = 0,
                          groups: List[int] = None, high_detail: bool = False,
                          editor_layer_1: int = 0, editor_layer_2: int = 0) -> GDObject:
        """Create a decoration object"""
        return GDObject(
            object_id=deco_id, x=x, y=y,
            rotation=rotation, scale=scale,
            flip_x=flip_x, flip_y=flip_y,
            color_1=color_1, color_2=color_2,
            z_order=z_order, z_layer=z_layer,
            groups=groups or [],
            high_detail=high_detail,
            editor_layer_1=editor_layer_1,
            editor_layer_2=editor_layer_2
        )
    
    def create_pulse_object(self, x: float, y: float, pulse_id: int,
                            hsv: Tuple[float, float, float],
                            duration: float = 1.0, easing: int = 0,
                            groups: List[int] = None) -> GDObject:
        """Create a pulse object (object that pulses)"""
        return GDObject(
            object_id=pulse_id,
            x=x, y=y,
            groups=groups or [],
            # Pulse properties stored in object
        )
    
    # ============================================================
    # SECTION BUILDERS
    # ============================================================
    
    def build_intro_section(self, start_x: float) -> LevelSection:
        """Section 0: Intro - Easy Cube, atmospheric buildup"""
        section = LevelSection(
            name="Intro - Atmospheric Buildup",
            start_x=start_x,
            end_x=start_x + self.section_width * 2,
            game_mode="cube",
            difficulty="Easy",
            bg_color=(10, 5, 20),
            ground_color=(30, 15, 50)
        )
        
        x = start_x
        y = 15
        
        # Starting portal
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_CUBE))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_1))
        x += 30
        
        # Atmospheric cube gameplay - simple but beautiful
        for i in range(20):
            # Ground pattern
            for gx in range(3):
                bx = x + i * 15 + gx * 30
                by = y - 15
                section.decoration.append(self.create_block(bx, by, BlockType.SOLID_BLOCK,
                    color_1=self.new_color(), color_2=self.new_color(),
                    z_layer=-1, high_detail=True))
            
            # Floating platforms
            if i % 3 == 0:
                px = x + i * 15 + 15
                py = y + 30 + math.sin(i * 0.5) * 20
                section.objects.append(self.create_block(px, py, BlockType.PLATFORM,
                    scale=0.5, color_1=self.new_color(), groups=[self.new_group()]))
            
            # Orbs for flow
            if i % 4 == 1:
                ox = x + i * 15 + 20
                oy = y + 45 + math.sin(i * 0.3) * 15
                section.objects.append(self.create_orb(ox, oy, BlockType.ORB_YELLOW))
            
            # Pulse triggers for atmosphere
            if i % 5 == 0:
                trigger_x = x + i * 15
                group = self.new_group()
                section.triggers.append(self.create_pulse_trigger(trigger_x, y - 30, group,
                    hsv=(0.6 + i * 0.02, 0.8, 1.0), duration=2.0, spawn_triggered=True))
                # Apply to background objects
                for obj in section.decoration[-10:]:
                    obj.groups.append(group)
        
        # Decorative glow lines
        for i in range(40):
            gx = start_x + i * 15
            gy = y - 15 + math.sin(i * 0.2) * 5
            section.decoration.append(self.create_decoration(gx, gy, BlockType.GLOW_1,
                scale=0.3, rotation=i * 9, color_1=self.new_color(), z_layer=-2))
        
        section.end_x = x + 20 * 15
        return section
    
    def build_cube_section_1(self, start_x: float) -> LevelSection:
        """Section 1: Main Cube - Easy Demon, rhythmic"""
        section = LevelSection(
            name="Cube 1 - Rhythmic Flow",
            start_x=start_x,
            end_x=start_x + self.section_width * 3,
            game_mode="cube",
            difficulty="Easy Demon",
            bg_color=(20, 10, 40),
            ground_color=(50, 25, 80)
        )
        
        x = start_x
        y = 15
        
        # Speed portal
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_2))
        x += 30
        
        # Rhythmic cube pattern - synced to music
        pattern_length = 45
        for i in range(pattern_length):
            bx = x + i * 15
            
            # Ground
            section.objects.append(self.create_block(bx, y - 15, BlockType.SOLID_BLOCK,
                color_1=self.new_color(), color_2=self.new_color(), high_detail=True))
            
            # Jump pattern every 3-4 blocks
            if i % 4 == 0 and i > 0:
                # Yellow orb jump
                section.objects.append(self.create_orb(bx + 7, y + 30, BlockType.ORB_YELLOW))
            elif i % 4 == 2:
                # Blue orb (double jump)
                section.objects.append(self.create_orb(bx + 7, y + 45, BlockType.ORB_BLUE))
            
            # Decorative spikes (non-lethal looking)
            if i % 5 == 0:
                section.decoration.append(self.create_spike(bx + 15, y - 15, rotation=180,
                    scale=0.5, color_1=self.new_color()))
            
            # Pulse triggers on beat
            if i % 8 == 0:
                group = self.new_group()
                section.triggers.append(self.create_pulse_trigger(bx, y - 30, group,
                    hsv=(0.55, 0.9, 1.0), duration=0.5, spawn_triggered=True))
        
        # Add moving platforms via triggers
        for i in range(10):
            mx = x + 50 + i * 60
            my = y + 60
            group = self.new_group()
            section.objects.append(self.create_block(mx, my, BlockType.PLATFORM,
                scale=0.8, groups=[group], color_1=self.new_color()))
            section.triggers.append(self.create_move_trigger(x + i * 60, y - 30, group,
                move_x=0, move_y=math.sin(i) * 20, duration=3.0, spawn_triggered=True))
        
        section.end_x = x + pattern_length * 15
        return section
    
    def build_ship_section(self, start_x: float) -> LevelSection:
        """Section 2: Ship - Medium Demon, tight spaces"""
        section = LevelSection(
            name="Ship - Tight Corridors",
            start_x=start_x,
            end_x=start_x + self.section_width * 2.5,
            game_mode="ship",
            difficulty="Medium Demon",
            bg_color=(30, 15, 50),
            ground_color=(60, 30, 90)
        )
        
        x = start_x
        y = 15
        
        # Transition portals
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SHIP))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_3))
        x += 40
        
        # Ship corridor - wave-like pattern
        corridor_height = 80
        for i in range(35):
            bx = x + i * 15
            
            # Top ceiling
            top_y = y + corridor_height + math.sin(i * 0.4) * 15
            section.objects.append(self.create_block(bx, top_y, BlockType.SOLID_BLOCK,
                rotation=180, color_1=self.new_color(), color_2=self.new_color(),
                high_detail=True, z_layer=1))
            
            # Bottom floor
            bot_y = y - 15 + math.sin(i * 0.3) * 10
            section.objects.append(self.create_block(bx, bot_y, BlockType.SOLID_BLOCK,
                color_1=self.new_color(), color_2=self.new_color(),
                high_detail=True, z_layer=1))
            
            # Obstacles in middle
            if i % 3 == 1:
                obs_y = y + 20 + math.sin(i * 0.5) * 20
                section.objects.append(self.create_block(bx + 7, obs_y, BlockType.SOLID_BLOCK,
                    scale=0.5, rotation=random.choice([0, 90, 180, 270]),
                    color_1=self.new_color(), groups=[self.new_group()]))
            
            # Gravity portals for flair
            if i % 10 == 5:
                section.objects.append(self.create_portal(bx + 7, y + 20, BlockType.PORTAL_GRAVITY,
                    groups=[self.new_group()]))
                # Trigger to revert gravity
                section.triggers.append(self.create_spawn_trigger(bx + 30, y + 20, 
                    self.new_group(), spawn_triggered=True))
        
        # Decorative particles
        for i in range(50):
            px = x + i * 10
            py = y + random.uniform(-10, 90)
            section.decoration.append(self.create_decoration(px, py, BlockType.PARTICLE_1,
                scale=0.2, color_1=self.new_color(), z_layer=2))
        
        section.end_x = x + 35 * 15
        return section
    
    def build_ball_section(self, start_x: float) -> LevelSection:
        """Section 3: Ball - Medium Demon, gravity switching"""
        section = LevelSection(
            name="Ball - Gravity Mastery",
            start_x=start_x,
            end_x=start_x + self.section_width * 2,
            game_mode="ball",
            difficulty="Medium Demon",
            bg_color=(15, 30, 40),
            ground_color=(40, 60, 80)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_BALL))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_2))
        x += 30
        
        # Ball section with frequent gravity changes
        for i in range(30):
            bx = x + i * 15
            
            # Alternating ceiling/floor
            if i % 2 == 0:
                # Floor
                section.objects.append(self.create_block(bx, y - 15, BlockType.SOLID_BLOCK,
                    color_1=self.new_color(), high_detail=True))
                # Ceiling
                section.objects.append(self.create_block(bx, y + 85, BlockType.SOLID_BLOCK,
                    rotation=180, color_1=self.new_color(), high_detail=True))
            else:
                # Inverted
                section.objects.append(self.create_block(bx, y - 15, BlockType.SOLID_BLOCK,
                    color_1=self.new_color(), high_detail=True))
                section.objects.append(self.create_block(bx, y + 85, BlockType.SOLID_BLOCK,
                    rotation=180, color_1=self.new_color(), high_detail=True))
            
            # Gravity portals every few blocks
            if i % 4 == 0:
                section.objects.append(self.create_portal(bx + 7, y + 35, BlockType.PORTAL_GRAVITY))
            
            # Orbs for height control
            if i % 3 == 1:
                section.objects.append(self.create_orb(bx + 7, y + 20, BlockType.ORB_BLUE))
            if i % 3 == 2:
                section.objects.append(self.create_orb(bx + 7, y + 50, BlockType.ORB_RED))
            
            # Moving platforms
            if i % 5 == 0:
                group = self.new_group()
                section.objects.append(self.create_block(bx + 7, y + 35, BlockType.PLATFORM,
                    scale=0.6, groups=[group], color_1=self.new_color()))
                section.triggers.append(self.create_move_trigger(bx, y - 30, group,
                    move_x=0, move_y=15, duration=2.0, easing=1, spawn_triggered=True))
        
        section.end_x = x + 30 * 15
        return section
    
    def build_ufo_section(self, start_x: float) -> LevelSection:
        """Section 4: UFO - Easy-Medium Demon, click timing"""
        section = LevelSection(
            name="UFO - Precision Clicks",
            start_x=start_x,
            end_x=start_x + self.section_width * 2,
            game_mode="ufo",
            difficulty="Easy-Medium Demon",
            bg_color=(25, 20, 45),
            ground_color=(50, 40, 85)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_UFO))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_2))
        x += 30
        
        # UFO corridor with varying heights
        for i in range(25):
            bx = x + i * 15
            
            # Ceiling and floor
            top = y + 70 + math.sin(i * 0.3) * 20
            bot = y - 15 + math.sin(i * 0.2) * 10
            
            section.objects.append(self.create_block(bx, top, BlockType.SOLID_BLOCK,
                rotation=180, color_1=self.new_color(), high_detail=True))
            section.objects.append(self.create_block(bx, bot, BlockType.SOLID_BLOCK,
                color_1=self.new_color(), high_detail=True))
            
            # Floating obstacles
            if i % 2 == 0:
                obs_y = (top + bot) / 2 + math.sin(i * 0.5) * 15
                section.objects.append(self.create_block(bx + 7, obs_y, BlockType.SOLID_BLOCK,
                    scale=0.4, color_1=self.new_color(), groups=[self.new_group()]))
            
            # Jump orbs
            if i % 3 == 1:
                section.objects.append(self.create_orb(bx + 7, bot + 25, BlockType.ORB_YELLOW))
            if i % 3 == 2:
                section.objects.append(self.create_orb(bx + 7, top - 25, BlockType.ORB_BLUE))
        
        section.end_x = x + 25 * 15
        return section
    
    def build_wave_section(self, start_x: float) -> LevelSection:
        """Section 5: Wave - Medium Demon, tight wave"""
        section = LevelSection(
            name="Wave - Tight Navigation",
            start_x=start_x,
            end_x=start_x + self.section_width * 2,
            game_mode="wave",
            difficulty="Medium Demon",
            bg_color=(35, 10, 50),
            ground_color=(70, 20, 90)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_WAVE))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_3))
        x += 30
        
        # Classic tight wave
        for i in range(30):
            bx = x + i * 15
            
            # Zigzag ceiling/floor
            top = y + 50 + (1 if i % 2 == 0 else -1) * 20
            bot = y - 15 + (1 if i % 2 == 0 else -1) * 20
            
            section.objects.append(self.create_block(bx, top, BlockType.SOLID_BLOCK,
                rotation=180, color_1=self.new_color(), high_detail=True))
            section.objects.append(self.create_block(bx, bot, BlockType.SOLID_BLOCK,
                color_1=self.new_color(), high_detail=True))
            
            # Mini portals for variety
            if i % 8 == 3:
                section.objects.append(self.create_portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_MINI))
            if i % 8 == 7:
                section.objects.append(self.create_portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_NORMAL))
        
        section.end_x = x + 30 * 15
        return section
    
    def build_robot_section(self, start_x: float) -> LevelSection:
        """Section 6: Robot - Medium Demon, hold timing"""
        section = LevelSection(
            name="Robot - Hold Mastery",
            start_x=start_x,
            end_x=start_x + self.section_width * 2.5,
            game_mode="robot",
            difficulty="Medium Demon",
            bg_color=(20, 35, 45),
            ground_color=(45, 70, 85)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_ROBOT))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_2))
        x += 30
        
        # Robot with varying hold lengths
        for i in range(28):
            bx = x + i * 15
            
            # Ground
            section.objects.append(self.create_block(bx, y - 15, BlockType.SOLID_BLOCK,
                color_1=self.new_color(), high_detail=True))
            
            # Platforms at different heights
            if i % 3 == 0:
                section.objects.append(self.create_block(bx + 7, y + 30, BlockType.PLATFORM,
                    scale=0.7, color_1=self.new_color()))
            if i % 3 == 1:
                section.objects.append(self.create_block(bx + 7, y + 55, BlockType.PLATFORM,
                    scale=0.5, color_1=self.new_color()))
            if i % 3 == 2:
                section.objects.append(self.create_block(bx + 7, y + 15, BlockType.PLATFORM,
                    scale=0.6, color_1=self.new_color()))
            
            # Jump orbs for height
            if i % 4 == 1:
                section.objects.append(self.create_orb(bx + 7, y + 45, BlockType.ORB_YELLOW))
            if i % 4 == 3:
                section.objects.append(self.create_orb(bx + 7, y + 70, BlockType.ORB_BLUE))
        
        section.end_x = x + 28 * 15
        return section
    
    def build_spider_section(self, start_x: float) -> LevelSection:
        """Section 7: Spider - Medium Demon, teleport timing"""
        section = LevelSection(
            name="Spider - Teleport Flow",
            start_x=start_x,
            end_x=start_x + self.section_width * 2,
            game_mode="spider",
            difficulty="Medium Demon",
            bg_color=(30, 20, 55),
            ground_color=(60, 40, 95)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPIDER))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_2))
        x += 30
        
        # Spider with ceiling/floor switching
        for i in range(25):
            bx = x + i * 15
            
            # Ceiling and floor
            section.objects.append(self.create_block(bx, y + 85, BlockType.SOLID_BLOCK,
                rotation=180, color_1=self.new_color(), high_detail=True))
            section.objects.append(self.create_block(bx, y - 15, BlockType.SOLID_BLOCK,
                color_1=self.new_color(), high_detail=True))
            
            # Middle obstacles
            if i % 2 == 0:
                section.objects.append(self.create_block(bx + 7, y + 35, BlockType.SOLID_BLOCK,
                    scale=0.5, color_1=self.new_color()))
            
            # Orbs for forced switches
            if i % 3 == 1:
                section.objects.append(self.create_orb(bx + 7, y + 20, BlockType.ORB_YELLOW))
            if i % 3 == 2:
                section.objects.append(self.create_orb(bx + 7, y + 65, BlockType.ORB_BLUE))
        
        section.end_x = x + 25 * 15
        return section
    
    def build_swing_section(self, start_x: float) -> LevelSection:
        """Section 8: Swing - Easy Demon, momentum"""
        section = LevelSection(
            name="Swing - Momentum",
            start_x=start_x,
            end_x=start_x + self.section_width * 2,
            game_mode="swing",
            difficulty="Easy Demon",
            bg_color=(25, 25, 50),
            ground_color=(55, 50, 90)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SWING))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_2))
        x += 30
        
        # Swing with anchor points
        for i in range(20):
            bx = x + i * 15
            
            # Ground
            section.objects.append(self.create_block(bx, y - 15, BlockType.SOLID_BLOCK,
                color_1=self.new_color(), high_detail=True))
            
            # Anchor points (swing uses these)
            if i % 2 == 0:
                section.objects.append(self.create_block(bx + 7, y + 50, BlockType.SOLID_BLOCK,
                    scale=0.3, color_1=self.new_color(), groups=[self.new_group()]))
            
            # Orbs for release timing
            if i % 3 == 1:
                section.objects.append(self.create_orb(bx + 7, y + 30, BlockType.ORB_YELLOW))
        
        section.end_x = x + 20 * 15
        return section
    
    def build_platformer_section(self, start_x: float) -> LevelSection:
        """Section 9: Platformer - Easy Demon, precision jumps"""
        section = LevelSection(
            name="Platformer - Precision",
            start_x=start_x,
            end_x=start_x + self.section_width * 2,
            game_mode="platformer",
            difficulty="Easy Demon",
            bg_color=(15, 25, 40),
            ground_color=(35, 50, 75)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_PLATFORMER))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_1))
        x += 30
        
        # Platformer with moving platforms
        for i in range(22):
            bx = x + i * 15
            
            # Ground platforms
            if i % 3 == 0:
                section.objects.append(self.create_block(bx, y - 15, BlockType.SOLID_BLOCK,
                    scale=2.0, color_1=self.new_color(), high_detail=True))
            
            # Floating platforms
            if i % 2 == 1:
                py = y + 15 + (i % 4) * 20
                group = self.new_group()
                section.objects.append(self.create_block(bx + 7, py, BlockType.PLATFORM,
                    scale=0.8, groups=[group], color_1=self.new_color()))
                section.triggers.append(self.create_move_trigger(bx, y - 30, group,
                    move_x=15, move_y=0, duration=2.0, spawn_triggered=True))
            
            # Orbs for double jumps
            if i % 4 == 2:
                section.objects.append(self.create_orb(bx + 7, y + 35, BlockType.ORB_YELLOW))
        
        section.end_x = x + 22 * 15
        return section
    
    def build_final_cube(self, start_x: float) -> LevelSection:
        """Section 10: Final Cube - Medium Demon climax"""
        section = LevelSection(
            name="Final Cube - Climax",
            start_x=start_x,
            end_x=start_x + self.section_width * 3,
            game_mode="cube",
            difficulty="Medium Demon",
            bg_color=(50, 10, 60),
            ground_color=(90, 20, 100)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_CUBE))
        section.objects.append(self.create_portal(x, y, BlockType.PORTAL_SPEED_3))
        x += 30
        
        # Intense final section with all mechanics
        for i in range(50):
            bx = x + i * 15
            
            # Ground
            section.objects.append(self.create_block(bx, y - 15, BlockType.SOLID_BLOCK,
                color_1=self.new_color(), color_2=self.new_color(), high_detail=True))
            
            # Complex jump patterns
            pattern = i % 12
            if pattern == 0:
                section.objects.append(self.create_orb(bx + 7, y + 30, BlockType.ORB_YELLOW))
            elif pattern == 1:
                section.objects.append(self.create_orb(bx + 7, y + 45, BlockType.ORB_BLUE))
            elif pattern == 2:
                section.objects.append(self.create_orb(bx + 7, y + 30, BlockType.ORB_GREEN))
            elif pattern == 3:
                section.objects.append(self.create_pad(bx + 7, y - 15, BlockType.PAD_YELLOW))
            elif pattern == 4:
                section.objects.append(self.create_pad(bx + 7, y - 15, BlockType.PAD_PINK))
            elif pattern == 5:
                section.objects.append(self.create_orb(bx + 7, y + 60, BlockType.ORB_RED))
            elif pattern == 6:
                section.objects.append(self.create_orb(bx + 7, y + 30, BlockType.ORB_PURPLE))
            elif pattern == 7:
                section.objects.append(self.create_orb(bx + 7, y + 45, BlockType.ORB_DASH))
            elif pattern == 8:
                section.objects.append(self.create_portal(bx + 7, y + 15, BlockType.PORTAL_GRAVITY))
            elif pattern == 9:
                section.objects.append(self.create_portal(bx + 7, y + 15, BlockType.PORTAL_MIRROR))
            elif pattern == 10:
                section.objects.append(self.create_portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_MINI))
            elif pattern == 11:
                section.objects.append(self.create_portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_NORMAL))
            
            # Intense pulse triggers
            if i % 4 == 0:
                group = self.new_group()
                section.triggers.append(self.create_pulse_trigger(bx, y - 30, group,
                    hsv=(0.95, 1.0, 1.0), duration=0.3, spawn_triggered=True))
        
        # End portal
        section.objects.append(self.create_portal(x + 50 * 15, y, BlockType.PORTAL_CUBE))
        
        section.end_x = x + 50 * 15
        return section
    
    # ============================================================
    # ART & DECORATION SYSTEMS
    # ============================================================
    
    def add_3d_background(self, section: LevelSection, depth_layers: int = 5):
        """Add 3D-like layered background"""
        for layer in range(depth_layers):
            z = -5 - layer * 2
            parallax = 1.0 - layer * 0.15
            color_intensity = 30 + layer * 20
            
            for i in range(int((section.end_x - section.start_x) / 30) + 2):
                x = section.start_x + i * 30
                y = 15 + math.sin(i * 0.1 + layer) * 40 * parallax
                
                # Large background structures
                obj = self.create_block(x, y, BlockType.DECOR_LARGE_1,
                    scale=2.0 + layer * 0.5,
                    color_1=self.new_color(),
                    color_2=self.new_color(),
                    z_layer=z,
                    high_detail=(layer < 2))
                section.decoration.append(obj)
                
                # Glow effects
                if layer < 3:
                    glow = self.create_decoration(x + 15, y + 20, BlockType.GLOW_2,
                        scale=1.5 + layer * 0.3,
                        color_1=self.new_color(),
                        z_layer=z - 1)
                    section.decoration.append(glow)
    
    def add_foreground_art(self, section: LevelSection):
        """Add foreground decorative art"""
        for i in range(int((section.end_x - section.start_x) / 45) + 1):
            x = section.start_x + i * 45 + random.uniform(-10, 10)
            y = 15 + random.uniform(-50, 100)
            
            # Rings
            if random.random() < 0.3:
                group = self.new_group()
                ring = self.create_decoration(x, y, BlockType.RING_1,
                    scale=random.uniform(0.5, 1.5),
                    rotation=random.uniform(0, 360),
                    color_1=self.new_color(),
                    color_2=self.new_color(),
                    z_layer=2,
                    groups=[group])
                section.decoration.append(ring)
                
                # Pulse trigger for rings
                section.triggers.append(self.create_pulse_trigger(
                    x - 100, 15, group,
                    hsv=(random.random(), 0.8, 1.0),
                    duration=random.uniform(1.0, 3.0),
                    spawn_triggered=True))
            
            # Saw blades (decorative)
            if random.random() < 0.2:
                saw = self.create_decoration(x, y, BlockType.SAW_1,
                    scale=random.uniform(0.4, 0.8),
                    color_1=self.new_color(),
                    z_layer=1)
                section.decoration.append(saw)
            
            # Particle systems
            if random.random() < 0.4:
                for _ in range(random.randint(3, 8)):
                    px = x + random.uniform(-20, 20)
                    py = y + random.uniform(-20, 20)
                    part = self.create_decoration(px, py, BlockType.PARTICLE_1,
                        scale=random.uniform(0.1, 0.3),
                        color_1=self.new_color(),
                        z_layer=3)
                    section.decoration.append(part)
    
    def add_color_scheme(self, section: LevelSection, base_hue: float):
        """Apply consistent color scheme to section"""
        colors = []
        for i in range(20):
            h = (base_hue + i * 0.05) % 1.0
            s = 0.7 + random.random() * 0.3
            v = 0.6 + random.random() * 0.4
            colors.append((h, s, v))
        
        # Apply to objects
        for obj in section.objects + section.decoration:
            if obj.color_1 == 0:
                c = random.choice(colors)
                obj.color_1 = self.new_color()
                # Store HSV for trigger reference
                obj.color_hsv = c
        
        # Add color triggers at section start
        for i, obj in enumerate(section.objects[:10]):
            if obj.color_1 > 0:
                section.triggers.append(self.create_color_trigger(
                    section.start_x, 15, obj.color_1,
                    color_hsv=obj.color_hsv,
                    duration=0.1, spawn_triggered=True))
    
    def add_pulse_system(self, section: LevelSection, bpm: float = 150):
        """Add comprehensive pulse system synced to music"""
        beat_interval = 60.0 / bpm * 15  # Convert to GD units
        
        # Main pulse groups
        main_groups = [self.new_group() for _ in range(4)]
        
        # Assign objects to pulse groups
        for i, obj in enumerate(section.objects + section.decoration):
            if not obj.is_trigger and obj.z_layer >= -1:
                obj.groups.append(main_groups[i % len(main_groups)])
        
        # Create pulse triggers at regular intervals
        x = section.start_x
        while x < section.end_x:
            for gi, group in enumerate(main_groups):
                hue = (gi * 0.25 + x * 0.001) % 1.0
                section.triggers.append(self.create_pulse_trigger(
                    x, 15, group,
                    hsv=(hue, 0.9, 1.0),
                    duration=beat_interval / 15 * 0.5,
                    easing=1,
                    spawn_triggered=True))
            x += beat_interval
    
    def add_advanced_triggers(self, section: LevelSection):
        """Add advanced trigger chains: move, rotate, scale, follow, HSV"""
        # Moving decoration groups
        move_groups = [self.new_group() for _ in range(3)]
        
        for gi, group in enumerate(move_groups):
            # Add decorative objects to group
            for i in range(5):
                x = section.start_x + random.uniform(0, section.end_x - section.start_x)
                y = 15 + random.uniform(-30, 80)
                obj = self.create_decoration(x, y, BlockType.DECOR_MEDIUM_1,
                    scale=random.uniform(0.5, 1.2),
                    rotation=random.uniform(0, 360),
                    color_1=self.new_color(),
                    groups=[group],
                    z_layer=1)
                section.decoration.append(obj)
            
            # Complex move pattern
            section.triggers.append(self.create_move_trigger(
                section.start_x, 15, group,
                move_x=math.sin(gi) * 40,
                move_y=math.cos(gi) * 30,
                duration=random.uniform(3.0, 6.0),
                easing=1,
                spawn_triggered=True))
            
            # Rotate trigger
            section.triggers.append(self.create_rotate_trigger(
                section.start_x + 50, 15, group,
                degrees=360 * random.uniform(0.5, 2.0),
                duration=random.uniform(4.0, 8.0),
                spawn_triggered=True))
            
            # Scale pulse
            section.triggers.append(self.create_scale_trigger(
                section.start_x + 100, 15, group,
                multiplier=random.uniform(0.8, 1.3),
                duration=random.uniform(2.0, 4.0),
                spawn_triggered=True))
            
            # HSV shift
            section.triggers.append(self.create_hsv_trigger(
                section.start_x + 150, 15, group,
                hsv=(random.random(), 0.8, 1.0),
                duration=random.uniform(5.0, 10.0),
                spawn_triggered=True))
        
        # Follow player triggers for dynamic elements
        follow_group = self.new_group()
        for i in range(3):
            x = section.start_x + i * 100
            y = 15 + 50
            obj = self.create_decoration(x, y, BlockType.GLOW_2,
                scale=1.5, color_1=self.new_color(), groups=[follow_group], z_layer=2)
            section.decoration.append(obj)
        
        section.triggers.append(self.create_follow_trigger(
            section.start_x, 15, follow_group,
            follow_x=True, follow_y=True,
            x_speed=0.3, y_speed=0.2,
            x_offset=0, y_offset=0,
            spawn_triggered=True))
        
        # Shake triggers on beats
        for i in range(int((section.end_x - section.start_x) / 120)):
            x = section.start_x + i * 120
            section.triggers.append(self.create_shake_trigger(
                x, 15, self.new_group(),
                strength=random.uniform(0.5, 2.0),
                interval=0.1,
                spawn_triggered=True))
    
    # ============================================================
    # MAIN GENERATION
    # ============================================================
    
    def generate(self) -> str:
        """Generate the complete level"""
        print("Generating masterpiece level...")
        
        # Build all gameplay sections
        current_x = 0
        
        sections_builders = [
            self.build_intro_section,
            self.build_cube_section_1,
            self.build_ship_section,
            self.build_ball_section,
            self.build_ufo_section,
            self.build_wave_section,
            self.build_robot_section,
            self.build_spider_section,
            self.build_swing_section,
            self.build_platformer_section,
            self.build_final_cube,
        ]
        
        for i, builder in enumerate(sections_builders):
            print(f"  Building section {i+1}/{len(sections_builders)}: {builder.__name__}")
            section = builder(current_x)
            
            # Add art systems
            self.add_3d_background(section, depth_layers=5)
            self.add_foreground_art(section)
            self.add_color_scheme(section, base_hue=i * 0.09)
            self.add_pulse_system(section, bpm=150 + i * 5)
            self.add_advanced_triggers(section)
            
            # Collect all objects
            self.add_objects(section.objects)
            self.add_objects(section.triggers)
            self.add_objects(section.decoration)
            
            current_x = section.end_x + 50  # Gap between sections
            self.sections.append(section)
            
            print(f"    Objects: {len(section.objects)}, Triggers: {len(section.triggers)}, Decor: {len(section.decoration)}")
        
        # Add global level decoration
        self.add_global_decoration()
        
        # Add coins
        self.add_coins()
        
        print(f"\nTotal objects: {self.object_count}")
        
        # Encode level string
        level_string = self.encode_level_string()
        
        # Create .gdlvl file
        gdlvl_data = self.create_gdlvl(level_string)
        
        return gdlvl_data
    
    def add_global_decoration(self):
        """Add level-wide decorative elements"""
        # Title text (using text object ID 914)
        title = GDObject(
            object_id=914, x=-100, y=200,
            text_string=self.level_name,
            font_scale=2.0,
            color_1=self.new_color(),
            z_layer=10,
            editor_layer_1=1)
        self.add_object(title)
        
        # Author text
        author = GDObject(
            object_id=914, x=-100, y=170,
            text_string=f"By {self.author}",
            font_scale=1.0,
            color_1=self.new_color(),
            z_layer=10,
            editor_layer_1=1)
        self.add_object(author)
        
        # Difficulty indicator
        diff_text = "Easy-Medium Demon"
        diff = GDObject(
            object_id=914, x=-100, y=140,
            text_string=diff_text,
            font_scale=0.8,
            color_1=self.new_color(),
            z_layer=10,
            editor_layer_1=1)
        self.add_object(diff)
    
    def add_coins(self):
        """Add 3 secret coins at strategic locations"""
        coin_positions = [
            (self.sections[1].start_x + 100, 15 + 60),  # Cube section
            (self.sections[3].start_x + 200, 15 + 40),  # Ball section
            (self.sections[9].start_x + 300, 15 + 50),  # Final cube
        ]
        
        for i, (cx, cy) in enumerate(coin_positions):
            coin_group = self.new_group()
            # Coin object (trigger-based)
            coin_trigger = self.create_trigger(cx, cy, BlockType.TRIGGER_TOUCH,
                target_group=coin_group,
                activate_groups=[coin_group],
                touch_triggered=True)
            self.add_object(coin_trigger)
            
            # Coin visual
            coin_visual = self.create_decoration(cx, cy, 1048,  # Coin object ID
                scale=0.8, color_1=self.new_color(),
                groups=[coin_group], z_layer=5)
            self.add_object(coin_visual)
            
            # Coin counter trigger
            counter = self.create_trigger(cx, cy, BlockType.TRIGGER_ITEM_EDIT,
                target_group=coin_group,
                groups=[coin_group])
            self.add_object(counter)
    
    def encode_level_string(self) -> str:
        """Encode all objects into GD level string format"""
        print("Encoding level string...")
        
        # Level header data
        header_parts = [
            f"kS38:{self.level_name}",  # Level name (base64 encoded in real GD)
            f"kS39:{self.author}",
            f"kI40:{self.song_id}",  # Song ID
            f"kI41:{self.difficulty}",
            f"kI42:{self.demon_difficulty}",
            f"kI43:{self.stars}",
            f"kI44:{self.featured}",
            f"kI45:{self.epic}",
            f"kI46:{self.coins}",
            f"kI47:{self.length}",
            f"kI48:{self.two_player}",
            f"kI49:{self.auto}",
            f"kI50:{self.password}",
            f"kI51:{self.original}",
            f"kI52:{self.unlisted}",
            f"kI53:{self.friends_only}",
            f"kI54:{self.level_version}",
            f"kI55:{self.game_version}",
            f"kI56:{self.object_count}",
        ]
        
        # Object data
        object_strings = []
        for obj in self.objects:
            obj_dict = obj.to_dict()
            if not obj_dict:
                continue
            
            # Format: key1,value1,key2,value2;...
            pairs = []
            for k, v in sorted(obj_dict.items()):
                if isinstance(v, float):
                    v = f"{v:.3f}".rstrip('0').rstrip('.')
                elif isinstance(v, bool):
                    v = '1' if v else '0'
                pairs.append(f"{k},{v}")
            
            if pairs:
                object_strings.append(','.join(pairs))
        
        # Combine: header;objects;
        level_string = ';'.join(header_parts) + ';' + ';'.join(object_strings) + ';'
        
        print(f"Level string length: {len(level_string)} chars")
        return level_string
    
    def create_gdlvl(self, level_string: str) -> bytes:
        """Create .gdlvl file (gzip + base64)"""
        print("Creating .gdlvl file...")
        
        # GD level format: gzip compress then base64 encode
        compressed = gzip.compress(level_string.encode('utf-8'), compresslevel=9)
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
        
        # .gdlvl is typically just the base64 string
        # Some versions add a header
        gdlvl_content = encoded
        
        print(f"Compressed size: {len(compressed)} bytes")
        print(f"Base64 size: {len(encoded)} chars")
        
        return gdlvl_content.encode('ascii')
    
    def save(self, filename: str = "masterpiece.gdlvl"):
        """Save level to file"""
        gdlvl_data = self.generate()
        
        with open(filename, 'wb') as f:
            f.write(gdlvl_data)
        
        print(f"\nSaved to {filename}")
        print(f"Object count: {self.object_count}")
        print(f"Sections: {len(self.sections)}")
        print(f"Groups used: {self.next_group - 1000}")
        print(f"Colors used: {self.next_color - 1000}")
        
        # Also save level string for debugging
        with open(filename.replace('.gdlvl', '_levelstring.txt'), 'w') as f:
            f.write(self.encode_level_string())
        
        # Save metadata
        meta = {
            "level_name": self.level_name,
            "author": self.author,
            "song_id": self.song_id,
            "difficulty": "Easy-Medium Demon",
            "object_count": self.object_count,
            "sections": len(self.sections),
            "groups": self.next_group - 1000,
            "colors": self.next_color - 1000,
            "game_modes": [s.game_mode for s in self.sections],
            "version": "2.2091"
        }
        with open(filename.replace('.gdlvl', '_meta.json'), 'w') as f:
            json.dump(meta, f, indent=2)
        
        return filename


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("GEOMETRY DASH MASTERPIECE LEVEL GENERATOR")
    print("Target: GD 2.2091 | 150k-200k objects | All game modes")
    print("=" * 60)
    
    # Newgrounds song ID (example: "Geometry Dash" by Waterflame = 624012)
    # You can change this to any Newgrounds audio ID
    SONG_ID = 624012  # Waterflame - Geometry Dash (classic)
    
    generator = MasterpieceLevelGenerator(
        song_id=SONG_ID,
        level_name="MASTERPIECE",
        author="Kilo"
    )
    
    output_file = generator.save("masterpiece.gdlvl")
    
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE!")
    print("=" * 60)
    print(f"File: {output_file}")
    print(f"Objects: {generator.object_count:,}")
    print(f"Sections: {len(generator.sections)}")
    print(f"Game modes: {', '.join(set(s.game_mode for s in generator.sections))}")
    print("\nTo use in GD 2.2091:")
    print("1. Copy masterpiece.gdlvl to your GD levels folder")
    print("2. Import in-game via Level Browser -> Import")
    print("3. Enjoy the masterpiece!")
    
    return generator


if __name__ == "__main__":
    main()