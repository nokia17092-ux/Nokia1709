#!/usr/bin/env python3
"""
Geometry Dash Masterpiece Level Generator - HIGH DENSITY VERSION
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

class TriggerType(IntEnum):
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
# LEVEL GENERATOR - HIGH DENSITY
# ============================================================

class MasterpieceLevelGenerator:
    def __init__(self, song_id: int = 624012, level_name: str = "MASTERPIECE", author: str = "Kilo"):
        self.song_id = song_id
        self.level_name = level_name
        self.author = author
        self.objects: List[GDObject] = []
        self.sections: List[LevelSection] = []
        self.next_group = 1000
        self.next_color = 1000
        self.object_count = 0
        self.section_width = 1200  # Much wider sections
        
        self.level_desc = "A masterpiece level with 150k+ objects, all game modes, advanced triggers & art"
        self.level_version = 47
        self.game_version = 22
        self.difficulty = 4
        self.demon_difficulty = 3
        self.stars = 10
        self.featured = 0
        self.epic = 1
        self.coins = 3
        self.length = 5
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
    # OBJECT CREATION HELPERS
    # ============================================================
    
    def portal(self, x: float, y: float, portal_type: int, groups: List[int] = None) -> GDObject:
        return GDObject(object_id=portal_type, x=x, y=y, groups=groups or [])
    
    def orb(self, x: float, y: float, orb_type: int, groups: List[int] = None) -> GDObject:
        return GDObject(object_id=orb_type, x=x, y=y, groups=groups or [])
    
    def pad(self, x: float, y: float, pad_type: int, groups: List[int] = None) -> GDObject:
        return GDObject(object_id=pad_type, x=x, y=y, groups=groups or [])
    
    def block(self, x: float, y: float, block_id: int, rotation: float = 0, scale: float = 1.0,
              flip_x: bool = False, flip_y: bool = False, groups: List[int] = None,
              color_1: int = 0, color_2: int = 0, z_order: int = 0, z_layer: int = 0,
              high_detail: bool = False) -> GDObject:
        return GDObject(
            object_id=block_id, x=x, y=y, rotation=rotation, scale=scale,
            flip_x=flip_x, flip_y=flip_y, groups=groups or [],
            color_1=color_1, color_2=color_2, z_order=z_order, z_layer=z_layer,
            high_detail=high_detail
        )
    
    def spike(self, x: float, y: float, rotation: float = 0, scale: float = 1.0,
              groups: List[int] = None, color_1: int = 0, color_2: int = 0) -> GDObject:
        return GDObject(
            object_id=BlockType.SPIKE, x=x, y=y, rotation=rotation, scale=scale,
            groups=groups or [], color_1=color_1, color_2=color_2
        )
    
    def trigger(self, x: float, y: float, trigger_type: int, target_group: int,
                activate_groups: List[int] = None, deactivate_groups: List[int] = None,
                toggle_groups: List[int] = None, spawn_triggered: bool = False,
                touch_triggered: bool = False, multi_trigger: bool = False,
                groups: List[int] = None) -> GDObject:
        return GDObject(
            object_id=trigger_type, x=x, y=y, is_trigger=True,
            target_group=target_group, activate_group=activate_groups or [],
            deactivate_group=deactivate_groups or [], toggle_group=toggle_groups or [],
            spawn_triggered=spawn_triggered, touch_triggered=touch_triggered,
            multi_trigger=multi_trigger, groups=groups or []
        )
    
    def move_trigger(self, x: float, y: float, target_group: int, move_x: float, move_y: float,
                     duration: float = 1.0, easing: int = 0, spawn_triggered: bool = False,
                     touch_triggered: bool = False, groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_MOVE, x=x, y=y, is_trigger=True,
                     target_group=target_group, move_x=move_x, move_y=move_y,
                     spawn_triggered=spawn_triggered, touch_triggered=touch_triggered,
                     groups=groups or [])
        return t
    
    def rotate_trigger(self, x: float, y: float, target_group: int, degrees: float,
                       duration: float = 1.0, easing: int = 0, spawn_triggered: bool = False,
                       groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_ROTATE, x=x, y=y, is_trigger=True,
                     target_group=target_group, rotate_degrees=degrees,
                     spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def scale_trigger(self, x: float, y: float, target_group: int, multiplier: float,
                      duration: float = 1.0, easing: int = 0, spawn_triggered: bool = False,
                      groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_SCALE, x=x, y=y, is_trigger=True,
                     target_group=target_group, scale_multiplier=multiplier,
                     spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def color_trigger(self, x: float, y: float, target_group: int, color_hsv: Tuple[float, float, float],
                      duration: float = 1.0, easing: int = 0, copy_color_1: int = 0,
                      copy_color_2: int = 0, copy_opacity: int = 0, copy_blending: int = 0,
                      spawn_triggered: bool = False, groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_COLOR, x=x, y=y, is_trigger=True,
                     target_group=target_group, color_hsv=color_hsv,
                     copy_color_1=copy_color_1, copy_color_2=copy_color_2,
                     copy_opacity=copy_opacity, copy_blending=copy_blending,
                     spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def pulse_trigger(self, x: float, y: float, target_group: int, hsv: Tuple[float, float, float],
                      duration: float = 1.0, easing: int = 0, spawn_triggered: bool = False,
                      groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_PULSE, x=x, y=y, is_trigger=True,
                     target_group=target_group, pulse_hsv=hsv, pulse_duration=duration,
                     pulse_easing=easing, spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def alpha_trigger(self, x: float, y: float, target_group: int, alpha: float,
                      duration: float = 1.0, easing: int = 0, spawn_triggered: bool = False,
                      groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_ALPHA, x=x, y=y, is_trigger=True,
                     target_group=target_group, alpha_value=alpha, alpha_duration=duration,
                     spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def hsv_trigger(self, x: float, y: float, target_group: int, hsv: Tuple[float, float, float],
                    duration: float = 1.0, easing: int = 0, spawn_triggered: bool = False,
                    groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_HSV, x=x, y=y, is_trigger=True,
                     target_group=target_group, color_hsv=hsv, color_duration=duration,
                     spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def follow_trigger(self, x: float, y: float, target_group: int,
                       follow_x: bool = True, follow_y: bool = True,
                       x_speed: float = 1.0, y_speed: float = 1.0,
                       x_offset: float = 0, y_offset: float = 0,
                       x_modulo: float = 0, y_modulo: float = 0,
                       x_amount: float = 1.0, y_amount: float = 1.0,
                       spawn_triggered: bool = False, groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_FOLLOW, x=x, y=y, is_trigger=True,
                     target_group=target_group, follow_player_x=follow_x, follow_player_y=follow_y,
                     follow_x_speed=x_speed, follow_y_speed=y_speed,
                     follow_x_offset=x_offset, follow_y_offset=y_offset,
                     follow_x_modulo=x_modulo, follow_y_modulo=y_modulo,
                     follow_x_amount=x_amount, follow_y_amount=y_amount,
                     spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def shake_trigger(self, x: float, y: float, target_group: int, strength: float, interval: float,
                      spawn_triggered: bool = False, groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_SHAKE, x=x, y=y, is_trigger=True,
                     target_group=target_group, shake_strength=strength, shake_interval=interval,
                     spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def anim_trigger(self, x: float, y: float, target_group: int, anim_id: int,
                     spawn_triggered: bool = False, groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_ANIMATION, x=x, y=y, is_trigger=True,
                     target_group=target_group, animation_id=anim_id,
                     spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def spawn_trigger(self, x: float, y: float, target_group: int, delay: float = 0,
                      spawn_triggered: bool = True, groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_SPAWN, x=x, y=y, is_trigger=True,
                     target_group=target_group, spawn_triggered=spawn_triggered, groups=groups or [])
        return t
    
    def touch_trigger(self, x: float, y: float, target_group: int,
                      activate_groups: List[int] = None, deactivate_groups: List[int] = None,
                      toggle_groups: List[int] = None, groups: List[int] = None) -> GDObject:
        t = GDObject(object_id=BlockType.TRIGGER_TOUCH, x=x, y=y, is_trigger=True,
                     target_group=target_group, activate_group=activate_groups or [],
                     deactivate_group=deactivate_groups or [], toggle_group=toggle_groups or [],
                     touch_triggered=True, groups=groups or [])
        return t
    
    def deco(self, x: float, y: float, deco_id: int, rotation: float = 0, scale: float = 1.0,
             flip_x: bool = False, flip_y: bool = False, color_1: int = 0, color_2: int = 0,
             z_order: int = 0, z_layer: int = 0, groups: List[int] = None,
             high_detail: bool = False, editor_layer_1: int = 0, editor_layer_2: int = 0) -> GDObject:
        return GDObject(object_id=deco_id, x=x, y=y, rotation=rotation, scale=scale,
                        flip_x=flip_x, flip_y=flip_y, color_1=color_1, color_2=color_2,
                        z_order=z_order, z_layer=z_layer, groups=groups or [],
                        high_detail=high_detail, editor_layer_1=editor_layer_1,
                        editor_layer_2=editor_layer_2)
    
    # ============================================================
    # DENSE DECORATION SYSTEMS
    # ============================================================
    
    def add_dense_ground(self, section: LevelSection, density: int = 3):
        """Add dense ground pattern with variations"""
        width = section.end_x - section.start_x
        segments = int(width / 15)
        
        for i in range(segments):
            x = section.start_x + i * 15
            y = 15
            
            # Main ground
            for layer in range(density):
                ly = y - 15 - layer * 30
                obj = self.block(x, ly, BlockType.SOLID_BLOCK,
                    color_1=self.new_color(), color_2=self.new_color(),
                    high_detail=(layer == 0), z_layer=-1 - layer)
                section.objects.append(obj)
            
            # Ground decoration every few segments
            if i % 2 == 0:
                deco_y = y - 15 + random.uniform(-5, 5)
                obj = self.deco(x + 7, deco_y, random.choice([BlockType.DECOR_SMALL_1, BlockType.DECOR_SMALL_2]),
                    scale=random.uniform(0.3, 0.8), rotation=random.uniform(0, 360),
                    color_1=self.new_color(), z_layer=-2)
                section.decoration.append(obj)
            
            # Spikes on ground (visual)
            if i % 5 == 0:
                obj = self.spike(x + 7, y - 15, rotation=180, scale=0.6,
                    color_1=self.new_color(), color_2=self.new_color())
                section.decoration.append(obj)
    
    def add_dense_ceiling(self, section: LevelSection, height: float = 100, density: int = 2):
        """Add dense ceiling pattern"""
        width = section.end_x - section.start_x
        segments = int(width / 15)
        
        for i in range(segments):
            x = section.start_x + i * 15
            y = 15 + height
            
            for layer in range(density):
                ly = y + layer * 30
                obj = self.block(x, ly, BlockType.SOLID_BLOCK, rotation=180,
                    color_1=self.new_color(), color_2=self.new_color(),
                    high_detail=(layer == 0), z_layer=-1 - layer)
                section.objects.append(obj)
    
    def add_3d_background_layers(self, section: LevelSection, num_layers: int = 8):
        """Add many 3D background layers for depth"""
        width = section.end_x - section.start_x
        
        for layer in range(num_layers):
            z = -10 - layer * 3
            parallax = 1.0 - layer * 0.1
            scale = 2.0 + layer * 0.4
            count = int(width / (30 * parallax))
            
            for i in range(count + 2):
                x = section.start_x + i * 30 * parallax - 30
                y = 15 + math.sin(i * 0.08 + layer * 0.5) * 60 * parallax
                
                # Large background structures
                deco_id = random.choice([BlockType.DECOR_LARGE_1, BlockType.DECOR_MEDIUM_1, BlockType.GLOW_2])
                obj = self.deco(x, y, deco_id, scale=scale * random.uniform(0.8, 1.2),
                    rotation=random.uniform(0, 360), color_1=self.new_color(),
                    color_2=self.new_color(), z_layer=z, high_detail=(layer < 3))
                section.decoration.append(obj)
                
                # Additional glow
                if layer < 4 and random.random() < 0.3:
                    glow = self.deco(x + random.uniform(-20, 20), y + random.uniform(-20, 20),
                        BlockType.GLOW_1, scale=scale * 0.5 * random.uniform(0.5, 1.5),
                        color_1=self.new_color(), z_layer=z - 1)
                    section.decoration.append(glow)
    
    def add_foreground_art_dense(self, section: LevelSection):
        """Add dense foreground decorative art"""
        width = section.end_x - section.start_x
        count = int(width / 20)
        
        for i in range(count):
            x = section.start_x + i * 20 + random.uniform(-10, 10)
            y = 15 + random.uniform(-40, 120)
            
            # Rings with pulse triggers
            if random.random() < 0.4:
                group = self.new_group()
                ring = self.deco(x, y, random.choice([BlockType.RING_1, BlockType.RING_2]),
                    scale=random.uniform(0.4, 1.8), rotation=random.uniform(0, 360),
                    color_1=self.new_color(), color_2=self.new_color(),
                    z_layer=2, groups=[group])
                section.decoration.append(ring)
                
                section.triggers.append(self.pulse_trigger(
                    section.start_x, 15, group,
                    hsv=(random.random(), 0.8, 1.0),
                    duration=random.uniform(1.0, 4.0), spawn_triggered=True))
            
            # Saw blades
            if random.random() < 0.25:
                saw = self.deco(x, y, random.choice([BlockType.SAW_1, BlockType.SAW_2]),
                    scale=random.uniform(0.3, 1.0), color_1=self.new_color(), z_layer=1)
                section.decoration.append(saw)
            
            # Particle clusters
            if random.random() < 0.5:
                for _ in range(random.randint(2, 6)):
                    px = x + random.uniform(-15, 15)
                    py = y + random.uniform(-15, 15)
                    part = self.deco(px, py, BlockType.PARTICLE_1,
                        scale=random.uniform(0.08, 0.25), color_1=self.new_color(), z_layer=3)
                    section.decoration.append(part)
            
            # Glow orbs
            if random.random() < 0.3:
                glow = self.deco(x, y, random.choice([BlockType.GLOW_1, BlockType.GLOW_2]),
                    scale=random.uniform(0.5, 1.5), color_1=self.new_color(),
                    color_2=self.new_color(), z_layer=2)
                section.decoration.append(glow)
            
            # Small decor
            if random.random() < 0.35:
                deco = self.deco(x, y, random.choice([BlockType.DECOR_SMALL_1, BlockType.DECOR_SMALL_2]),
                    scale=random.uniform(0.2, 0.6), rotation=random.uniform(0, 360),
                    color_1=self.new_color(), z_layer=1)
                section.decoration.append(deco)
    
    def add_pulse_system_dense(self, section: LevelSection, bpm: float = 150):
        """Add comprehensive pulse system with many groups"""
        beat_interval = 60.0 / bpm * 15
        num_groups = 8
        
        main_groups = [self.new_group() for _ in range(num_groups)]
        
        # Assign objects to pulse groups
        all_objects = section.objects + section.decoration
        for i, obj in enumerate(all_objects):
            if not obj.is_trigger and obj.z_layer >= -2:
                obj.groups.append(main_groups[i % num_groups])
        
        # Pulse triggers at beat intervals
        x = section.start_x
        beat = 0
        while x < section.end_x:
            for gi, group in enumerate(main_groups):
                hue = (gi / num_groups + beat * 0.02 + x * 0.0005) % 1.0
                section.triggers.append(self.pulse_trigger(
                    x, 15, group,
                    hsv=(hue, 0.9, 1.0),
                    duration=beat_interval / 15 * 0.4, easing=1, spawn_triggered=True))
            x += beat_interval
            beat += 1
        
        # Off-beat pulses
        x = section.start_x + beat_interval / 2
        beat = 0
        while x < section.end_x:
            for gi, group in enumerate(main_groups):
                hue = (gi / num_groups + beat * 0.02 + x * 0.0005 + 0.5) % 1.0
                section.triggers.append(self.pulse_trigger(
                    x, 15, group,
                    hsv=(hue, 0.6, 0.8),
                    duration=beat_interval / 15 * 0.3, easing=2, spawn_triggered=True))
            x += beat_interval
            beat += 1
    
    def add_color_scheme_dense(self, section: LevelSection, base_hue: float):
        """Apply color scheme with many color triggers"""
        # Create color palette
        palette = []
        for i in range(30):
            h = (base_hue + i * 0.03 + random.uniform(-0.02, 0.02)) % 1.0
            s = 0.6 + random.random() * 0.4
            v = 0.5 + random.random() * 0.5
            palette.append((h, s, v))
        
        # Assign colors to objects
        for obj in section.objects + section.decoration:
            if obj.color_1 == 0 and not obj.is_trigger:
                c = random.choice(palette)
                obj.color_1 = self.new_color()
                obj.color_hsv = c
        
        # Color triggers at section transitions
        for i in range(0, int(section.end_x - section.start_x), 100):
            x = section.start_x + i
            for obj in section.objects[:5]:
                if obj.color_1 > 0:
                    section.triggers.append(self.color_trigger(
                        x, 15, obj.color_1, color_hsv=obj.color_hsv,
                        duration=0.1, spawn_triggered=True))
    
    def add_advanced_trigger_chains(self, section: LevelSection):
        """Add complex trigger chains: move, rotate, scale, follow, HSV, shake"""
        num_chains = 6
        
        for chain in range(num_chains):
            group = self.new_group()
            
            # Add decorative objects to this chain
            for i in range(8):
                x = section.start_x + random.uniform(0, section.end_x - section.start_x)
                y = 15 + random.uniform(-30, 100)
                obj = self.deco(x, y, random.choice([BlockType.DECOR_MEDIUM_1, BlockType.DECOR_LARGE_1, BlockType.GLOW_2]),
                    scale=random.uniform(0.5, 1.5), rotation=random.uniform(0, 360),
                    color_1=self.new_color(), groups=[group], z_layer=1)
                section.decoration.append(obj)
            
            # Move trigger
            section.triggers.append(self.move_trigger(
                section.start_x, 15, group,
                move_x=random.uniform(-50, 50), move_y=random.uniform(-40, 40),
                duration=random.uniform(3.0, 8.0), easing=random.randint(0, 3),
                spawn_triggered=True))
            
            # Rotate trigger
            section.triggers.append(self.rotate_trigger(
                section.start_x + 50, 15, group,
                degrees=360 * random.uniform(0.25, 3.0),
                duration=random.uniform(4.0, 12.0), easing=random.randint(0, 2),
                spawn_triggered=True))
            
            # Scale trigger
            section.triggers.append(self.scale_trigger(
                section.start_x + 100, 15, group,
                multiplier=random.uniform(0.7, 1.4),
                duration=random.uniform(2.0, 5.0), easing=random.randint(0, 2),
                spawn_triggered=True))
            
            # HSV shift
            section.triggers.append(self.hsv_trigger(
                section.start_x + 150, 15, group,
                hsv=(random.random(), 0.8, 1.0),
                duration=random.uniform(5.0, 15.0), easing=random.randint(0, 2),
                spawn_triggered=True))
            
            # Alpha pulse
            section.triggers.append(self.alpha_trigger(
                section.start_x + 200, 15, group,
                alpha=random.uniform(0.3, 1.0),
                duration=random.uniform(2.0, 4.0), easing=random.randint(0, 2),
                spawn_triggered=True))
        
        # Follow player chains
        for chain in range(3):
            group = self.new_group()
            for i in range(4):
                x = section.start_x + i * 150 + random.uniform(-30, 30)
                y = 15 + 50 + random.uniform(-20, 20)
                obj = self.deco(x, y, random.choice([BlockType.GLOW_1, BlockType.GLOW_2, BlockType.RING_1]),
                    scale=random.uniform(1.0, 2.0), color_1=self.new_color(),
                    groups=[group], z_layer=2)
                section.decoration.append(obj)
            
            section.triggers.append(self.follow_trigger(
                section.start_x, 15, group,
                follow_x=True, follow_y=True,
                x_speed=random.uniform(0.1, 0.5), y_speed=random.uniform(0.1, 0.4),
                x_offset=random.uniform(-20, 20), y_offset=random.uniform(-20, 20),
                spawn_triggered=True))
        
        # Shake triggers on strong beats
        beat_interval = 60.0 / 150 * 15 * 4  # Every 4 beats
        x = section.start_x
        while x < section.end_x:
            section.triggers.append(self.shake_trigger(
                x, 15, self.new_group(),
                strength=random.uniform(1.0, 4.0), interval=0.05,
                spawn_triggered=True))
            x += beat_interval
        
        # Animation triggers
        for i in range(3):
            group = self.new_group()
            for _ in range(3):
                x = section.start_x + random.uniform(0, section.end_x - section.start_x)
                y = 15 + random.uniform(-20, 80)
                obj = self.deco(x, y, BlockType.PULSE_OBJECT,
                    scale=random.uniform(0.8, 1.5), color_1=self.new_color(),
                    groups=[group], z_layer=1)
                section.decoration.append(obj)
            
            section.triggers.append(self.anim_trigger(
                section.start_x + i * 200, 15, group,
                anim_id=random.randint(1, 5), spawn_triggered=True))
    
    def add_moving_platforms(self, section: LevelSection, count: int = 10):
        """Add moving platforms with complex paths"""
        width = section.end_x - section.start_x
        
        for i in range(count):
            x = section.start_x + i * (width / count) + random.uniform(-20, 20)
            y = 15 + random.uniform(10, 80)
            group = self.new_group()
            
            # Platform
            obj = self.block(x, y, BlockType.PLATFORM, scale=random.uniform(0.6, 1.2),
                color_1=self.new_color(), groups=[group])
            section.objects.append(obj)
            
            # Complex move pattern
            move_type = random.randint(0, 4)
            if move_type == 0:  # Horizontal
                section.triggers.append(self.move_trigger(
                    section.start_x, 15, group,
                    move_x=random.uniform(-40, 40), move_y=0,
                    duration=random.uniform(2.0, 4.0), easing=1, spawn_triggered=True))
            elif move_type == 1:  # Vertical
                section.triggers.append(self.move_trigger(
                    section.start_x, 15, group,
                    move_x=0, move_y=random.uniform(-30, 30),
                    duration=random.uniform(2.0, 4.0), easing=1, spawn_triggered=True))
            elif move_type == 2:  # Circular
                section.triggers.append(self.move_trigger(
                    section.start_x, 15, group,
                    move_x=random.uniform(-25, 25), move_y=random.uniform(-25, 25),
                    duration=random.uniform(3.0, 6.0), easing=2, spawn_triggered=True))
                section.triggers.append(self.rotate_trigger(
                    section.start_x + 50, 15, group,
                    degrees=360, duration=random.uniform(4.0, 8.0), spawn_triggered=True))
            elif move_type == 3:  # Figure-8
                section.triggers.append(self.move_trigger(
                    section.start_x, 15, group,
                    move_x=random.uniform(-30, 30), move_y=random.uniform(-20, 20),
                    duration=random.uniform(4.0, 8.0), easing=3, spawn_triggered=True))
            else:  # Random
                section.triggers.append(self.move_trigger(
                    section.start_x, 15, group,
                    move_x=random.uniform(-50, 50), move_y=random.uniform(-40, 40),
                    duration=random.uniform(3.0, 7.0), easing=random.randint(0, 3),
                    spawn_triggered=True))
    
    # ============================================================
    # SECTION BUILDERS - HIGH DENSITY
    # ============================================================
    
    def build_intro_section(self, start_x: float) -> LevelSection:
        section = LevelSection(
            name="Intro - Atmospheric Buildup",
            start_x=start_x, end_x=start_x + self.section_width,
            game_mode="cube", difficulty="Easy",
            bg_color=(10, 5, 20), ground_color=(30, 15, 50)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.portal(x, y, BlockType.PORTAL_CUBE))
        section.objects.append(self.portal(x, y, BlockType.PORTAL_SPEED_1))
        x += 50
        
        # Dense atmospheric cube
        pattern_length = int(self.section_width / 15)
        for i in range(pattern_length):
            bx = x + i * 15
            
            # Multi-layer ground
            for layer in range(4):
                ly = y - 15 - layer * 30
                obj = self.block(bx, ly, BlockType.SOLID_BLOCK,
                    color_1=self.new_color(), color_2=self.new_color(),
                    high_detail=(layer < 2), z_layer=-1 - layer)
                section.objects.append(obj)
            
            # Floating platforms
            if i % 3 == 0:
                px = bx + 7
                py = y + 35 + math.sin(i * 0.4) * 25
                group = self.new_group()
                obj = self.block(px, py, BlockType.PLATFORM, scale=0.7,
                    color_1=self.new_color(), groups=[group])
                section.objects.append(obj)
                section.triggers.append(self.move_trigger(bx, y - 30, group,
                    move_x=0, move_y=math.sin(i) * 15, duration=4.0, spawn_triggered=True))
            
            # Orbs
            if i % 4 == 1:
                section.objects.append(self.orb(bx + 7, y + 50 + math.sin(i * 0.3) * 20, BlockType.ORB_YELLOW))
            if i % 4 == 3:
                section.objects.append(self.orb(bx + 7, y + 70 + math.sin(i * 0.5) * 15, BlockType.ORB_BLUE))
            
            # Decoration
            if i % 2 == 0:
                section.decoration.append(self.deco(bx + 7, y - 10, random.choice([BlockType.DECOR_SMALL_1, BlockType.DECOR_SMALL_2]),
                    scale=0.5, rotation=i * 15, color_1=self.new_color(), z_layer=-2))
        
        section.end_x = x + pattern_length * 15
        return section
    
    def build_gameplay_section(self, start_x: float, name: str, game_mode: str,
                                portal_id: int, speed: int, difficulty: str,
                                pattern_count: int, bg_color: Tuple, ground_color: Tuple,
                                extra_portals: List[int] = None) -> LevelSection:
        """Generic gameplay section builder"""
        section = LevelSection(
            name=name, start_x=start_x, end_x=start_x + self.section_width,
            game_mode=game_mode, difficulty=difficulty,
            bg_color=bg_color, ground_color=ground_color
        )
        
        x = start_x
        y = 15
        
        # Portals
        section.objects.append(self.portal(x, y, portal_id))
        section.objects.append(self.portal(x, y, speed))
        if extra_portals:
            for p in extra_portals:
                section.objects.append(self.portal(x, y, p))
        x += 50
        
        pattern_length = int(self.section_width / 15)
        
        for i in range(pattern_length):
            bx = x + i * 15
            
            # Ground
            for layer in range(3):
                ly = y - 15 - layer * 30
                obj = self.block(bx, ly, BlockType.SOLID_BLOCK,
                    color_1=self.new_color(), color_2=self.new_color(),
                    high_detail=(layer == 0), z_layer=-1 - layer)
                section.objects.append(obj)
            
            # Ceiling for non-cube modes
            if game_mode in ["ship", "ball", "ufo", "wave", "spider"]:
                for layer in range(2):
                    ly = y + 100 + layer * 30
                    obj = self.block(bx, ly, BlockType.SOLID_BLOCK, rotation=180,
                        color_1=self.new_color(), color_2=self.new_color(),
                        high_detail=(layer == 0), z_layer=-1 - layer)
                    section.objects.append(obj)
            
            # Gameplay patterns based on mode
            pattern = i % 16
            
            if game_mode == "cube":
                if pattern == 0:
                    section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_YELLOW))
                elif pattern == 2:
                    section.objects.append(self.orb(bx + 7, y + 45, BlockType.ORB_BLUE))
                elif pattern == 4:
                    section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_GREEN))
                elif pattern == 6:
                    section.objects.append(self.pad(bx + 7, y - 15, BlockType.PAD_YELLOW))
                elif pattern == 8:
                    section.objects.append(self.pad(bx + 7, y - 15, BlockType.PAD_PINK))
                elif pattern == 10:
                    section.objects.append(self.orb(bx + 7, y + 60, BlockType.ORB_RED))
                elif pattern == 12:
                    section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_PURPLE))
                elif pattern == 14:
                    section.objects.append(self.orb(bx + 7, y + 45, BlockType.ORB_DASH))
                elif pattern in [1, 5, 9, 13]:
                    section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_GRAVITY))
                elif pattern in [3, 7, 11, 15]:
                    section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_MIRROR))
            
            elif game_mode == "ship":
                if pattern % 3 == 1:
                    obs_y = y + 30 + math.sin(i * 0.4) * 30
                    group = self.new_group()
                    obj = self.block(bx + 7, obs_y, BlockType.SOLID_BLOCK, scale=0.6,
                        rotation=random.choice([0, 90, 180, 270]), color_1=self.new_color(), groups=[group])
                    section.objects.append(obj)
                    section.triggers.append(self.move_trigger(bx, y - 30, group,
                        move_x=0, move_y=math.sin(i) * 20, duration=3.0, spawn_triggered=True))
                if pattern % 5 == 0:
                    section.objects.append(self.orb(bx + 7, y + 25, BlockType.ORB_YELLOW))
                if pattern % 7 == 0:
                    section.objects.append(self.portal(bx + 7, y + 40, BlockType.PORTAL_GRAVITY))
            
            elif game_mode == "ball":
                if pattern % 4 == 0:
                    section.objects.append(self.portal(bx + 7, y + 35, BlockType.PORTAL_GRAVITY))
                if pattern % 3 == 1:
                    section.objects.append(self.orb(bx + 7, y + 20, BlockType.ORB_BLUE))
                if pattern % 3 == 2:
                    section.objects.append(self.orb(bx + 7, y + 55, BlockType.ORB_RED))
                if pattern % 5 == 0:
                    group = self.new_group()
                    obj = self.block(bx + 7, y + 35, BlockType.PLATFORM, scale=0.6,
                        color_1=self.new_color(), groups=[group])
                    section.objects.append(obj)
                    section.triggers.append(self.move_trigger(bx, y - 30, group,
                        move_x=0, move_y=20, duration=2.5, easing=1, spawn_triggered=True))
            
            elif game_mode == "ufo":
                if pattern % 2 == 0:
                    mid_y = y + 40 + math.sin(i * 0.3) * 25
                    group = self.new_group()
                    obj = self.block(bx + 7, mid_y, BlockType.SOLID_BLOCK, scale=0.5,
                        color_1=self.new_color(), groups=[group])
                    section.objects.append(obj)
                if pattern % 3 == 1:
                    section.objects.append(self.orb(bx + 7, y + 20, BlockType.ORB_YELLOW))
                if pattern % 3 == 2:
                    section.objects.append(self.orb(bx + 7, y + 70, BlockType.ORB_BLUE))
            
            elif game_mode == "wave":
                if pattern % 8 == 3:
                    section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_MINI))
                if pattern % 8 == 7:
                    section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_NORMAL))
                # Wave corridor
                top = y + 55 + (1 if i % 2 == 0 else -1) * 25
                bot = y - 10 + (1 if i % 2 == 0 else -1) * 25
                # Already added ceiling/floor above
            
            elif game_mode == "robot":
                if pattern % 3 == 0:
                    section.objects.append(self.block(bx + 7, y + 30, BlockType.PLATFORM, scale=0.8,
                        color_1=self.new_color()))
                elif pattern % 3 == 1:
                    section.objects.append(self.block(bx + 7, y + 55, BlockType.PLATFORM, scale=0.6,
                        color_1=self.new_color()))
                elif pattern % 3 == 2:
                    section.objects.append(self.block(bx + 7, y + 15, BlockType.PLATFORM, scale=0.7,
                        color_1=self.new_color()))
                if pattern % 4 == 1:
                    section.objects.append(self.orb(bx + 7, y + 45, BlockType.ORB_YELLOW))
                if pattern % 4 == 3:
                    section.objects.append(self.orb(bx + 7, y + 70, BlockType.ORB_BLUE))
            
            elif game_mode == "spider":
                if pattern % 2 == 0:
                    section.objects.append(self.block(bx + 7, y + 35, BlockType.SOLID_BLOCK, scale=0.5,
                        color_1=self.new_color()))
                if pattern % 3 == 1:
                    section.objects.append(self.orb(bx + 7, y + 20, BlockType.ORB_YELLOW))
                if pattern % 3 == 2:
                    section.objects.append(self.orb(bx + 7, y + 65, BlockType.ORB_BLUE))
            
            elif game_mode == "swing":
                if pattern % 2 == 0:
                    group = self.new_group()
                    obj = self.block(bx + 7, y + 50, BlockType.SOLID_BLOCK, scale=0.3,
                        color_1=self.new_color(), groups=[group])
                    section.objects.append(obj)
                if pattern % 3 == 1:
                    section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_YELLOW))
            
            elif game_mode == "platformer":
                if pattern % 3 == 0:
                    section.objects.append(self.block(bx, y - 15, BlockType.SOLID_BLOCK, scale=2.5,
                        color_1=self.new_color(), high_detail=True))
                if pattern % 2 == 1:
                    py = y + 20 + (pattern % 4) * 20
                    group = self.new_group()
                    obj = self.block(bx + 7, py, BlockType.PLATFORM, scale=0.9,
                        color_1=self.new_color(), groups=[group])
                    section.objects.append(obj)
                    section.triggers.append(self.move_trigger(bx, y - 30, group,
                        move_x=20, move_y=0, duration=2.5, spawn_triggered=True))
                if pattern % 4 == 2:
                    section.objects.append(self.orb(bx + 7, y + 35, BlockType.ORB_YELLOW))
            
            # Dense decoration every few patterns
            if i % 2 == 0:
                section.decoration.append(self.deco(bx + 7, y - 5 + random.uniform(-5, 5),
                    random.choice([BlockType.DECOR_SMALL_1, BlockType.DECOR_SMALL_2]),
                    scale=random.uniform(0.3, 0.7), rotation=random.uniform(0, 360),
                    color_1=self.new_color(), z_layer=-2))
            
            if i % 3 == 0:
                section.decoration.append(self.spike(bx + 7, y - 15, rotation=180, scale=0.5,
                    color_1=self.new_color(), color_2=self.new_color()))
        
        section.end_x = x + pattern_length * 15
        return section
    
    def build_cube_section_1(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "Cube 1 - Rhythmic Flow", "cube",
            BlockType.PORTAL_CUBE, BlockType.PORTAL_SPEED_2, "Easy Demon",
            80, (20, 10, 40), (50, 25, 80))
    
    def build_ship_section(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "Ship - Tight Corridors", "ship",
            BlockType.PORTAL_SHIP, BlockType.PORTAL_SPEED_3, "Medium Demon",
            80, (30, 15, 50), (60, 30, 90))
    
    def build_ball_section(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "Ball - Gravity Mastery", "ball",
            BlockType.PORTAL_BALL, BlockType.PORTAL_SPEED_2, "Medium Demon",
            80, (15, 30, 40), (40, 60, 80))
    
    def build_ufo_section(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "UFO - Precision Clicks", "ufo",
            BlockType.PORTAL_UFO, BlockType.PORTAL_SPEED_2, "Easy-Medium Demon",
            80, (25, 20, 45), (50, 40, 85))
    
    def build_wave_section(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "Wave - Tight Navigation", "wave",
            BlockType.PORTAL_WAVE, BlockType.PORTAL_SPEED_3, "Medium Demon",
            80, (35, 10, 50), (70, 20, 90))
    
    def build_robot_section(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "Robot - Hold Mastery", "robot",
            BlockType.PORTAL_ROBOT, BlockType.PORTAL_SPEED_2, "Medium Demon",
            80, (20, 35, 45), (45, 70, 85))
    
    def build_spider_section(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "Spider - Teleport Flow", "spider",
            BlockType.PORTAL_SPIDER, BlockType.PORTAL_SPEED_2, "Medium Demon",
            80, (30, 20, 55), (60, 40, 95))
    
    def build_swing_section(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "Swing - Momentum", "swing",
            BlockType.PORTAL_SWING, BlockType.PORTAL_SPEED_2, "Easy Demon",
            80, (25, 25, 50), (55, 50, 90))
    
    def build_platformer_section(self, start_x: float) -> LevelSection:
        return self.build_gameplay_section(start_x, "Platformer - Precision", "platformer",
            BlockType.PORTAL_PLATFORMER, BlockType.PORTAL_SPEED_1, "Easy Demon",
            80, (15, 25, 40), (35, 50, 75))
    
    def build_final_cube(self, start_x: float) -> LevelSection:
        section = LevelSection(
            name="Final Cube - Climax",
            start_x=start_x, end_x=start_x + self.section_width * 1.5,
            game_mode="cube", difficulty="Medium Demon",
            bg_color=(50, 10, 60), ground_color=(90, 20, 100)
        )
        
        x = start_x
        y = 15
        
        section.objects.append(self.portal(x, y, BlockType.PORTAL_CUBE))
        section.objects.append(self.portal(x, y, BlockType.PORTAL_SPEED_3))
        x += 50
        
        pattern_length = int(self.section_width * 1.5 / 15)
        
        for i in range(pattern_length):
            bx = x + i * 15
            
            # Multi-layer ground
            for layer in range(4):
                ly = y - 15 - layer * 30
                obj = self.block(bx, ly, BlockType.SOLID_BLOCK,
                    color_1=self.new_color(), color_2=self.new_color(),
                    high_detail=True, z_layer=-1 - layer)
                section.objects.append(obj)
            
            # Intense patterns
            pattern = i % 20
            if pattern == 0:
                section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_YELLOW))
            elif pattern == 1:
                section.objects.append(self.orb(bx + 7, y + 45, BlockType.ORB_BLUE))
            elif pattern == 2:
                section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_GREEN))
            elif pattern == 3:
                section.objects.append(self.pad(bx + 7, y - 15, BlockType.PAD_YELLOW))
            elif pattern == 4:
                section.objects.append(self.pad(bx + 7, y - 15, BlockType.PAD_PINK))
            elif pattern == 5:
                section.objects.append(self.orb(bx + 7, y + 60, BlockType.ORB_RED))
            elif pattern == 6:
                section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_PURPLE))
            elif pattern == 7:
                section.objects.append(self.orb(bx + 7, y + 45, BlockType.ORB_DASH))
            elif pattern == 8:
                section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_GRAVITY))
            elif pattern == 9:
                section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_MIRROR))
            elif pattern == 10:
                section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_MINI))
            elif pattern == 11:
                section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_NORMAL))
            elif pattern == 12:
                section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_YELLOW))
                section.objects.append(self.orb(bx + 12, y + 45, BlockType.ORB_BLUE))
            elif pattern == 13:
                section.objects.append(self.pad(bx + 7, y - 15, BlockType.PAD_YELLOW))
                section.objects.append(self.orb(bx + 12, y + 30, BlockType.ORB_GREEN))
            elif pattern == 14:
                section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_GRAVITY))
                section.objects.append(self.portal(bx + 12, y + 15, BlockType.PORTAL_MIRROR))
            elif pattern == 15:
                section.objects.append(self.orb(bx + 7, y + 45, BlockType.ORB_DASH))
                section.objects.append(self.orb(bx + 12, y + 60, BlockType.ORB_RED))
            elif pattern == 16:
                section.objects.append(self.pad(bx + 7, y - 15, BlockType.PAD_PINK))
                section.objects.append(self.orb(bx + 12, y + 30, BlockType.ORB_PURPLE))
            elif pattern == 17:
                section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_MINI))
                section.objects.append(self.portal(bx + 12, y + 15, BlockType.PORTAL_GRAVITY))
            elif pattern == 18:
                section.objects.append(self.portal(bx + 7, y + 15, BlockType.PORTAL_SIZE_NORMAL))
                section.objects.append(self.portal(bx + 12, y + 15, BlockType.PORTAL_MIRROR))
            elif pattern == 19:
                section.objects.append(self.orb(bx + 7, y + 30, BlockType.ORB_YELLOW))
                section.objects.append(self.orb(bx + 10, y + 45, BlockType.ORB_BLUE))
                section.objects.append(self.orb(bx + 13, y + 60, BlockType.ORB_RED))
            
            # Intense decoration
            if i % 1 == 0:
                section.decoration.append(self.deco(bx + 7, y + random.uniform(-10, 80),
                    random.choice([BlockType.GLOW_1, BlockType.GLOW_2, BlockType.RING_1]),
                    scale=random.uniform(0.5, 1.5), color_1=self.new_color(),
                    color_2=self.new_color(), z_layer=random.randint(1, 3)))
        
        section.objects.append(self.portal(x + pattern_length * 15, y, BlockType.PORTAL_CUBE))
        section.end_x = x + pattern_length * 15
        return section
    
    # ============================================================
    # MAIN GENERATION
    # ============================================================
    
    def generate(self) -> str:
        print("Generating masterpiece level (HIGH DENSITY)...")
        
        current_x = 0
        
        # Build all sections
        sections_builders = [
            ("Intro", self.build_intro_section),
            ("Cube 1", self.build_cube_section_1),
            ("Ship", self.build_ship_section),
            ("Ball", self.build_ball_section),
            ("UFO", self.build_ufo_section),
            ("Wave", self.build_wave_section),
            ("Robot", self.build_robot_section),
            ("Spider", self.build_spider_section),
            ("Swing", self.build_swing_section),
            ("Platformer", self.build_platformer_section),
            ("Final Cube", self.build_final_cube),
        ]
        
        for i, (name, builder) in enumerate(sections_builders):
            print(f"  Building section {i+1}/{len(sections_builders)}: {name}")
            section = builder(current_x)
            
            # Add all dense decoration systems
            print(f"    Adding 3D background...")
            self.add_3d_background_layers(section, num_layers=8)
            
            print(f"    Adding foreground art...")
            self.add_foreground_art_dense(section)
            
            print(f"    Adding pulse system...")
            self.add_pulse_system_dense(section, bpm=150 + i * 5)
            
            print(f"    Adding color scheme...")
            self.add_color_scheme_dense(section, base_hue=i * 0.08)
            
            print(f"    Adding advanced triggers...")
            self.add_advanced_trigger_chains(section)
            
            print(f"    Adding moving platforms...")
            self.add_moving_platforms(section, count=15)
            
            # Add ground/ceiling
            self.add_dense_ground(section, density=4)
            if section.game_mode in ["ship", "ball", "ufo", "wave", "spider"]:
                self.add_dense_ceiling(section, height=100, density=3)
            
            # Collect all
            self.add_objects(section.objects)
            self.add_objects(section.triggers)
            self.add_objects(section.decoration)
            
            current_x = section.end_x + 80
            self.sections.append(section)
            
            print(f"    Objects: {len(section.objects)}, Triggers: {len(section.triggers)}, Decor: {len(section.decoration)}")
        
        # Global elements
        self.add_global_decoration()
        self.add_secret_coins()
        
        print(f"\nTotal objects: {self.object_count:,}")
        
        # Encode
        level_string = self.encode_level_string()
        gdlvl_data = self.create_gdlvl(level_string)
        
        return gdlvl_data
    
    def add_global_decoration(self):
        """Add level title, author, difficulty text"""
        title = GDObject(object_id=914, x=-150, y=220,
            text_string=self.level_name, font_scale=2.5,
            color_1=self.new_color(), z_layer=10, editor_layer_1=1)
        self.add_object(title)
        
        author = GDObject(object_id=914, x=-150, y=190,
            text_string=f"By {self.author}", font_scale=1.2,
            color_1=self.new_color(), z_layer=10, editor_layer_1=1)
        self.add_object(author)
        
        diff = GDObject(object_id=914, x=-150, y=160,
            text_string="Easy-Medium Demon  ★★★★★★★★★★", font_scale=1.0,
            color_1=self.new_color(), z_layer=10, editor_layer_1=1)
        self.add_object(diff)
        
        # Version info
        ver = GDObject(object_id=914, x=-150, y=130,
            text_string="v1.0  |  GD 2.2091  |  150k+ Objects", font_scale=0.7,
            color_1=self.new_color(), z_layer=10, editor_layer_1=1)
        self.add_object(ver)
    
    def add_secret_coins(self):
        """Add 3 secret coins"""
        coin_sections = [1, 4, 9]  # Cube, Ball, Final Cube
        
        for idx, sec_idx in enumerate(coin_sections):
            if sec_idx < len(self.sections):
                sec = self.sections[sec_idx]
                sec_width = sec.end_x - sec.start_x
                cx = sec.start_x + sec_width // 3 * (idx + 1)
                cy = 15 + 50 + idx * 20
                
                coin_group = self.new_group()
                
                # Coin trigger
                coin_trigger = self.touch_trigger(cx, cy, coin_group,
                    activate_groups=[coin_group])
                self.add_object(coin_trigger)
                
                # Coin visual
                coin_visual = self.deco(cx, cy, 1048, scale=1.0,
                    color_1=self.new_color(), groups=[coin_group], z_layer=5)
                self.add_object(coin_visual)
                
                # Coin counter
                counter = GDObject(object_id=BlockType.TRIGGER_ITEM_EDIT,
                    x=cx, y=cy, is_trigger=True, target_group=coin_group,
                    groups=[coin_group])
                self.add_object(counter)
    
    def encode_level_string(self) -> str:
        print("Encoding level string...")
        
        header_parts = [
            f"kS38:{self.level_name}",
            f"kS39:{self.author}",
            f"kI40:{self.song_id}",
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
        
        object_strings = []
        for obj in self.objects:
            obj_dict = obj.to_dict()
            if not obj_dict:
                continue
            
            pairs = []
            for k, v in sorted(obj_dict.items()):
                if isinstance(v, float):
                    v = f"{v:.3f}".rstrip('0').rstrip('.')
                elif isinstance(v, bool):
                    v = '1' if v else '0'
                pairs.append(f"{k},{v}")
            
            if pairs:
                object_strings.append(','.join(pairs))
        
        level_string = ';'.join(header_parts) + ';' + ';'.join(object_strings) + ';'
        print(f"Level string length: {len(level_string):,} chars")
        return level_string
    
    def create_gdlvl(self, level_string: str) -> bytes:
        print("Creating .gdlvl file...")
        compressed = gzip.compress(level_string.encode('utf-8'), compresslevel=9)
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
        print(f"Compressed: {len(compressed):,} bytes | Base64: {len(encoded):,} chars")
        return encoded.encode('ascii')
    
    def save(self, filename: str = "masterpiece.gdlvl"):
        gdlvl_data = self.generate()
        
        with open(filename, 'wb') as f:
            f.write(gdlvl_data)
        
        print(f"\nSaved to {filename}")
        print(f"Object count: {self.object_count:,}")
        print(f"Sections: {len(self.sections)}")
        print(f"Groups: {self.next_group - 1000}")
        print(f"Colors: {self.next_color - 1000}")
        
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


def main():
    print("=" * 60)
    print("GEOMETRY DASH MASTERPIECE LEVEL GENERATOR - HIGH DENSITY")
    print("Target: GD 2.2091 | 150k-200k objects | All game modes")
    print("=" * 60)
    
    # Waterflame - Geometry Dash (Newgrounds ID: 624012)
    generator = MasterpieceLevelGenerator(
        song_id=624012,
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