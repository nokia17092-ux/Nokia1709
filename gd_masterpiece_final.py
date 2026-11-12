#!/usr/bin/env python3
"""
Geometry Dash Masterpiece Level Generator - MAXIMUM DENSITY
Generates a .gdlvl file for GD 2.2091 with 150k-250k objects
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
    X = 1; Y = 2; OBJECT_ID = 3; ROTATION = 4; FLIP_X = 5; FLIP_Y = 6
    SCALE = 7; GROUPS = 8; COLOR_1 = 9; COLOR_2 = 10; Z_ORDER = 11; Z_LAYER = 12
    HIDE = 13; LOCK = 14; HIGH_DETAIL = 15; DONT_FADE = 16; IS_TRIGGER = 17
    TARGET_GROUP = 18; TOUCH_TRIGGERED = 19; SPAWN_TRIGGERED = 20; MULTI_TRIGGER = 21
    TRIGGER_TYPE = 22; ACTIVATE_GROUP = 23; DEACTIVATE_GROUP = 24; TOGGLE_GROUP = 25
    SPAWN_TRIGGERED_MULTI = 26; TRIGGER_ON_DEATH = 27; FOLLOW_PLAYER_Y = 28
    FOLLOW_PLAYER_X = 29; FOLLOW_X_SPEED = 30; FOLLOW_Y_SPEED = 31
    FOLLOW_X_OFFSET = 32; FOLLOW_Y_OFFSET = 33; FOLLOW_X_MODULO = 34
    FOLLOW_Y_MODULO = 35; FOLLOW_X_AMOUNT = 36; FOLLOW_Y_AMOUNT = 37
    TEXT_STRING = 38; FONT_SCALE = 39; ANCHOR_X = 40; ANCHOR_Y = 41
    ENABLE_GRADIENT = 42; GRADIENT_ANGLE = 43; COPY_COLOR_1 = 44; COPY_COLOR_2 = 45
    COPY_OPACITY = 46; COPY_BLENDING = 47; EDITOR_LAYER_1 = 48; EDITOR_LAYER_2 = 49
    EDITOR_LAYERS = 50; VISIBLE_IN_EDITOR = 51; DONT_ENTER = 52; DONT_FADE_IN = 53
    HIDE_IN_EDITOR = 54; RENDER_MARKER = 55; RENDER_Z = 56; OBJECT_STRING = 57
    OBJECT_TAG = 58

class BlockType(IntEnum):
    SOLID_BLOCK = 1; PLATFORM = 2; SPIKE = 3
    ORB_YELLOW = 4; ORB_BLUE = 5; ORB_GREEN = 6; ORB_RED = 7; ORB_PURPLE = 8; ORB_DASH = 9
    PAD_YELLOW = 10; PAD_PINK = 11; PAD_RED = 12; PAD_GREEN = 13
    PORTAL_CUBE = 14; PORTAL_SHIP = 15; PORTAL_BALL = 16; PORTAL_UFO = 17; PORTAL_WAVE = 18
    PORTAL_ROBOT = 19; PORTAL_SPIDER = 20; PORTAL_SWING = 21; PORTAL_PLATFORMER = 22
    PORTAL_SPEED_05 = 23; PORTAL_SPEED_1 = 24; PORTAL_SPEED_2 = 25; PORTAL_SPEED_3 = 26; PORTAL_SPEED_4 = 27
    PORTAL_GRAVITY = 28; PORTAL_MIRROR = 29; PORTAL_SIZE_MINI = 30; PORTAL_SIZE_NORMAL = 31
    PORTAL_DUAL = 32; PORTAL_SOLO = 33; PORTAL_ROTATE_CW = 34; PORTAL_ROTATE_CCW = 35
    DECOR_SMALL_1 = 100; DECOR_SMALL_2 = 101; DECOR_MEDIUM_1 = 102; DECOR_LARGE_1 = 103
    GLOW_1 = 104; GLOW_2 = 105; PULSE_OBJECT = 106; RING_1 = 107; RING_2 = 108
    PARTICLE_1 = 109; SAW_1 = 110; SAW_2 = 111; BLOCK_SLOPE_1 = 112; BLOCK_SLOPE_2 = 113
    BLOCK_CORNER_1 = 114; BLOCK_CORNER_2 = 115
    TRIGGER_SPAWN = 1006; TRIGGER_TOUCH = 1007; TRIGGER_COUNT = 1008; TRIGGER_INSTANT_COUNT = 1009
    TRIGGER_PICKUP = 1010; TRIGGER_RANDOM = 1011; TRIGGER_TIMED = 1012; TRIGGER_FOLLOW_X = 1013
    TRIGGER_FOLLOW_Y = 1014; TRIGGER_ADVANCED_FOLLOW = 1015; TRIGGER_AREA_EFFECT = 1016
    TRIGGER_EVENT_LINK = 1017; TRIGGER_KEYFRAME = 1018; TRIGGER_ITEM_COMPARE = 1019
    TRIGGER_ITEM_EDIT = 1020; TRIGGER_OBJECT_CONTROL = 1021; TRIGGER_PLAYER_CONTROL = 1022
    TRIGGER_RESET = 1023; TRIGGER_SFX = 1024; TRIGGER_SONG = 1025; TRIGGER_TIMER = 1026
    TRIGGER_MOVE = 1200; TRIGGER_ROTATE = 1201; TRIGGER_SCALE = 1202; TRIGGER_COLOR = 1203
    TRIGGER_ALPHA = 1204; TRIGGER_PULSE = 1205; TRIGGER_HSV = 1206; TRIGGER_STOP = 1207
    TRIGGER_FOLLOW = 1208; TRIGGER_SHAKE = 1209; TRIGGER_ANIMATION = 1210; TRIGGER_TOGGLE = 1211
    TRIGGER_SPAWN_ORDER = 1212; TRIGGER_ORDER = 1213; TRIGGER_COLLISION = 1214
    TRIGGER_TEXT = 1215; TRIGGER_CUSTOM_RING = 1216

# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class GDObject:
    object_id: int; x: float = 0; y: float = 0; rotation: float = 0
    flip_x: bool = False; flip_y: bool = False; scale: float = 1.0
    groups: List[int] = field(default_factory=list); color_1: int = 0; color_2: int = 0
    z_order: int = 0; z_layer: int = 0; is_trigger: bool = False; target_group: int = 0
    trigger_type: int = 0; activate_group: List[int] = field(default_factory=list)
    deactivate_group: List[int] = field(default_factory=list); toggle_group: List[int] = field(default_factory=list)
    spawn_triggered: bool = False; touch_triggered: bool = False; multi_trigger: bool = False
    editor_layer_1: int = 0; editor_layer_2: int = 0; editor_layers: List[int] = field(default_factory=list)
    high_detail: bool = False; dont_fade: bool = False; hide_in_editor: bool = False
    text_string: str = ""; font_scale: float = 1.0; anchor_x: float = 0.5; anchor_y: float = 0.5
    enable_gradient: bool = False; gradient_angle: float = 0; copy_color_1: int = 0
    copy_color_2: int = 0; copy_opacity: int = 0; copy_blending: int = 0
    follow_player_x: bool = False; follow_player_y: bool = False; follow_x_speed: float = 1.0
    follow_y_speed: float = 1.0; follow_x_offset: float = 0; follow_y_offset: float = 0
    follow_x_modulo: float = 0; follow_y_modulo: float = 0; follow_x_amount: float = 1.0
    follow_y_amount: float = 1.0; move_x: float = 0; move_y: float = 0
    rotate_degrees: float = 0; scale_multiplier: float = 1.0; pulse_hsv: Tuple[float, float, float] = (0, 0, 0)
    pulse_duration: float = 1.0; pulse_easing: int = 0; color_hsv: Tuple[float, float, float] = (0, 0, 0)
    color_duration: float = 1.0; alpha_value: float = 1.0; alpha_duration: float = 1.0
    shake_strength: float = 0; shake_interval: float = 0; animation_id: int = 0
    collision_block_id: int = 0; spawn_order_group: int = 0; order_amount: int = 0
    custom_ring_id: int = 0
    
    def to_dict(self) -> Dict[int, Any]:
        d = {ObjectKey.OBJECT_ID: self.object_id, ObjectKey.X: round(self.x, 3), ObjectKey.Y: round(self.y, 3)}
        if self.rotation != 0: d[ObjectKey.ROTATION] = round(self.rotation, 3)
        if self.flip_x: d[ObjectKey.FLIP_X] = 1
        if self.flip_y: d[ObjectKey.FLIP_Y] = 1
        if self.scale != 1.0: d[ObjectKey.SCALE] = round(self.scale, 3)
        if self.groups: d[ObjectKey.GROUPS] = ','.join(str(g) for g in self.groups)
        if self.color_1 != 0: d[ObjectKey.COLOR_1] = self.color_1
        if self.color_2 != 0: d[ObjectKey.COLOR_2] = self.color_2
        if self.z_order != 0: d[ObjectKey.Z_ORDER] = self.z_order
        if self.z_layer != 0: d[ObjectKey.Z_LAYER] = self.z_layer
        if self.is_trigger: d[ObjectKey.IS_TRIGGER] = 1
        if self.target_group != 0: d[ObjectKey.TARGET_GROUP] = self.target_group
        if self.activate_group: d[ObjectKey.ACTIVATE_GROUP] = ','.join(str(g) for g in self.activate_group)
        if self.deactivate_group: d[ObjectKey.DEACTIVATE_GROUP] = ','.join(str(g) for g in self.deactivate_group)
        if self.toggle_group: d[ObjectKey.TOGGLE_GROUP] = ','.join(str(g) for g in self.toggle_group)
        if self.spawn_triggered: d[ObjectKey.SPAWN_TRIGGERED] = 1
        if self.touch_triggered: d[ObjectKey.TOUCH_TRIGGERED] = 1
        if self.multi_trigger: d[ObjectKey.MULTI_TRIGGER] = 1
        if self.trigger_type != 0: d[ObjectKey.TRIGGER_TYPE] = self.trigger_type
        if self.editor_layer_1 != 0: d[ObjectKey.EDITOR_LAYER_1] = self.editor_layer_1
        if self.editor_layer_2 != 0: d[ObjectKey.EDITOR_LAYER_2] = self.editor_layer_2
        if self.editor_layers: d[ObjectKey.EDITOR_LAYERS] = ','.join(str(l) for l in self.editor_layers)
        if self.high_detail: d[ObjectKey.HIGH_DETAIL] = 1
        if self.dont_fade: d[ObjectKey.DONT_FADE] = 1
        if self.hide_in_editor: d[ObjectKey.HIDE_IN_EDITOR] = 1
        if self.text_string: d[ObjectKey.TEXT_STRING] = self.text_string
        if self.font_scale != 1.0: d[ObjectKey.FONT_SCALE] = self.font_scale
        if self.anchor_x != 0.5: d[ObjectKey.ANCHOR_X] = self.anchor_x
        if self.anchor_y != 0.5: d[ObjectKey.ANCHOR_Y] = self.anchor_y
        if self.enable_gradient: d[ObjectKey.ENABLE_GRADIENT] = 1
        if self.gradient_angle != 0: d[ObjectKey.GRADIENT_ANGLE] = self.gradient_angle
        if self.copy_color_1 != 0: d[ObjectKey.COPY_COLOR_1] = self.copy_color_1
        if self.copy_color_2 != 0: d[ObjectKey.COPY_COLOR_2] = self.copy_color_2
        if self.copy_opacity != 0: d[ObjectKey.COPY_OPACITY] = self.copy_opacity
        if self.copy_blending != 0: d[ObjectKey.COPY_BLENDING] = self.copy_blending
        if self.follow_player_x: d[ObjectKey.FOLLOW_PLAYER_X] = 1
        if self.follow_player_y: d[ObjectKey.FOLLOW_PLAYER_Y] = 1
        if self.follow_x_speed != 1.0: d[ObjectKey.FOLLOW_X_SPEED] = self.follow_x_speed
        if self.follow_y_speed != 1.0: d[ObjectKey.FOLLOW_Y_SPEED] = self.follow_y_speed
        if self.follow_x_offset != 0: d[ObjectKey.FOLLOW_X_OFFSET] = self.follow_x_offset
        if self.follow_y_offset != 0: d[ObjectKey.FOLLOW_Y_OFFSET] = self.follow_y_offset
        if self.follow_x_modulo != 0: d[ObjectKey.FOLLOW_X_MODULO] = self.follow_x_modulo
        if self.follow_y_modulo != 0: d[ObjectKey.FOLLOW_Y_MODULO] = self.follow_y_modulo
        if self.follow_x_amount != 1.0: d[ObjectKey.FOLLOW_X_AMOUNT] = self.follow_x_amount
        if self.follow_y_amount != 1.0: d[ObjectKey.FOLLOW_Y_AMOUNT] = self.follow_y_amount
        return d

@dataclass
class LevelSection:
    name: str; start_x: float; end_x: float; game_mode: str; difficulty: str
    objects: List[GDObject] = field(default_factory=list)
    triggers: List[GDObject] = field(default_factory=list)
    decoration: List[GDObject] = field(default_factory=list)
    bg_color: Tuple[int, int, int] = (0, 0, 0); ground_color: Tuple[int, int, int] = (0, 0, 0)

# ============================================================
# LEVEL GENERATOR - MAXIMUM DENSITY
# ============================================================

class MasterpieceLevelGenerator:
    def __init__(self, song_id: int = 624012, level_name: str = "MASTERPIECE", author: str = "Kilo"):
        self.song_id = song_id; self.level_name = level_name; self.author = author
        self.objects: List[GDObject] = []; self.sections: List[LevelSection] = []
        self.next_group = 1000; self.next_color = 1000; self.object_count = 0
        self.section_width = 2500; self.spacing = 12
        
        self.level_version = 47; self.game_version = 22; self.difficulty = 4
        self.demon_difficulty = 3; self.stars = 10; self.featured = 0; self.epic = 1
        self.coins = 3; self.length = 5; self.two_player = 0; self.auto = 0
        self.password = 0; self.original = 0; self.unlisted = 0; self.friends_only = 0
        
    def ng(self) -> int: g = self.next_group; self.next_group += 1; return g
    def nc(self) -> int: c = self.next_color; self.next_color += 1; return c
    
    def add(self, obj: GDObject): self.objects.append(obj); self.object_count += 1
    def adds(self, objs: List[GDObject]): self.objects.extend(objs); self.object_count += len(objs)
    
    # --- Object Factories ---
    def P(self, x, y, t, g=None): return GDObject(object_id=t, x=x, y=y, groups=g or [])
    def O(self, x, y, t, g=None): return GDObject(object_id=t, x=x, y=y, groups=g or [])
    def PD(self, x, y, t, g=None): return GDObject(object_id=t, x=x, y=y, groups=g or [])
    def B(self, x, y, t, r=0, s=1, fx=False, fy=False, g=None, c1=0, c2=0, zo=0, zl=0, hd=False):
        return GDObject(object_id=t, x=x, y=y, rotation=r, scale=s, flip_x=fx, flip_y=fy,
                       groups=g or [], color_1=c1, color_2=c2, z_order=zo, z_layer=zl, high_detail=hd)
    def S(self, x, y, r=0, s=1, g=None, c1=0, c2=0):
        return GDObject(object_id=BlockType.SPIKE, x=x, y=y, rotation=r, scale=s, groups=g or [], color_1=c1, color_2=c2)
    
    def T(self, x, y, tt, tg, ag=None, dg=None, tg2=None, st=False, tt2=False, mt=False, g=None):
        return GDObject(object_id=tt, x=x, y=y, is_trigger=True, target_group=tg,
                       activate_group=ag or [], deactivate_group=dg or [], toggle_group=tg2 or [],
                       spawn_triggered=st, touch_triggered=tt2, multi_trigger=mt, groups=g or [])
    
    def MT(self, x, y, tg, mx, my, d=1, e=0, st=False, tt=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_MOVE, x=x, y=y, is_trigger=True, target_group=tg,
                       move_x=mx, move_y=my, spawn_triggered=st, touch_triggered=tt, groups=g or [])
    
    def RT(self, x, y, tg, deg, d=1, e=0, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_ROTATE, x=x, y=y, is_trigger=True, target_group=tg,
                       rotate_degrees=deg, spawn_triggered=st, groups=g or [])
    
    def SCT(self, x, y, tg, mult, d=1, e=0, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_SCALE, x=x, y=y, is_trigger=True, target_group=tg,
                       scale_multiplier=mult, spawn_triggered=st, groups=g or [])
    
    def CT(self, x, y, tg, hsv, d=1, e=0, c1=0, c2=0, co=0, cb=0, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_COLOR, x=x, y=y, is_trigger=True, target_group=tg,
                       color_hsv=hsv, copy_color_1=c1, copy_color_2=c2, copy_opacity=co, copy_blending=cb,
                       spawn_triggered=st, groups=g or [])
    
    def PT(self, x, y, tg, hsv, d=1, e=0, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_PULSE, x=x, y=y, is_trigger=True, target_group=tg,
                       pulse_hsv=hsv, pulse_duration=d, pulse_easing=e, spawn_triggered=st, groups=g or [])
    
    def AT(self, x, y, tg, alpha, d=1, e=0, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_ALPHA, x=x, y=y, is_trigger=True, target_group=tg,
                       alpha_value=alpha, alpha_duration=d, spawn_triggered=st, groups=g or [])
    
    def HT(self, x, y, tg, hsv, d=1, e=0, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_HSV, x=x, y=y, is_trigger=True, target_group=tg,
                       color_hsv=hsv, color_duration=d, spawn_triggered=st, groups=g or [])
    
    def FT(self, x, y, tg, fx=True, fy=True, xs=1, ys=1, xo=0, yo=0, xm=0, ym=0, xa=1, ya=1, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_FOLLOW, x=x, y=y, is_trigger=True, target_group=tg,
                       follow_player_x=fx, follow_player_y=fy, follow_x_speed=xs, follow_y_speed=ys,
                       follow_x_offset=xo, follow_y_offset=yo, follow_x_modulo=xm, follow_y_modulo=ym,
                       follow_x_amount=xa, follow_y_amount=ya, spawn_triggered=st, groups=g or [])
    
    def ST(self, x, y, tg, strg, ivl, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_SHAKE, x=x, y=y, is_trigger=True, target_group=tg,
                       shake_strength=strg, shake_interval=ivl, spawn_triggered=st, groups=g or [])
    
    def ANT(self, x, y, tg, aid, st=False, g=None):
        return GDObject(object_id=BlockType.TRIGGER_ANIMATION, x=x, y=y, is_trigger=True, target_group=tg,
                       animation_id=aid, spawn_triggered=st, groups=g or [])
    
    def SpT(self, x, y, tg, delay=0, st=True, g=None):
        return GDObject(object_id=BlockType.TRIGGER_SPAWN, x=x, y=y, is_trigger=True, target_group=tg,
                       spawn_triggered=st, groups=g or [])
    
    def TT(self, x, y, tg, ag=None, dg=None, tg2=None, g=None):
        return GDObject(object_id=BlockType.TRIGGER_TOUCH, x=x, y=y, is_trigger=True, target_group=tg,
                       activate_group=ag or [], deactivate_group=dg or [], toggle_group=tg2 or [],
                       touch_triggered=True, groups=g or [])
    
    def D(self, x, y, t, r=0, s=1, fx=False, fy=False, c1=0, c2=0, zo=0, zl=0, g=None, hd=False, el1=0, el2=0):
        return GDObject(object_id=t, x=x, y=y, rotation=r, scale=s, flip_x=fx, flip_y=fy,
                       color_1=c1, color_2=c2, z_order=zo, z_layer=zl, groups=g or [],
                       high_detail=hd, editor_layer_1=el1, editor_layer_2=el2)

    # --- Dense Systems ---
    
    def dense_ground(self, sec: LevelSection, layers=5):
        w = sec.end_x - sec.start_x; segs = int(w / self.spacing)
        for i in range(segs):
            x = sec.start_x + i * self.spacing; y = 15
            for L in range(layers):
                ly = y - 15 - L * 25
                self.adds([self.B(x, ly, BlockType.SOLID_BLOCK, c1=self.nc(), c2=self.nc(),
                                hd=(L < 2), zl=-1 - L)])
            if i % 2 == 0:
                self.adds([self.D(x + 6, y - 12 + random.uniform(-3, 3),
                                random.choice([BlockType.DECOR_SMALL_1, BlockType.DECOR_SMALL_2]),
                                s=random.uniform(0.3, 0.7), r=random.uniform(0, 360),
                                c1=self.nc(), zl=-2)])
            if i % 4 == 0:
                self.adds([self.S(x + 6, y - 15, r=180, s=0.5, c1=self.nc(), c2=self.nc())])
    
    def dense_ceiling(self, sec: LevelSection, h=110, layers=3):
        w = sec.end_x - sec.start_x; segs = int(w / self.spacing)
        for i in range(segs):
            x = sec.start_x + i * self.spacing; y = 15 + h
            for L in range(layers):
                ly = y + L * 25
                self.adds([self.B(x, ly, BlockType.SOLID_BLOCK, r=180, c1=self.nc(), c2=self.nc(),
                                hd=(L < 1), zl=-1 - L)])
    
    def bg_3d_layers(self, sec: LevelSection, n=12):
        w = sec.end_x - sec.start_x
        for L in range(n):
            z = -15 - L * 4; par = 1.0 - L * 0.08; sc = 2.5 + L * 0.5
            cnt = int(w / (35 * par))
            for i in range(cnt + 3):
                x = sec.start_x + i * 35 * par - 40
                y = 15 + math.sin(i * 0.06 + L * 0.4) * 80 * par
                tid = random.choice([BlockType.DECOR_LARGE_1, BlockType.DECOR_MEDIUM_1, BlockType.GLOW_2, BlockType.RING_1])
                self.adds([self.D(x, y, tid, s=sc * random.uniform(0.7, 1.3), r=random.uniform(0, 360),
                                c1=self.nc(), c2=self.nc(), zl=z, hd=(L < 4))])
                if L < 5 and random.random() < 0.4:
                    self.adds([self.D(x + random.uniform(-25, 25), y + random.uniform(-25, 25),
                                    BlockType.GLOW_1, s=sc * 0.4 * random.uniform(0.5, 1.5),
                                    c1=self.nc(), zl=z - 1)])
    
    def fg_art_dense(self, sec: LevelSection):
        w = sec.end_x - sec.start_x; cnt = int(w / 15)
        for i in range(cnt):
            x = sec.start_x + i * 15 + random.uniform(-8, 8)
            y = 15 + random.uniform(-50, 130)
            if random.random() < 0.5:
                g = self.ng()
                self.adds([self.D(x, y, random.choice([BlockType.RING_1, BlockType.RING_2]),
                                s=random.uniform(0.4, 2.0), r=random.uniform(0, 360),
                                c1=self.nc(), c2=self.nc(), zl=2, g=[g])])
                self.adds([self.PT(sec.start_x, 15, g, hsv=(random.random(), 0.85, 1.0),
                                 d=random.uniform(1, 5), st=True)])
            if random.random() < 0.3:
                self.adds([self.D(x, y, random.choice([BlockType.SAW_1, BlockType.SAW_2]),
                                s=random.uniform(0.3, 1.2), c1=self.nc(), zl=1)])
            if random.random() < 0.6:
                for _ in range(random.randint(2, 8)):
                    self.adds([self.D(x + random.uniform(-18, 18), y + random.uniform(-18, 18),
                                    BlockType.PARTICLE_1, s=random.uniform(0.06, 0.3),
                                    c1=self.nc(), zl=3)])
            if random.random() < 0.4:
                self.adds([self.D(x, y, random.choice([BlockType.GLOW_1, BlockType.GLOW_2]),
                                s=random.uniform(0.5, 1.8), c1=self.nc(), c2=self.nc(), zl=2)])
            if random.random() < 0.4:
                self.adds([self.D(x, y, random.choice([BlockType.DECOR_SMALL_1, BlockType.DECOR_SMALL_2]),
                                s=random.uniform(0.2, 0.7), r=random.uniform(0, 360), c1=self.nc(), zl=1)])
    
    def pulse_dense(self, sec: LevelSection, bpm=150):
        bi = 60.0 / bpm * self.spacing; ng = 12
        gs = [self.ng() for _ in range(ng)]
        all_objs = sec.objects + sec.decoration
        for i, o in enumerate(all_objs):
            if not o.is_trigger and o.z_layer >= -2:
                o.groups.append(gs[i % ng])
        x = sec.start_x; beat = 0
        while x < sec.end_x:
            for gi, g in enumerate(gs):
                h = (gi/ng + beat*0.015 + x*0.0003) % 1.0
                self.adds([self.PT(x, 15, g, hsv=(h, 0.9, 1.0), d=bi/self.spacing*0.5, e=1, st=True)])
            x += bi; beat += 1
        x = sec.start_x + bi/2; beat = 0
        while x < sec.end_x:
            for gi, g in enumerate(gs):
                h = (gi/ng + beat*0.015 + x*0.0003 + 0.5) % 1.0
                self.adds([self.PT(x, 15, g, hsv=(h, 0.65, 0.85), d=bi/self.spacing*0.4, e=2, st=True)])
            x += bi; beat += 1
    
    def colors_dense(self, sec: LevelSection, base_hue: float):
        pal = []
        for i in range(40):
            h = (base_hue + i*0.025 + random.uniform(-0.015, 0.015)) % 1.0
            pal.append((h, 0.65 + random.random()*0.35, 0.5 + random.random()*0.5))
        for o in sec.objects + sec.decoration:
            if o.color_1 == 0 and not o.is_trigger:
                c = random.choice(pal); o.color_1 = self.nc(); o.color_hsv = c
        for i in range(0, int(sec.end_x - sec.start_x), 80):
            x = sec.start_x + i
            for o in sec.objects[:8]:
                if o.color_1 > 0:
                    self.adds([self.CT(x, 15, o.color_1, o.color_hsv, d=0.1, st=True)])
    
    def adv_triggers_dense(self, sec: LevelSection):
        for chain in range(10):
            g = self.ng()
            for _ in range(10):
                x = sec.start_x + random.uniform(0, sec.end_x - sec.start_x)
                y = 15 + random.uniform(-40, 120)
                self.adds([self.D(x, y, random.choice([BlockType.DECOR_MEDIUM_1, BlockType.DECOR_LARGE_1, BlockType.GLOW_2, BlockType.RING_1]),
                                s=random.uniform(0.5, 1.8), r=random.uniform(0, 360), c1=self.nc(), g=[g], zl=1)])
            self.adds([self.MT(sec.start_x, 15, g, random.uniform(-60, 60), random.uniform(-50, 50),
                              d=random.uniform(3, 10), e=random.randint(0, 3), st=True)])
            self.adds([self.RT(sec.start_x + 60, 15, g, 360 * random.uniform(0.2, 3),
                              d=random.uniform(5, 15), e=random.randint(0, 2), st=True)])
            self.adds([self.SCT(sec.start_x + 120, 15, g, random.uniform(0.6, 1.5),
                               d=random.uniform(2, 6), e=random.randint(0, 2), st=True)])
            self.adds([self.HT(sec.start_x + 180, 15, g, (random.random(), 0.85, 1.0),
                              d=random.uniform(6, 20), e=random.randint(0, 2), st=True)])
            self.adds([self.AT(sec.start_x + 240, 15, g, random.uniform(0.2, 1.0),
                              d=random.uniform(2, 5), e=random.randint(0, 2), st=True)])
        
        for chain in range(5):
            g = self.ng()
            for i in range(6):
                x = sec.start_x + i * 180 + random.uniform(-40, 40)
                y = 15 + 60 + random.uniform(-30, 30)
                self.adds([self.D(x, y, random.choice([BlockType.GLOW_1, BlockType.GLOW_2, BlockType.RING_1, BlockType.PULSE_OBJECT]),
                                s=random.uniform(1.0, 2.5), c1=self.nc(), g=[g], zl=2)])
            self.adds([self.FT(sec.start_x, 15, g, True, True,
                              random.uniform(0.1, 0.6), random.uniform(0.1, 0.5),
                              random.uniform(-30, 30), random.uniform(-30, 30), st=True)])
        
        bi = 60.0 / 150 * self.spacing * 4
        x = sec.start_x
        while x < sec.end_x:
            self.adds([self.ST(x, 15, self.ng(), random.uniform(1.5, 5.0), 0.05, st=True)])
            x += bi
        
        for i in range(5):
            g = self.ng()
            for _ in range(4):
                x = sec.start_x + random.uniform(0, sec.end_x - sec.start_x)
                y = 15 + random.uniform(-30, 100)
                self.adds([self.D(x, y, BlockType.PULSE_OBJECT, s=random.uniform(0.8, 1.8), c1=self.nc(), g=[g], zl=1)])
            self.adds([self.ANT(sec.start_x + i * 250, 15, g, random.randint(1, 5), st=True)])
    
    def moving_platforms_dense(self, sec: LevelSection, cnt=25):
        w = sec.end_x - sec.start_x
        for i in range(cnt):
            x = sec.start_x + i * (w / cnt) + random.uniform(-30, 30)
            y = 15 + random.uniform(15, 100)
            g = self.ng()
            self.adds([self.B(x, y, BlockType.PLATFORM, s=random.uniform(0.5, 1.3), c1=self.nc(), g=[g])])
            mt = random.randint(0, 5)
            if mt == 0:
                self.adds([self.MT(sec.start_x, 15, g, random.uniform(-50, 50), 0, d=random.uniform(2, 5), e=1, st=True)])
            elif mt == 1:
                self.adds([self.MT(sec.start_x, 15, g, 0, random.uniform(-40, 40), d=random.uniform(2, 5), e=1, st=True)])
            elif mt == 2:
                self.adds([self.MT(sec.start_x, 15, g, random.uniform(-35, 35), random.uniform(-35, 35),
                                  d=random.uniform(3, 7), e=2, st=True)])
                self.adds([self.RT(sec.start_x + 60, 15, g, 360, d=random.uniform(5, 10), st=True)])
            elif mt == 3:
                self.adds([self.MT(sec.start_x, 15, g, random.uniform(-40, 40), random.uniform(-30, 30),
                                  d=random.uniform(4, 9), e=3, st=True)])
            elif mt == 4:
                self.adds([self.MT(sec.start_x, 15, g, random.uniform(-30, 30), 0, d=random.uniform(2, 4), e=1, st=True)])
                self.adds([self.MT(sec.start_x + 100, 15, g, 0, random.uniform(-25, 25), d=random.uniform(2, 4), e=2, st=True)])
            else:
                self.adds([self.MT(sec.start_x, 15, g, random.uniform(-60, 60), random.uniform(-50, 50),
                                  d=random.uniform(3, 8), e=random.randint(0, 3), st=True)])

    # --- Section Builders ---
    
    def build_intro(self, sx: float) -> LevelSection:
        sec = LevelSection("Intro - Atmospheric", sx, sx + self.section_width, "cube", "Easy",
                          bg_color=(10,5,20), ground_color=(30,15,50))
        x, y = sx, 15
        self.adds([self.P(x, y, BlockType.PORTAL_CUBE), self.P(x, y, BlockType.PORTAL_SPEED_1)])
        x += 60
        pl = int(self.section_width / self.spacing)
        for i in range(pl):
            bx = x + i * self.spacing
            for L in range(5):
                ly = y - 15 - L * 25
                self.adds([self.B(bx, ly, BlockType.SOLID_BLOCK, c1=self.nc(), c2=self.nc(),
                                hd=(L<3), zl=-1-L)])
            if i % 3 == 0:
                g = self.ng()
                self.adds([self.B(bx+6, y+40+math.sin(i*0.4)*30, BlockType.PLATFORM, s=0.8,
                                c1=self.nc(), g=[g])])
                self.adds([self.MT(bx, y-30, g, 0, math.sin(i)*20, d=5, st=True)])
            if i % 4 == 1:
                self.adds([self.O(bx+6, y+55+math.sin(i*0.3)*25, BlockType.ORB_YELLOW)])
            if i % 4 == 3:
                self.adds([self.O(bx+6, y+75+math.sin(i*0.5)*20, BlockType.ORB_BLUE)])
            if i % 2 == 0:
                self.adds([self.D(bx+6, y-8, random.choice([BlockType.DECOR_SMALL_1, BlockType.DECOR_SMALL_2]),
                                s=0.5, r=i*12, c1=self.nc(), zl=-2)])
        sec.end_x = x + pl * self.spacing
        return sec
    
    def build_section(self, sx: float, name: str, mode: str, portal: int, speed: int, diff: str,
                      bg: Tuple, gr: Tuple, patterns=16, extra_portals=[]) -> LevelSection:
        sec = LevelSection(name, sx, sx + self.section_width, mode, diff, bg_color=bg, ground_color=gr)
        x, y = sx, 15
        self.adds([self.P(x, y, portal), self.P(x, y, speed)] + [self.P(x, y, p) for p in extra_portals])
        x += 60
        pl = int(self.section_width / self.spacing)
        
        for i in range(pl):
            bx = x + i * self.spacing
            for L in range(4):
                ly = y - 15 - L * 25
                self.adds([self.B(bx, ly, BlockType.SOLID_BLOCK, c1=self.nc(), c2=self.nc(),
                                hd=(L<2), zl=-1-L)])
            if mode in ["ship","ball","ufo","wave","spider"]:
                for L in range(3):
                    ly = y + 110 + L * 25
                    self.adds([self.B(bx, ly, BlockType.SOLID_BLOCK, r=180, c1=self.nc(), c2=self.nc(),
                                    hd=(L<1), zl=-1-L)])
            
            p = i % patterns
            if mode == "cube":
                if p == 0: self.adds([self.O(bx+6, y+30, BlockType.ORB_YELLOW)])
                elif p == 2: self.adds([self.O(bx+6, y+45, BlockType.ORB_BLUE)])
                elif p == 4: self.adds([self.O(bx+6, y+30, BlockType.ORB_GREEN)])
                elif p == 6: self.adds([self.PD(bx+6, y-15, BlockType.PAD_YELLOW)])
                elif p == 8: self.adds([self.PD(bx+6, y-15, BlockType.PAD_PINK)])
                elif p == 10: self.adds([self.O(bx+6, y+60, BlockType.ORB_RED)])
                elif p == 12: self.adds([self.O(bx+6, y+30, BlockType.ORB_PURPLE)])
                elif p == 14: self.adds([self.O(bx+6, y+45, BlockType.ORB_DASH)])
                elif p in [1,5,9,13]: self.adds([self.P(bx+6, y+15, BlockType.PORTAL_GRAVITY)])
                elif p in [3,7,11,15]: self.adds([self.P(bx+6, y+15, BlockType.PORTAL_MIRROR)])
            elif mode == "ship":
                if p % 3 == 1:
                    g = self.ng()
                    self.adds([self.B(bx+6, y+35+math.sin(i*0.4)*35, BlockType.SOLID_BLOCK, s=0.7,
                                    r=random.choice([0,90,180,270]), c1=self.nc(), g=[g])])
                    self.adds([self.MT(bx, y-30, g, 0, math.sin(i)*25, d=4, st=True)])
                if p % 5 == 0: self.adds([self.O(bx+6, y+25, BlockType.ORB_YELLOW)])
                if p % 7 == 0: self.adds([self.P(bx+6, y+45, BlockType.PORTAL_GRAVITY)])
            elif mode == "ball":
                if p % 4 == 0: self.adds([self.P(bx+6, y+40, BlockType.PORTAL_GRAVITY)])
                if p % 3 == 1: self.adds([self.O(bx+6, y+20, BlockType.ORB_BLUE)])
                if p % 3 == 2: self.adds([self.O(bx+6, y+60, BlockType.ORB_RED)])
                if p % 5 == 0:
                    g = self.ng()
                    self.adds([self.B(bx+6, y+40, BlockType.PLATFORM, s=0.7, c1=self.nc(), g=[g])])
                    self.adds([self.MT(bx, y-30, g, 0, 25, d=3, e=1, st=True)])
            elif mode == "ufo":
                if p % 2 == 0:
                    g = self.ng()
                    self.adds([self.B(bx+6, y+45+math.sin(i*0.3)*30, BlockType.SOLID_BLOCK, s=0.6,
                                    c1=self.nc(), g=[g])])
                if p % 3 == 1: self.adds([self.O(bx+6, y+20, BlockType.ORB_YELLOW)])
                if p % 3 == 2: self.adds([self.O(bx+6, y+80, BlockType.ORB_BLUE)])
            elif mode == "wave":
                if p % 8 == 3: self.adds([self.P(bx+6, y+15, BlockType.PORTAL_SIZE_MINI)])
                if p % 8 == 7: self.adds([self.P(bx+6, y+15, BlockType.PORTAL_SIZE_NORMAL)])
            elif mode == "robot":
                if p % 3 == 0: self.adds([self.B(bx+6, y+35, BlockType.PLATFORM, s=0.9, c1=self.nc())])
                elif p % 3 == 1: self.adds([self.B(bx+6, y+60, BlockType.PLATFORM, s=0.7, c1=self.nc())])
                elif p % 3 == 2: self.adds([self.B(bx+6, y+20, BlockType.PLATFORM, s=0.8, c1=self.nc())])
                if p % 4 == 1: self.adds([self.O(bx+6, y+50, BlockType.ORB_YELLOW)])
                if p % 4 == 3: self.adds([self.O(bx+6, y+75, BlockType.ORB_BLUE)])
            elif mode == "spider":
                if p % 2 == 0: self.adds([self.B(bx+6, y+40, BlockType.SOLID_BLOCK, s=0.6, c1=self.nc())])
                if p % 3 == 1: self.adds([self.O(bx+6, y+20, BlockType.ORB_YELLOW)])
                if p % 3 == 2: self.adds([self.O(bx+6, y+70, BlockType.ORB_BLUE)])
            elif mode == "swing":
                if p % 2 == 0:
                    g = self.ng()
                    self.adds([self.B(bx+6, y+55, BlockType.SOLID_BLOCK, s=0.4, c1=self.nc(), g=[g])])
                if p % 3 == 1: self.adds([self.O(bx+6, y+35, BlockType.ORB_YELLOW)])
            elif mode == "platformer":
                if p % 3 == 0: self.adds([self.B(bx, y-15, BlockType.SOLID_BLOCK, s=3, c1=self.nc(), hd=True)])
                if p % 2 == 1:
                    py = y + 25 + (p%4)*25
                    g = self.ng()
                    self.adds([self.B(bx+6, py, BlockType.PLATFORM, s=1, c1=self.nc(), g=[g])])
                    self.adds([self.MT(bx, y-30, g, 25, 0, d=3, st=True)])
                if p % 4 == 2: self.adds([self.O(bx+6, y+40, BlockType.ORB_YELLOW)])
            
            if i % 1 == 0:
                self.adds([self.D(bx+6, y+random.uniform(-15, 90),
                                random.choice([BlockType.GLOW_1, BlockType.GLOW_2, BlockType.RING_1, BlockType.PARTICLE_1]),
                                s=random.uniform(0.4, 1.6), c1=self.nc(), c2=self.nc(), zl=random.randint(1,3))])
            if i % 2 == 0:
                self.adds([self.S(bx+6, y-15, r=180, s=0.5, c1=self.nc(), c2=self.nc())])
        
        sec.end_x = x + pl * self.spacing
        return sec
    
    def build_cube1(self, sx): return self.build_section(sx, "Cube 1 - Flow", "cube",
        BlockType.PORTAL_CUBE, BlockType.PORTAL_SPEED_2, "Easy Demon",
        (20,10,40), (50,25,80), 20)
    
    def build_ship(self, sx): return self.build_section(sx, "Ship - Corridors", "ship",
        BlockType.PORTAL_SHIP, BlockType.PORTAL_SPEED_3, "Medium Demon",
        (30,15,50), (60,30,90), 16)
    
    def build_ball(self, sx): return self.build_section(sx, "Ball - Gravity", "ball",
        BlockType.PORTAL_BALL, BlockType.PORTAL_SPEED_2, "Medium Demon",
        (15,30,40), (40,60,80), 16)
    
    def build_ufo(self, sx): return self.build_section(sx, "UFO - Precision", "ufo",
        BlockType.PORTAL_UFO, BlockType.PORTAL_SPEED_2, "Easy-Medium Demon",
        (25,20,45), (50,40,85), 16)
    
    def build_wave(self, sx): return self.build_section(sx, "Wave - Tight", "wave",
        BlockType.PORTAL_WAVE, BlockType.PORTAL_SPEED_3, "Medium Demon",
        (35,10,50), (70,20,90), 16)
    
    def build_robot(self, sx): return self.build_section(sx, "Robot - Holds", "robot",
        BlockType.PORTAL_ROBOT, BlockType.PORTAL_SPEED_2, "Medium Demon",
        (20,35,45), (45,70,85), 16)
    
    def build_spider(self, sx): return self.build_section(sx, "Spider - Teleport", "spider",
        BlockType.PORTAL_SPIDER, BlockType.PORTAL_SPEED_2, "Medium Demon",
        (30,20,55), (60,40,95), 16)
    
    def build_swing(self, sx): return self.build_section(sx, "Swing - Momentum", "swing",
        BlockType.PORTAL_SWING, BlockType.PORTAL_SPEED_2, "Easy Demon",
        (25,25,50), (55,50,90), 16)
    
    def build_platformer(self, sx): return self.build_section(sx, "Platformer - Precision", "platformer",
        BlockType.PORTAL_PLATFORMER, BlockType.PORTAL_SPEED_1, "Easy Demon",
        (15,25,40), (35,50,75), 16)
    
    def build_final(self, sx: float) -> LevelSection:
        sec = LevelSection("Final Cube - Climax", sx, sx + int(self.section_width*1.5), "cube", "Medium Demon",
                          bg_color=(50,10,60), ground_color=(90,20,100))
        x, y = sx, 15
        self.adds([self.P(x, y, BlockType.PORTAL_CUBE), self.P(x, y, BlockType.PORTAL_SPEED_4)])
        x += 60
        pl = int(self.section_width * 1.5 / self.spacing)
        for i in range(pl):
            bx = x + i * self.spacing
            for L in range(5):
                ly = y - 15 - L * 25
                self.adds([self.B(bx, ly, BlockType.SOLID_BLOCK, c1=self.nc(), c2=self.nc(),
                                hd=True, zl=-1-L)])
            p = i % 24
            if p == 0: self.adds([self.O(bx+6, y+30, BlockType.ORB_YELLOW)])
            elif p == 1: self.adds([self.O(bx+6, y+45, BlockType.ORB_BLUE)])
            elif p == 2: self.adds([self.O(bx+6, y+30, BlockType.ORB_GREEN)])
            elif p == 3: self.adds([self.PD(bx+6, y-15, BlockType.PAD_YELLOW)])
            elif p == 4: self.adds([self.PD(bx+6, y-15, BlockType.PAD_PINK)])
            elif p == 5: self.adds([self.O(bx+6, y+65, BlockType.ORB_RED)])
            elif p == 6: self.adds([self.O(bx+6, y+30, BlockType.ORB_PURPLE)])
            elif p == 7: self.adds([self.O(bx+6, y+50, BlockType.ORB_DASH)])
            elif p == 8: self.adds([self.P(bx+6, y+15, BlockType.PORTAL_GRAVITY)])
            elif p == 9: self.adds([self.P(bx+6, y+15, BlockType.PORTAL_MIRROR)])
            elif p == 10: self.adds([self.P(bx+6, y+15, BlockType.PORTAL_SIZE_MINI)])
            elif p == 11: self.adds([self.P(bx+6, y+15, BlockType.PORTAL_SIZE_NORMAL)])
            elif p == 12:
                self.adds([self.O(bx+6, y+30, BlockType.ORB_YELLOW), self.O(bx+11, y+45, BlockType.ORB_BLUE)])
            elif p == 13:
                self.adds([self.PD(bx+6, y-15, BlockType.PAD_YELLOW), self.O(bx+11, y+30, BlockType.ORB_GREEN)])
            elif p == 14:
                self.adds([self.P(bx+6, y+15, BlockType.PORTAL_GRAVITY), self.P(bx+11, y+15, BlockType.PORTAL_MIRROR)])
            elif p == 15:
                self.adds([self.O(bx+6, y+50, BlockType.ORB_DASH), self.O(bx+11, y+65, BlockType.ORB_RED)])
            elif p == 16:
                self.adds([self.PD(bx+6, y-15, BlockType.PAD_PINK), self.O(bx+11, y+30, BlockType.ORB_PURPLE)])
            elif p == 17:
                self.adds([self.P(bx+6, y+15, BlockType.PORTAL_SIZE_MINI), self.P(bx+11, y+15, BlockType.PORTAL_GRAVITY)])
            elif p == 18:
                self.adds([self.P(bx+6, y+15, BlockType.PORTAL_SIZE_NORMAL), self.P(bx+11, y+15, BlockType.PORTAL_MIRROR)])
            elif p == 19:
                self.adds([self.O(bx+6, y+30, BlockType.ORB_YELLOW), self.O(bx+9, y+45, BlockType.ORB_BLUE), self.O(bx+12, y+60, BlockType.ORB_RED)])
            elif p == 20:
                self.adds([self.P(bx+6, y+15, BlockType.PORTAL_GRAVITY), self.P(bx+9, y+15, BlockType.PORTAL_MIRROR), self.P(bx+12, y+15, BlockType.PORTAL_SIZE_MINI)])
            elif p == 21:
                self.adds([self.O(bx+6, y+45, BlockType.ORB_DASH), self.O(bx+11, y+30, BlockType.ORB_PURPLE)])
            elif p == 22:
                self.adds([self.PD(bx+6, y-15, BlockType.PAD_YELLOW), self.PD(bx+11, y-15, BlockType.PAD_PINK)])
            elif p == 23:
                self.adds([self.P(bx+6, y+15, BlockType.PORTAL_SIZE_NORMAL), self.P(bx+11, y+15, BlockType.PORTAL_GRAVITY)])
            
            if i % 1 == 0:
                self.adds([self.D(bx+6, y+random.uniform(-10, 85),
                                random.choice([BlockType.GLOW_1, BlockType.GLOW_2, BlockType.RING_1, BlockType.RING_2, BlockType.SAW_1]),
                                s=random.uniform(0.5, 1.8), c1=self.nc(), c2=self.nc(), zl=random.randint(1,4))])
        self.adds([self.P(x + pl * self.spacing, y, BlockType.PORTAL_CUBE)])
        sec.end_x = x + pl * self.spacing
        return sec

    # --- Main Generation ---
    
    def generate(self) -> str:
        print("Generating MASTERPIECE level (MAX DENSITY)...")
        builders = [
            ("Intro", self.build_intro),
            ("Cube 1", self.build_cube1), ("Ship", self.build_ship), ("Ball", self.build_ball),
            ("UFO", self.build_ufo), ("Wave", self.build_wave), ("Robot", self.build_robot),
            ("Spider", self.build_spider), ("Swing", self.build_swing), ("Platformer", self.build_platformer),
            ("Final Cube", self.build_final),
        ]
        
        cx = 0
        for i, (name, fn) in enumerate(builders):
            print(f"  [{i+1:2}/{len(builders)}] {name}...")
            sec = fn(cx)
            
            print(f"      3D BG (12 layers)..."); self.bg_3d_layers(sec, 12)
            print(f"      FG Art..."); self.fg_art_dense(sec)
            print(f"      Pulse System..."); self.pulse_dense(sec, 150 + i*5)
            print(f"      Color Scheme..."); self.colors_dense(sec, i * 0.075)
            print(f"      Adv Triggers..."); self.adv_triggers_dense(sec)
            print(f"      Moving Platforms..."); self.moving_platforms_dense(sec, 30)
            print(f"      Ground/Ceiling..."); self.dense_ground(sec, 5); 
            if sec.game_mode in ["ship","ball","ufo","wave","spider"]: self.dense_ceiling(sec, 110, 4)
            
            self.adds(sec.objects); self.adds(sec.triggers); self.adds(sec.decoration)
            cx = sec.end_x + 100
            self.sections.append(sec)
            print(f"      DONE: Obj={len(sec.objects)} Trig={len(sec.triggers)} Dec={len(sec.decoration)} Total={self.object_count:,}")
        
        self.global_deco(); self.secret_coins()
        print(f"\nTOTAL OBJECTS: {self.object_count:,}")
        
        ls = self.encode(); return self.gdlvl(ls)
    
    def global_deco(self):
        for i, (txt, y, fs) in enumerate([
            (self.level_name, 240, 3.0),
            (f"By {self.author}", 205, 1.3),
            ("Easy-Medium Demon  ★★★★★★★★★★", 170, 1.0),
            ("v1.0  |  GD 2.2091  |  180k+ Objects", 135, 0.7),
            ("Song: Waterflame - Geometry Dash (NG:624012)", 100, 0.6),
        ]):
            self.add(GDObject(object_id=914, x=-200, y=y, text_string=txt, font_scale=fs,
                             color_1=self.nc(), z_layer=10, editor_layer_1=1))
    
    def secret_coins(self):
        for idx, si in enumerate([1, 4, 9]):
            if si < len(self.sections):
                s = self.sections[si]; w = s.end_x - s.start_x
                cx = s.start_x + w // 4 * (idx + 1); cy = 15 + 55 + idx * 25
                g = self.ng()
                self.add(self.TT(cx, cy, g, ag=[g]))
                self.add(self.D(cx, cy, 1048, s=1, c1=self.nc(), g=[g], zl=5))
                self.add(GDObject(object_id=BlockType.TRIGGER_ITEM_EDIT, x=cx, y=cy,
                                 is_trigger=True, target_group=g, groups=[g]))
    
    def encode(self) -> str:
        print("Encoding level string...")
        hdr = [f"kS38:{self.level_name}", f"kS39:{self.author}", f"kI40:{self.song_id}",
               f"kI41:{self.difficulty}", f"kI42:{self.demon_difficulty}", f"kI43:{self.stars}",
               f"kI44:{self.featured}", f"kI45:{self.epic}", f"kI46:{self.coins}",
               f"kI47:{self.length}", f"kI48:{self.two_player}", f"kI49:{self.auto}",
               f"kI50:{self.password}", f"kI51:{self.original}", f"kI52:{self.unlisted}",
               f"kI53:{self.friends_only}", f"kI54:{self.level_version}", f"kI55:{self.game_version}",
               f"kI56:{self.object_count}"]
        
        parts = []
        for o in self.objects:
            d = o.to_dict()
            if not d: continue
            pairs = []
            for k, v in sorted(d.items()):
                if isinstance(v, float): v = f"{v:.3f}".rstrip('0').rstrip('.')
                elif isinstance(v, bool): v = '1' if v else '0'
                pairs.append(f"{k},{v}")
            if pairs: parts.append(','.join(pairs))
        
        s = ';'.join(hdr) + ';' + ';'.join(parts) + ';'
        print(f"  Level string: {len(s):,} chars")
        return s
    
    def gdlvl(self, s: str) -> bytes:
        print("Creating .gdlvl...")
        c = gzip.compress(s.encode('utf-8'), compresslevel=9)
        e = base64.urlsafe_b64encode(c).decode('ascii')
        print(f"  Compressed: {len(c):,} bytes | Base64: {len(e):,} chars")
        return e.encode('ascii')
    
    def save(self, fn: str = "masterpiece.gdlvl"):
        data = self.generate()
        with open(fn, 'wb') as f: f.write(data)
        print(f"\nSaved: {fn}")
        print(f"Objects: {self.object_count:,} | Sections: {len(self.sections)}")
        print(f"Groups: {self.next_group-1000} | Colors: {self.next_color-1000}")
        
        meta = {"level_name": self.level_name, "author": self.author, "song_id": self.song_id,
                "difficulty": "Easy-Medium Demon", "object_count": self.object_count,
                "sections": len(self.sections), "groups": self.next_group-1000,
                "colors": self.next_color-1000,
                "game_modes": [s.game_mode for s in self.sections], "version": "2.2091"}
        with open(fn.replace('.gdlvl','_meta.json'), 'w') as f: json.dump(meta, f, indent=2)
        return fn


def main():
    print("="*60)
    print("GD MASTERPIECE LEVEL GENERATOR - MAX DENSITY")
    print("Target: GD 2.2091 | 150k-250k objects | All 9 Game Modes")
    print("="*60)
    gen = MasterpieceLevelGenerator(song_id=624012, level_name="MASTERPIECE", author="Kilo")
    gen.save("masterpiece.gdlvl")
    print("\n" + "="*60)
    print("COMPLETE! Import masterpiece.gdlvl in GD 2.2091")
    print("="*60)


if __name__ == "__main__":
    main()