# 通常ブロック
NORMAL = 'gray60'
# 動かせる通常ブロック
M_NORMAL = 'gray80'
# ジャンプブロック
JUMP = 'gold'
# 動かせるジャンプブロック
M_JUMP = 'gold2'


class Stage3:
    # 名前
    name = 'STAGE 3'

    # クリア済み
    clear = False

    # 次のステージ
    next_stage = None

    # ゴールの座標
    goal_pos = (21, 19)

    # キャラの初期位置
    obake_pos = (21, 14)

    # 動かせるブロックの位置
    movable_block_pos = [(5, 10, M_JUMP), (5, 12, M_NORMAL), (8, 10, M_NORMAL), (24, 14, M_NORMAL)]

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
        16: [None]*8 + [NORMAL, JUMP] + [None]*10 + [NORMAL]*2,
        15: [None]*5 + [NORMAL],
        14: [None]*5 + [NORMAL],
        13: [None]*4 + [NORMAL]*2,
        10: [None]*2 + [NORMAL],
        9: [None]*4 + [NORMAL],
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