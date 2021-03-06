'''ステージの定義をするモジュール'''

### ブロック ###
### ふつう色で定義するが、重力ブロックは Block.draw() で特別扱い。
# 通常ブロック
NORMAL = 'gray60'
# 動かせる通常ブロック
M_NORMAL = 'gray80'
# ジャンプブロック
JUMP = 'gold'
# 動かせるジャンプブロック
M_JUMP = 'gold2'
# ジャンプ・ダッシュ禁止ブロック
DARK = 'purple4'
# 動かせるジャンプ・ダッシュ禁止ブロック
M_DARK = 'MediumPurple4'
# 重力ブロック
GRAVUD = 'udarrow'


### ブロック群 ###
### わかりやすいように変数名の末尾に使用する空間数（リストの長さ）を記述する。
# 全部通常ブロック
ALL_NORMAL_30 = [NORMAL]*30
# 両端通常ブロック
EDGE_30 = [NORMAL] + [None]*28 + [NORMAL]
# 空白、上下重力ブロック、空白
GRAVUD_3 = [None, GRAVUD, None]
# 空白、上下重力ブロックx2、空白
GRAVUD2_4 = [None, GRAVUD, GRAVUD, None]
# 通常、空白x2、通常
N__N_4 = [NORMAL, None, None, NORMAL]
# 通常、空白x2、ダーク
N__D_4 = [NORMAL, None, None, DARK]
# ダーク、空白x2、通常
D__N_4 = [DARK, None, None, NORMAL]



### ステージ ###
class Stage10:
    # 名前
    name = 'STAGE 10'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = None

    # ゴールの座標
    goal_pos = (15, 14)

    # キャラの初期位置
    obake_pos = (15, 12)

    # 動かせるブロックの位置
    movable_block_pos = [(6, 8, M_NORMAL), (18, 8, M_NORMAL), (18, 16, M_NORMAL)]

    # ブロック配置
    blocks = {
        27: [None] + [NORMAL]*6 + N__N_4 + [NORMAL]*8 + N__N_4 + [NORMAL]*6,
        26: [None] + [NORMAL] + [None]*5 + N__N_4 + [None]*8 + N__N_4 + [None]*5 + [NORMAL],
        25: [None] + [NORMAL] + [None]*26 + [NORMAL],
        24: [None] + N__N_4 + [None]*8 + N__D_4 + [None]*8 + N__N_4,
        23: [None] + N__N_4 + [NORMAL]*3 + [JUMP]*2 + [NORMAL]*3 + N__D_4 + [NORMAL]*3 + [JUMP]*2 + [GRAVUD]*3 + N__N_4,
        22: [None] + N__N_4 + [None]*8 + N__D_4 + [None]*8 + N__N_4,
        21: [None] + [NORMAL] + [None]*26 + [NORMAL],
        20: [None] + [NORMAL] + [None]*5 + N__N_4 + [None]*8 + N__D_4 + [None]*5 + [NORMAL],
        19: [None] + [NORMAL]*6 + N__N_4 + [DARK]*3 + [NORMAL]*2 + [GRAVUD]*3 + N__D_4 + [NORMAL]*6,
        18: [None] + [NORMAL] + [None]*5 + N__N_4 + [None]*8 + N__D_4 + [None]*5 + [NORMAL],
        17: [None] + [NORMAL] + [None]*26 + [NORMAL],
        16: [None] + N__N_4 + [None]*8 + N__N_4 + [None]*8 + N__N_4,
        15: [None] + N__N_4 + [NORMAL]*5 + [DARK]*3 + N__N_4 + [DARK]*3 + [NORMAL]*5 + N__N_4,
        14: [None] + N__N_4 + [None]*8 + N__N_4 + [None]*8 + N__N_4,
        13: [None] + [NORMAL] + [None]*26 + [NORMAL],
        12: [None] + [NORMAL] + [None]*5 + N__N_4 + [None]*8 + D__N_4 + [None]*5 + [NORMAL],
        11: [None] + [NORMAL]*6 + N__N_4 + [DARK]*5 + [NORMAL]*3 + D__N_4 + [NORMAL]*6,
        10: [None] + [NORMAL] + [None]*5 + N__N_4 + [None]*8 + D__N_4 + [None]*5 + [NORMAL],
        9: [None] + [NORMAL] + [None]*26 + [NORMAL],
        8: [None] + N__N_4 + [None]*8 + N__D_4 + [None]*8 + N__N_4,
        7: [None] + N__N_4 + [NORMAL]*5 + [GRAVUD]*3 + N__D_4 + [NORMAL]*5 + [GRAVUD]*3 + N__N_4,
        6: [None] + N__N_4 + [None]*8 + N__D_4 + [None]*8 + N__N_4,
        5: [None] + [NORMAL] + [None]*26 + [NORMAL],
        4: [None] + [NORMAL] + [None]*5 + N__N_4 + [None]*8 + N__D_4 + [None]*5 + [NORMAL],
        3: [None] + [NORMAL] + [JUMP]*2 + [NORMAL]*3 + N__N_4 + [NORMAL]*3 + [JUMP]*2 + [NORMAL]*3 + N__D_4 + [NORMAL]*6,
    }


class Stage9:
    # 名前
    name = 'STAGE 9'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage10

    # ゴールの座標
    goal_pos = (27, 14)

    # キャラの初期位置
    obake_pos = (3, 13)

    # 動かせるブロックの位置
    #movable_block_pos = []

    # ブロック配置
    blocks = {
        28: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        27: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        26: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        25: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [DARK]*4 + [None]*4 + [NORMAL]*4,
        20: [None] + [GRAVUD]*4 + [None]*4 + [DARK]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [GRAVUD]*4,
        19: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        18: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        17: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [DARK]*4 + [None]*4 + [NORMAL]*4,
        12: [None] + [DARK]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [DARK]*4 + [None]*4 + [NORMAL]*4,
        11: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [DARK]*4 + [DARK]*4 + [NORMAL]*4,
        10: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [NORMAL]*4 + [NORMAL]*4,
        9: [None] + [GRAVUD]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        8: [None]*26 + [NORMAL]*2,
        7: [None]*26 + [NORMAL]*2,
        6: [None]*26 + [NORMAL]*2,
        5: [None]*26 + [NORMAL]*2,
        4: [None] + [NORMAL]*4 + [None]*4 + [DARK]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        3: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        2: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
        1: [None] + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4 + [None]*4 + [NORMAL]*4,
    }


class Stage8:
    # 名前
    name = 'STAGE 8'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage9

    # ゴールの座標
    goal_pos = (26, 11)

    # キャラの初期位置
    obake_pos = (2, 6)

    # 動かせるブロックの位置
    movable_block_pos = [(4, 21, NORMAL), (8, 6, NORMAL), (8, 8, GRAVUD)]

    # ブロック配置
    blocks = {
        23: ALL_NORMAL_30,
        22: [NORMAL] + [None]*6 + [NORMAL]*23,
        21: [NORMAL] + [None]*6 + [NORMAL]*23,
        20: [NORMAL] + [None]*2 + [GRAVUD]*2 + [None]*2 + [NORMAL]*23,
        19: N__N_4*2 + [NORMAL]*22,
        18: N__N_4*2 + [NORMAL]*22,
        17: N__N_4*2 + [NORMAL]*11 + [DARK]*10 + [NORMAL],
        16: [NORMAL] + [None]*16 + [NORMAL]*2 + [None]*10 + [NORMAL],
        15: [NORMAL] + [None]*16 + [NORMAL]*2 + [None]*10 + [NORMAL],
        14: [NORMAL] + [None]*4 + [DARK]*10 + [None]*2 + [NORMAL]*2 + [None]*10 + [NORMAL],
        13: [NORMAL] + [None]*16 + [NORMAL]*2 + [None]*10 + [NORMAL],
        12: [NORMAL] + [None]*16 + [NORMAL]*2 + [None]*10 + [NORMAL],
        11: EDGE_30,
        10: EDGE_30,
        9: [NORMAL] + [None]*16 + [NORMAL]*2 + [None]*10 + [NORMAL],
        8: [NORMAL] + [None]*16 + [NORMAL]*2 + [None]*10 + [NORMAL],
        7: [NORMAL] + [None]*16 + [NORMAL]*2 + [None]*10 + [NORMAL],
        6: [NORMAL] + [None]*16 + [NORMAL]*2 + [None]*10 + [NORMAL],
        5: ALL_NORMAL_30,
    }


class Stage7:
    # 名前
    name = 'STAGE 7'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage8

    # ゴールの座標
    goal_pos = (15, 4)

    # キャラの初期位置
    obake_pos = (10, 22)

    # 動かせるブロックの位置
    movable_block_pos = [(15, 19, NORMAL), (15, 22, GRAVUD)]

    # ブロック配置
    blocks = {
        26: [NORMAL] + [GRAVUD]*28 + [NORMAL],
        25: EDGE_30,
        24: EDGE_30,
        23: EDGE_30,
        22: EDGE_30,
        21: [NORMAL] + [None]*4 + [NORMAL]*20 + [None]*4 + [NORMAL],
        20: EDGE_30,
        19: EDGE_30,
        18: [NORMAL] + [None]*4 + [NORMAL]*20 + [None]*4 + [NORMAL],
        17: [NORMAL] + [None]*4 + [GRAVUD]*20 + [None]*4 + [NORMAL],
        16: EDGE_30,
        15: EDGE_30,
        14: [NORMAL] + [None]*6 + [NORMAL]*6 + [None]*4 + [NORMAL]*6 + [None]*6 + [NORMAL],
        13: [NORMAL] + [None]*6 + [NORMAL]*6 + [None]*4 + [NORMAL]*6 + [None]*6 + [NORMAL],
        12: [NORMAL] + [NORMAL]*6 + [NORMAL]*6 + [None]*4 + [NORMAL]*6 + [NORMAL]*6 + [NORMAL],
        11: [NORMAL] + [GRAVUD]*12 + [None]*4 + [GRAVUD]*12 + [NORMAL],
        10: EDGE_30,
        9: EDGE_30,
        8: [NORMAL] + [None]*4 + [NORMAL]*2 + [None]*16 + [NORMAL]*2 + [None]*4 + [NORMAL],
        7: [NORMAL] + [None]*4 + [NORMAL]*2 + [None]*16 + [NORMAL]*2 + [None]*4 + [NORMAL],
        6: [NORMAL] + [None]*4 + [NORMAL]*20 + [None]*4 + [NORMAL],
        5: EDGE_30,
        4: EDGE_30,
        3: ALL_NORMAL_30,
    }


class Stage6:
    # 名前
    name = 'STAGE 6'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage7

    # ゴールの座標
    goal_pos = (10, 7)

    # キャラの初期位置
    obake_pos = (10, 5)

    # 動かせるブロックの位置
    movable_block_pos = [(15, 17, GRAVUD)]

    # ブロック配置
    blocks = {
        25: [NORMAL]*26 + [DARK]*3 + [NORMAL],
        24: EDGE_30,
        23: EDGE_30,
        22: [NORMAL] + [None]*3 + [NORMAL]*22 + [None]*3 + [NORMAL],
        21: EDGE_30,
        20: EDGE_30,
        19: [NORMAL] + [DARK]*3 + [NORMAL]*14 + [None]*4 + [NORMAL]*4 + [None]*3 + [NORMAL],
        18: [NORMAL] + [None]*24 + [NORMAL] + [None]*3 + [NORMAL],
        17: [NORMAL] + [None]*24 + [NORMAL] + [None]*3 + [NORMAL],
        16: [NORMAL] + [None]*3 + [NORMAL]*4 + N__N_4 + [NORMAL]*6 + [DARK]*4 + [NORMAL]*4 + [None]*3 + [NORMAL],
        15: [NORMAL] + [None]*16 + [NORMAL] + [None]*11 + [NORMAL],
        14: [NORMAL] + [None]*16 + [NORMAL] + [None]*11 + [NORMAL],
        13: [NORMAL]*13 + [None]*4 + [NORMAL] + [None]*4 + [DARK]*4 + [NORMAL]*4,
        12: EDGE_30,
        11: EDGE_30,
        10: [NORMAL] + [None]*3 + [NORMAL]*5 + [None]*2 + [NORMAL]*7 + GRAVUD2_4 + [NORMAL]*4 + [None]*3 + [NORMAL],
        9: [NORMAL] + [None]*7 + N__N_4 + [None]*17 + [NORMAL],
        8: [NORMAL] + [None]*7 + N__N_4 + [None]*17 + [NORMAL],
        7: [NORMAL] + GRAVUD_3 + [NORMAL]*4 + N__N_4 + [NORMAL]*14 + [None]*3 + [NORMAL],
        6: EDGE_30,
        5: EDGE_30,
        4: [NORMAL] + [DARK]*3 + [NORMAL]*5 + [DARK]*2 + [NORMAL]*19,
    }


class Stage5:
    # 名前
    name = 'STAGE 5'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage6

    # ゴールの座標
    goal_pos = (20, 7)

    # キャラの初期位置
    obake_pos = (20, 10)

    # 説明の看板
    signs = [(10, 10, 'dsc_gravity')]

    # 動かせるブロックの位置
    movable_block_pos = [(3, 4, M_NORMAL), (16, 20, M_NORMAL)]

    # ブロック配置
    blocks = {
        26: [NORMAL]*13 + [JUMP]*4 + [NORMAL]*13,
        25: EDGE_30,
        24: EDGE_30,
        23: EDGE_30,
        22: EDGE_30,
        21: EDGE_30,
        20: EDGE_30,
        19: [NORMAL]*4 + [None]*3 + [NORMAL]*6 + GRAVUD2_4 + [NORMAL]*6 + [None]*3 + [NORMAL]*4,
        18: EDGE_30,
        17: EDGE_30,
        16: EDGE_30,
        15: EDGE_30,
        14: [NORMAL]*4 + GRAVUD_3 + [NORMAL]*6 + [None]*4 + [NORMAL]*6 + [JUMP]*3 + [NORMAL]*4,
        13: EDGE_30,
        12: EDGE_30,
        11: EDGE_30,
        10: EDGE_30,
        9: [NORMAL]*4 + [None]*3 + [NORMAL]*6 + GRAVUD2_4 + [NORMAL]*6 + [None]*3 + [NORMAL]*4,
        8: EDGE_30,
        7: EDGE_30,
        6: EDGE_30,
        5: EDGE_30,
        4: EDGE_30,
        3: [NORMAL]*4 + [JUMP]*3 + [NORMAL]*16 + [None]*3 + [NORMAL]*4,
    }


class Stage4:
    # 名前
    name = 'STAGE 4'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage5

    # ゴールの座標
    goal_pos = (20, 16)

    # キャラの初期位置
    obake_pos = (10, 12)

    # 説明の看板
    signs = [(20, 12, 'dsc_dark')]

    # 動かせるブロックの位置
    movable_block_pos = [
        (6, 12, M_NORMAL),
        (13, 12, M_DARK),
        (24, 12, M_JUMP),
        (13, 16, M_DARK),
        (10, 20, M_DARK),
        (20, 20, M_DARK),
    ]

    # ブロック配置
    blocks = {
        25: ALL_NORMAL_30,
        24: EDGE_30,
        23: EDGE_30,
        22: EDGE_30,
        21: EDGE_30,
        20: EDGE_30,
        19: [NORMAL] + [None]*4 + [NORMAL]*9 + [None]*2 + [NORMAL]*9 + [None]*4 + [NORMAL],
        18: [NORMAL] + [None]*7 + [NORMAL]*6 + [None]*5 + [NORMAL]*6 + [None]*4 + [NORMAL],
        17: [NORMAL] + [None]*23 + [DARK] + [None]*4 + [NORMAL],
        16: [NORMAL] + [None]*23 + [DARK] + [None]*4 + [NORMAL],
        15: [NORMAL] + [None]*4 + [DARK]*9 + [None]*2 + [NORMAL]*9 + [None]*4 + [NORMAL],
        14: EDGE_30,
        13: EDGE_30,
        12: EDGE_30,
        11: [NORMAL]*5 + [DARK]*9 + [None]*2 + [NORMAL]*14,
        10: [NORMAL]*14 + [None]*2 + [NORMAL]*14,
        9: [NORMAL]*14 + [None]*2 + [NORMAL]*14,
        8: [NORMAL]*14 + [None]*2 + [NORMAL]*14,
        7: ALL_NORMAL_30,
        6: ALL_NORMAL_30,
    }


class Stage3:
    # 名前
    name = 'STAGE 3'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage4

    # ゴールの座標
    goal_pos = (21, 19)

    # キャラの初期位置
    obake_pos = (21, 14)

    # 説明の看板
    signs = [(15, 18, 'dsc_push')]

    # 動かせるブロックの位置
    movable_block_pos = [(5, 10, M_JUMP), (6, 12, M_NORMAL), (8, 10, M_NORMAL), (24, 14, M_NORMAL)]

    # ブロック配置
    blocks = {
        22: ALL_NORMAL_30,
        21: [NORMAL]*7 + [None]*22 + [NORMAL],
        20: [NORMAL]*7 + [None]*22 + [NORMAL],
        19: EDGE_30,
        18: EDGE_30,
        17: [NORMAL] + [None]*10 + [NORMAL]*19,
        16: [NORMAL] + [None]*17 + [NORMAL]*12,
        15: EDGE_30,
        14: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*13 + [NORMAL],
        13: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*4 + [NORMAL]*5 + [None]*4 + [NORMAL],
        12: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*4 + [NORMAL]*5 + [None]*4 + [NORMAL],
        11: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*13 + [NORMAL],
        10: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*13 + [NORMAL],
        9: ALL_NORMAL_30,
    }


class Stage2:
    # 名前
    name = 'STAGE 2'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage3

    # ゴールの座標
    goal_pos = (14, 24)

    # キャラの初期位置
    obake_pos = (3, 1)

    # 説明の看板
    signs = [(5, 1, 'dsc_dash')]

    # ブロック配置
    blocks = {
        17: [None]*8 + [NORMAL, JUMP],
        16: [None]*20 + [NORMAL]*2,
        15: [None]*5 + [NORMAL],
        14: [None]*5 + [NORMAL],
        13: [None]*3 + [NORMAL]*3,
        9: [None, JUMP] + [NORMAL]*3,
        6: [None]*6 + [NORMAL]*2 + [JUMP, NORMAL] + [None]*10 + [JUMP] + [NORMAL],
        0: [NORMAL]*10 + [None]*10 + [NORMAL]*7 + [JUMP] + [NORMAL]*2,
    }


class Stage1:
    # 名前
    name = 'STAGE 1'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage2

    # ゴールの座標
    goal_pos = (9, 15)

    # キャラの初期位置
    obake_pos = (3, 1)

    # 説明の看板
    signs = [(22, 1, 'dsc_J'), (25, 1, 'dsc_K'), (28, 1, 'dsc_L')]

    # ブロック配置
    blocks = {
        13: [None]*8 + [NORMAL]*4,
        12: [None]*11 + [NORMAL] + [None]*5 + [NORMAL]*2,
        11: [None]*11 + [NORMAL],
        10: [None]*11 + [NORMAL],
        9: [None]*11 + [NORMAL]*3,
        7: [None]*16 + [NORMAL]*2,
        5: [None]*22 + [NORMAL]*4,
        3: [None]*16 + [NORMAL]*4,
        2: [None]*11 + [NORMAL],
        1: [None]*11 + [NORMAL],
        0: ALL_NORMAL_30,
    }

