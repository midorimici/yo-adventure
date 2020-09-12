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
GLAVUD = 'udarrow'


class Stage5:
    # 名前
    name = 'STAGE 5'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = None

    # ゴールの座標
    goal_pos = (20, 7)

    # キャラの初期位置
    obake_pos = (20, 10)

    # 動かせるブロックの位置
    movable_block_pos = [(16, 20, M_NORMAL)]

    # ブロック配置
    blocks = {
        28: [NORMAL]*13 + [JUMP]*4 + [NORMAL]*13,
        27: [NORMAL] + [None]*28 + [NORMAL],
        26: [NORMAL] + [None]*28 + [NORMAL],
        25: [NORMAL] + [None]*28 + [NORMAL],
        24: [NORMAL] + [None]*28 + [NORMAL],
        23: [NORMAL] + [None]*28 + [NORMAL],
        22: [NORMAL] + [None]*28 + [NORMAL],
        21: [NORMAL] + [None]*28 + [NORMAL],
        20: [NORMAL] + [None]*28 + [NORMAL],
        19: [NORMAL]*4 + [None]*3 + [NORMAL]*6 + [None, GLAVUD, GLAVUD, None] + [NORMAL]*6 + [None]*3 + [NORMAL]*4,
        18: [NORMAL] + [None]*28 + [NORMAL],
        17: [NORMAL] + [None]*28 + [NORMAL],
        16: [NORMAL] + [None]*28 + [NORMAL],
        15: [NORMAL] + [None]*28 + [NORMAL],
        14: [NORMAL]*4 + [None, GLAVUD, None] + [NORMAL]*6 + [None]*4 + [NORMAL]*6 + [JUMP]*3 + [NORMAL]*4,
        13: [NORMAL] + [None]*28 + [NORMAL],
        12: [NORMAL] + [None]*28 + [NORMAL],
        11: [NORMAL] + [None]*28 + [NORMAL],
        10: [NORMAL] + [None]*28 + [NORMAL],
        9: [NORMAL]*4 + [None]*3 + [NORMAL]*6 + [None, GLAVUD, GLAVUD, None] + [NORMAL]*6 + [None]*3 + [NORMAL]*4,
        8: [NORMAL] + [None]*28 + [NORMAL],
        7: [NORMAL] + [None]*28 + [NORMAL],
        6: [NORMAL] + [None]*28 + [NORMAL],
        5: [NORMAL] + [None]*28 + [NORMAL],
        4: [NORMAL] + [None]*28 + [NORMAL],
        3: [NORMAL] + [None]*28 + [NORMAL],
        2: [NORMAL] + [None]*28 + [NORMAL],
        1: [NORMAL]*4 + [JUMP]*3 + [NORMAL]*23,
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

    # 動かせるブロックの位置
    movable_block_pos = [
        (6, 12, M_NORMAL),
        (13, 12, M_NORMAL),
        (13, 16, M_DARK),
        (10, 20, M_NORMAL),
        (20, 20, M_NORMAL)
    ]

    # ブロック配置
    blocks = {
        25: [NORMAL]*30,
        24: [NORMAL]*30,
        23: [NORMAL] + [None]*28 + [NORMAL],
        22: [NORMAL] + [None]*28 + [NORMAL],
        21: [NORMAL] + [None]*28 + [NORMAL],
        20: [NORMAL] + [None]*28 + [NORMAL],
        19: [NORMAL] + [None]*4 + [NORMAL]*9 + [None]*2 + [NORMAL]*9 + [None]*4 + [NORMAL],
        18: [NORMAL] + [None]*7 + [NORMAL]*6 + [None]*5 + [NORMAL]*6 + [None]*4 + [NORMAL],
        17: [NORMAL] + [None]*28 + [NORMAL],
        16: [NORMAL] + [None]*28 + [NORMAL],
        15: [NORMAL] + [None]*4 + [DARK]*9 + [None]*2 + [NORMAL]*9 + [None]*4 + [NORMAL],
        14: [NORMAL] + [None]*28 + [NORMAL],
        13: [NORMAL] + [None]*28 + [NORMAL],
        12: [NORMAL] + [None]*28 + [NORMAL],
        11: [NORMAL]*5 + [DARK]*9 + [None]*2 + [NORMAL]*9 + [JUMP]*4 + [NORMAL],
        10: [NORMAL]*14 + [None]*2 + [NORMAL]*14,
        9: [NORMAL]*14 + [None]*2 + [NORMAL]*14,
        8: [NORMAL]*14 + [None]*2 + [NORMAL]*14,
        7: [NORMAL]*30,
        6: [NORMAL]*30,
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

    # 動かせるブロックの位置
    movable_block_pos = [(5, 10, M_JUMP), (6, 12, M_NORMAL), (8, 10, M_NORMAL), (24, 14, M_NORMAL)]

    # ブロック配置
    blocks = {
        22: [NORMAL]*30,
        21: [NORMAL]*7 + [None]*22 + [NORMAL],
        20: [NORMAL]*7 + [None]*22 + [NORMAL],
        19: [NORMAL] + [None]*28 + [NORMAL],
        18: [NORMAL] + [None]*28 + [NORMAL],
        17: [NORMAL] + [None]*10 + [NORMAL]*19,
        16: [NORMAL] + [None]*18 + [NORMAL]*7 + [None]*3 + [NORMAL],
        15: [NORMAL] + [None]*28 + [NORMAL],
        14: [NORMAL] + [None]*28 + [NORMAL],
        13: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*4 + [NORMAL]*5 + [None]*4 + [NORMAL],
        12: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*4 + [NORMAL]*5 + [None]*4 + [NORMAL],
        11: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*13 + [NORMAL],
        10: [NORMAL] + [None]*13 + [NORMAL]*2 + [None]*13 + [NORMAL],
        9: [NORMAL]*30,
    }


class Stage2:
    # 名前
    name = 'STAGE 2'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = Stage3

    # ゴールの座標
    goal_pos = (15, 25)

    # キャラの初期位置
    obake_pos = (3, 1)

    # ブロック配置
    blocks = {
        17: [None]*8 + [NORMAL, JUMP],
        16: [None]*20 + [NORMAL]*2,
        15: [None]*5 + [NORMAL],
        14: [None]*5 + [NORMAL],
        13: [None]*3 + [NORMAL]*3,
        10: [NORMAL],
        9: [None]*2 + [NORMAL]*3,
        8: [None]*6 + [NORMAL]*2 + [JUMP, NORMAL] + [None]*13 + [JUMP] + [NORMAL],
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
        0: [NORMAL]*30,
    }