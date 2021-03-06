import sys
import math
from ctypes import windll
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

import stages


# 画面サイズ
DISP_W = windll.user32.GetSystemMetrics(0)
DISP_H = windll.user32.GetSystemMetrics(1)

if DISP_W < 900 or DISP_H < 900:
	# ウィンドウサイズ
	WINDOW_WIDTH = 600
	WINDOW_HEIGHT = 600

	# タイマーテキストサイズ
	TIMER_TEXT_SIZE = 20
	# STAGE CLEAR テキストサイズ
	CLEAR_TEXT_SIZE = 60

	# ブロックサイズ
	BLOCK_SIZE = 20

	# キャラサイズ
	IMG_SIZE = 36
	IMG_WIDTH = 30
	IMG_HEIGHT = 30

	# 横移動初速さ
	MOVE_SPEED = 4
	# 横移動加速度
	MOVE_A = 1
	# ジャンプ初速度
	JUMP_V0 = 12
	# 重力加速度
	ga = 2.4
else:
	# ウィンドウサイズ
	WINDOW_WIDTH = int(600*1.5)
	WINDOW_HEIGHT = int(600*1.5)

	# タイマーテキストサイズ
	TIMER_TEXT_SIZE = int(20*1.5)
	# STAGE CLEAR テキストサイズ
	CLEAR_TEXT_SIZE = int(60*1.5)

	# ブロックサイズ
	BLOCK_SIZE = int(20*1.5)

	# キャラサイズ
	IMG_SIZE = int(36*1.5)
	IMG_WIDTH = int(30*1.5)
	IMG_HEIGHT = int(30*1.5)

	# 横移動初速さ
	MOVE_SPEED = 4*1.5
	# 横移動加速度
	MOVE_A = 1*1.5
	# ジャンプ初速度
	JUMP_V0 = 12*1.5
	# 重力加速度
	ga = 2.4*1.5

# ジャンプブロック初速係数
JUMP_M = 5

# 重力の方向
# u: ↑, d: ↓, l: ←, r: →
grav_dir = 'd'

# タイマー
time = 0
timer = None


# キャラクター
class Obake:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = IMG_WIDTH
		self.height = IMG_HEIGHT
		# キャラの向き
		# l: ←, r: →
		self.seeing_direction = 'l'
		# 加減速フラグ
		# acc: 加速, dec: 減速
		self.acc_state = 'acc'
		# アニメーションの時刻
		self.time_x = 0
		self.time_y = 0
		# ジャンプ中or落下中
		self.flying = False
		# ダークブロックの影響下
		self.isdark = False

		# 大ジャンプ判定
		self._do_long_jump = False
		# キー操作
		self._short_press_l = False
		self._short_press_j = False
		self._short_press_k = False

		self.draw()
		self.bind()
	
	def delete(self):
		cv.delete(self.id)

	def draw(self):
		'''
		幅 IMG_WIDTH 高さ IMG_HEIGHT の正方形
		┌ ─ ┐
		│ o │
		└ ─ ┘
		'''
		self.id = cv.create_image(self.x, self.y, image=obake_tkimg)

	def bind(self):
		# [L], [J] 押している間その方向に直線移動
		cv.bind("<KeyPress-l>", self.on_keypress_l)
		cv.bind("<KeyPress-j>", self.on_keypress_j)
		# キーを離したらストップ
		cv.bind("<KeyRelease-l>", self.on_keyrelease_l)
		cv.bind("<KeyRelease-j>", self.on_keyrelease_j)
		# [K] ちょっとだけ押すと小ジャンプ、長め押しで大ジャンプ
		cv.bind("<KeyPress-k>", self.on_keypress_k)
		cv.bind("<KeyRelease-k>", self.on_keyrelease_k)
	
	def on_keypress_l(self, event):
		if not self._short_press_l:
			self._short_press_l = True
			self._short_press_j = False
			self.move_right()
	
	def on_keypress_j(self, event):
		if not self._short_press_j:
			self._short_press_l = False
			self._short_press_j = True
			self.move_left()
	
	def on_keyrelease_l(self, event):
		if self._short_press_l:
			self._short_press_l = False
	
	def on_keyrelease_j(self, event):
		if self._short_press_j:
			self._short_press_j = False
	
	def on_keypress_k(self, event):
		if not self._short_press_k:
			self._short_press_k = True
			self._do_long_jump = root.after(100, self.on_longpress_k)
	
	def on_keyrelease_k(self, event):
		if self._short_press_k:
			self.jump(JUMP_V0)
			self._short_press_k = False
			root.after_cancel(self._do_long_jump)
	
	def on_longpress_k(self):
		self._short_press_k = False
		root.after_cancel(self._do_long_jump)
		self.jump(JUMP_V0*1.4)

	def move_right(self):
		# 画像左右反転
		self.delete()
		if grav_dir == 'd':
			self.id = cv.create_image(self.x, self.y, image=obake_mirror_tkimg)
		elif grav_dir == 'u':
			self.id = cv.create_image(self.x, self.y, image=obake_fm_tkimg)
		self.seeing_direction = 'r'
		self.time_x = 0
		self.r_move(MOVE_SPEED)
	
	def move_left(self):
		# 画像左右反転
		self.delete()
		if grav_dir == 'd':
			self.id = cv.create_image(self.x, self.y, image=obake_tkimg)
		elif grav_dir == 'u':
			self.id = cv.create_image(self.x, self.y, image=obake_flip_tkimg)
		self.seeing_direction = 'l'
		self.time_x = 0
		self.l_move(MOVE_SPEED)
	
	def r_move(self, prev_dx):
		xtmp = self.x
		if self._short_press_l:
			# キー押下時
			if self.flying:
				# 空中にいるときは速度は不変
				dx = prev_dx
			else:
				# 加速
				if on_block('dark'):
					dx = prev_dx
				else:
					dx = prev_dx + min(MOVE_A, 4*MOVE_SPEED)
		else:
			# キーを離しているとき減速
			dx = prev_dx - MOVE_A
			if dx < 0: return

		self.x += dx
		if not self.flying:
			self.fall_move()
			if self.time_x == -1: return
		if hitting_block_x(self):
			self.x = xtmp
			self.time_x = 0
			self._short_press_l = False
			self._short_press_j = False
			cv.coords(self.id, self.x, self.y)
			return
		self.time_x += 1
		self._lr_move = root.after(50, self.r_move, dx)
		cv.coords(self.id, self.x, self.y)
		judge_goal()
	
	def l_move(self, prev_dx):
		xtmp = self.x
		if self._short_press_j:
			# キー押下時
			if self.flying:
				# 空中にいるときは速度は不変
				dx = prev_dx
			else:
				# 加速
				if on_block('dark'):
					dx = prev_dx
				else:
					dx = prev_dx + min(MOVE_A, 4*MOVE_SPEED)
		else:
			# キーを離しているとき減速
			dx = prev_dx - MOVE_A
			if dx < 0: return

		self.x -= dx
		if not self.flying:
			self.fall_move()
			if self.time_x == -1: return
		if hitting_block_x(self):
			self.x = xtmp
			self.time_x = 0
			self._short_press_l = False
			self._short_press_j = False
			cv.coords(self.id, self.x, self.y)
			return
		self.time_x += 1
		self._lr_move = root.after(50, self.l_move, dx)
		cv.coords(self.id, self.x, self.y)
		judge_goal()
	
	def stop(self):
		root.after_cancel(self._lr_move)
		self.time_x = 0

	def fall_move(self):
		dy = min(ga*self.time_y, 20)
		if grav_dir == 'd':
			self.y += dy
			if self.y > WINDOW_HEIGHT:
				# 画面外に出た
				restart_game()
			elif hitting_block_floor(self):
				# 床に乗った
				self.y = math.floor(self.y/BLOCK_SIZE)*BLOCK_SIZE + (BLOCK_SIZE - IMG_HEIGHT/2)
				self.time_y = 0
				self.flying = False
				if on_block('dark'):
					self.isdark = True
				else:
					self.isdark = False
			else:
				self.flying = True
				self.time_y += 1
				root.after(50, self.fall_move)
		elif grav_dir == 'u':
			self.y -= dy
			if self.y < 0:
				# 画面外に出た
				restart_game()
			elif hitting_block_ceil():
				# 床に乗った
				self.y = math.ceil(self.y/BLOCK_SIZE)*BLOCK_SIZE - (BLOCK_SIZE - IMG_HEIGHT/2)
				self.time_y = 0
				self.flying = False
				if on_block('dark'):
					self.isdark = True
				else:
					self.isdark = False
			else:
				self.flying = True
				self.time_y += 1
				root.after(50, self.fall_move)
		cv.coords(self.id, self.x, self.y)
		judge_goal()
	
	def jump(self, vel):
		if self.flying or on_block('dark'): return
		jump_snd.play()
		self.flying = True
		self.jump_move(vel)
	
	def jump_move(self, vel):
		v0 = JUMP_M*vel if on_block('jump') else vel
		dy = max(v0 - ga*self.time_y, -20)
		if grav_dir == 'd':
			self.y -= dy
			if self.y > WINDOW_HEIGHT:
				# 画面外に出た
				restart_game()
			elif hitting_block_ceil():
				# 天井に当たった
				self.fall_move()
				return
			elif hitting_block_floor(self):
				# 床に乗った
				self.y = math.floor(self.y/BLOCK_SIZE)*BLOCK_SIZE + (BLOCK_SIZE - IMG_HEIGHT/2)
				self.time_y = 0
				self.flying = False
			else:
				self.time_y += 1
				root.after(50, self.jump_move, vel)
		elif grav_dir == 'u':
			self.y += dy
			if self.y < 0:
				# 画面外に出た
				restart_game()
			elif hitting_block_floor(self):
				# 天井に当たった
				self.fall_move()
				return
			elif hitting_block_ceil():
				# 床に乗った
				self.y = math.ceil(self.y/BLOCK_SIZE)*BLOCK_SIZE - (BLOCK_SIZE - IMG_HEIGHT/2)
				self.time_y = 0
				self.flying = False
			else:
				self.time_y += 1
				root.after(50, self.jump_move, vel)
		cv.coords(self.id, self.x, self.y)
		judge_goal()


# ブロック
class Block:
	def __init__(self, x, y, param, movable=False):
		self.x = x
		self.y = y
		self.width = 2*BLOCK_SIZE if movable else BLOCK_SIZE
		self.height = 2*BLOCK_SIZE if movable else BLOCK_SIZE
		self.param = param
		# 動かせるか
		self.movable = movable
		# アニメーション
		self.time_y = 0
		self.draw()
	
	def draw(self):
		'''
		if self.movable:
			一辺の長さ 2*BLOCK_SIZE の正方形
		else:
			一辺の長さ BLOCK_SIZE の正方形

		┌ o ┐
		│   │
		└ ─ ┘
		'''
		if self.movable:
			if 'arrow' in self.param:
				if self.param == 'udarrow': _img = udarrow2_tkimg
				self.id = cv.create_image(self.x, self.y + BLOCK_SIZE, image=_img)
			else:
				self.id = cv.create_rectangle(self.x - BLOCK_SIZE, self.y,
					self.x + BLOCK_SIZE, self.y + 2*BLOCK_SIZE,
					fill=self.param)
		else:
			if 'arrow' in self.param:
				if self.param == 'udarrow': _img = udarrow_tkimg
				cv.create_image(self.x, self.y + BLOCK_SIZE/2, image=_img)
			else:
				cv.create_rectangle(self.x - BLOCK_SIZE/2, self.y,
					self.x + BLOCK_SIZE/2, self.y + BLOCK_SIZE,
					fill=self.param)
	
	def __repr__(self):
		return ('M ' if self.movable else '') + self.param
	
	# 以下は movable = True のときのみ使用
	def slide_move(self):
		'''ブロックが押されたときの動き'''
		xtmp = self.x
		if self.x > obake.x:
			# ブロックがキャラの右側にあるとき
			self.x += 4
		else:
			# ブロックがキャラの左側にあるとき
			self.x -= 4
		self.fall_move()
		if hitting_block_x(self):
			self.x = xtmp
		if 'arrow' in self.param:
			cv.coords(self.id, self.x, self.y + BLOCK_SIZE)
		else:
			cv.coords(self.id, self.x - BLOCK_SIZE, self.y,
				self.x + BLOCK_SIZE, self.y + 2*BLOCK_SIZE)
	
	def fall_move(self):
		self.y += min(ga*self.time_y, 20)
		if self.y > WINDOW_HEIGHT:
			# 画面外に出た
			cv.delete(self.id)
		elif hitting_block_floor(self):
			# 床に乗った
			self.y = (self.y//BLOCK_SIZE)*BLOCK_SIZE
			self.time_y = 0
		else:
			self.time_y += 1
			root.after(50, self.fall_move)
		if 'arrow' in self.param:
			cv.coords(self.id, self.x, self.y + BLOCK_SIZE)
		else:
			cv.coords(self.id, self.x - BLOCK_SIZE, self.y,
				self.x + BLOCK_SIZE, self.y + 2*BLOCK_SIZE)


# ブロックとの関係を判定する関数
def hitting_block_x(obj):
	'''
	キャラがブロックに横からぶつかっているかどうか

	Parameters
	----------
	obj : obj -> Obake | Block
		obake または動かせるブロックのオブジェクト．
	
	Returns
	-------
	bool

	Notes
	-----
	if 文条件式の図

	abs(block.x - obj.x) < (obj.width + w)/2
	
	width
	┌ x ┐ ↔ ┌ x ┐
	│ x │   │ x │	obj
	└ ─ ┼ x ┼ ─ ┘
	    │   │		block
	    └ ─ ┘
	      w
	
	-(h + BLOCK_SIZE) < block.y - obj.y < obj.height - h
	(obj.y - block.y < h + BLOCK_SIZE) and (block.y - obj.y < obj.height - h)

	     obj  block
	h ↕ ┌ y ┐     ↑
	  ⇣ │ y │   height
	    └ ─ ┼ y ┐ ↓   ↑
	      ↕ │   │ BLOCK_SIZE
	h ↕ ┌ y ┼ ─ ┘     ↓
	  ⇣ │ y │
	    └ ─ ┘
	'''
	for block in blocks:
		if obj == block: continue
		# ブロックが動かせるとき、幅2倍で計算
		if getattr(block, 'movable', False):
			w = 2*BLOCK_SIZE
		else:
			w = BLOCK_SIZE
		# obj が動かせるブロックのとき、高さの当たり判定を0に
		if getattr(obj, 'movable', False):
			h = 0
		else:
			h = IMG_HEIGHT/2
		if (abs(block.x - obj.x) < (obj.width + w)/2
				and -(h + BLOCK_SIZE) < block.y - obj.y < obj.height - h):
			if block.movable:
				# ブロックが動かせるとき
				block.slide_move()
			return True


def hitting_block_floor(obj):
	'''
	キャラや動かせるブロックがブロックに上から接しているかどうか

	Parameters
	----------
	obj : obj -> Obake | Block
		obake または動かせるブロックのオブジェクト．
	
	Returns
	-------
	bool

	Notes
	-----
	if 文条件式の図

	abs(block.x - obj.x) < (obj.width + w)/2 - 2

	width
	┌ x ┐ ↔ ┌ x ┐
	│ x │   │ x │	obj
	└ ─ ┼ x ┼ ─ ┘
	    │   │		block
	    └ ─ ┘
	    ← w →
	
	block.y - h <= obj.y <= block.y

	     obj  block
	  ⇡ ┌ y ┐
	h ↑ │ y │
	  ↓ └ ─ ┼ y ┐
			│   │
			└ ─ ┘
	
	多少超過しても床をすり抜けないように制約を緩めている
	'''
	for block in blocks:
		if obj == block: continue
		# ブロックが動かせるとき、幅2倍で計算
		if getattr(block, 'movable', False):
			w = 2*BLOCK_SIZE
		else:
			w = BLOCK_SIZE
		# obj が動かせるブロックのとき、高さの当たり判定を2倍に
		if getattr(obj, 'movable', False):
			h = obj.height
		else:
			h = obj.height/2
		if (abs(block.x - obj.x) < (obj.width + w)/2 - 2
				and block.y - h <= obj.y <= block.y):
			if (block.param == 'udarrow'
					and not getattr(obj, 'movable', False)
					and grav_dir == 'u'):
				change_gravity('ud')
			return True


def hitting_block_ceil():
	'''
	キャラがブロックに下からぶつかっているかどうか
	
	Returns
	-------
	bool

	Notes
	-----
	if 文条件式の図

	abs(block.x - obj.x) < (IMG_WIDTH + size)/2 - 2

	    size
		┌ x ┐
		│   │		block
	┌ ─ ┼ ─ ┼ ─ ┐
	│ x │   │ x │	obake
	└ ─ ┘ ↔ └ ─ ┘
		  IMG_WIDTH
	
	block.y + size <= obake.y <= block.y + size + IMG_HEIGHT/2

		┌ y ┐		↑
	  ⇡ │   │      size
	┌ ─ ┼ ─ ┘	↑	↓
	│ y │   IMG_HEIGHT
	└ ─ ┘ 		↓
	'''
	for block in blocks:
		# ブロックが動かせるとき、サイズ2倍で計算
		if getattr(block, 'movable', False):
			size = BLOCK_SIZE*2
		else:
			size = BLOCK_SIZE
		if (abs(block.x - obake.x) < (IMG_WIDTH + size)/2 - 2
				and block.y + size <= obake.y <= block.y + size + IMG_HEIGHT/2):
			if block.param == 'udarrow' and grav_dir == 'd':
				change_gravity('ud')
			return True


def on_block(kind):
	'''
	キャラが特定のブロックに接しているかどうか

	Parameters
	----------
	kind : str -> 'jump' | 'dark'
		ブロックの種類
	
	Returns
	-------
	bool
	'''
	if kind == 'jump': collection = 'gold2'
	elif kind == 'dark': collection = ['purple4', 'MediumPurple4']
	if grav_dir == 'd':
		for block in blocks:
			if (block.param in collection
					and abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
					and block.y - IMG_HEIGHT/2 <= obake.y <= block.y):
				return True
	elif grav_dir == 'u':
		for block in blocks:
			if (block.param in collection
					and abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
					and block.y + BLOCK_SIZE <= obake.y <= block.y + BLOCK_SIZE + IMG_HEIGHT/2):
				return True


def change_gravity(kind):
	'''重力の方向を変える
	
	Parameters
	----------
	kind : str -> 'ud' | 'cw' | 'acw'
		方向変化の種類．
	'''
	global grav_dir
	if kind == 'ud':
		if grav_dir == 'd':
			grav_dir = 'u'
			obake.delete()
			obake.id = cv.create_image(obake.x, obake.y,
				image=(obake_flip_tkimg if obake.seeing_direction == 'l' else obake_fm_tkimg))
			obake.y += BLOCK_SIZE
		elif grav_dir == 'u':
			grav_dir = 'd'
			obake.delete()
			obake.id = cv.create_image(obake.x, obake.y,
				image=(obake_tkimg if obake.seeing_direction == 'l' else obake_mirror_tkimg))
			obake.y -= BLOCK_SIZE


# システム関連の処理
def addtime():
	global time, timer
	time += 0.125
	cv.delete('timer')
	cv.create_text(WINDOW_WIDTH - 2*TIMER_TEXT_SIZE, TIMER_TEXT_SIZE,
		text=f'{time:>7.3f}', fill='gray20', font=("System", TIMER_TEXT_SIZE), tag='timer')
	timer = root.after(125, addtime)


def judge_goal():
	global timer
	if (not stage.clear
			and abs(obake.x - (cv.coords(goal)[0] + cv.coords(goal)[2])/2 + BLOCK_SIZE/2) < IMG_WIDTH
			and abs(obake.y - (cv.coords(goal)[1] + cv.coords(goal)[3])/2 + BLOCK_SIZE/2) < IMG_HEIGHT):
		clear_snd.play()
		root.after_cancel(timer)
		stage.clear = True
		root.title(f'{stage.name} - CLEAR!')
		cv.create_text(WINDOW_WIDTH/2, CLEAR_TEXT_SIZE,
				text='STAGE CLEAR!', fill='LimeGreen', font=("System", CLEAR_TEXT_SIZE),
				justify='center', tag='clear')
		cv.bind('N', to_next_stage)


def to_next_stage(event):
	global stage
	if stage.clear and stage.next_stage is not None:
		stage = stage.next_stage()
		root.title(stage.name)
		init_game(stage.goal_pos, stage.obake_pos)


def init_game(goal_pos, start_pos):
	global grav_dir, goal, obake, blocks, time
	grav_dir = 'd'
	cv.delete('all')
	# インスタンス削除
	if obake is not None:
		del obake
	if blocks:
		for block in blocks:
			del block
	# ゴールの描画
	goal = cv.create_rectangle(BLOCK_SIZE*(goal_pos[0] - 1/2),
		WINDOW_HEIGHT - BLOCK_SIZE*(goal_pos[1] + 1/2),
		BLOCK_SIZE*(goal_pos[0] + 1/2),
		WINDOW_HEIGHT - BLOCK_SIZE*(goal_pos[1] + 3/2),
		fill='orange')
	# インスタンス生成
	# キャラ
	obake = Obake(BLOCK_SIZE*start_pos[0],
		WINDOW_HEIGHT - BLOCK_SIZE*start_pos[1] - IMG_HEIGHT/2)
	# 看板
	for x, y, img_name in getattr(stage, 'signs', []):
		cv.create_image(BLOCK_SIZE*x,
			WINDOW_HEIGHT - BLOCK_SIZE*(y + 1.4), image=sign_img[img_name])
	# ブロック
	blocks = []
	for y, row in stage.blocks.items():
		for i, param in enumerate(row):
			if param is not None:
				block = Block(BLOCK_SIZE*(i + 1/2),
					WINDOW_HEIGHT - BLOCK_SIZE*(y + 1), param)
				blocks.append(block)
	for x, y, param in getattr(stage, 'movable_block_pos', []):
		block = Block(BLOCK_SIZE*x,
			WINDOW_HEIGHT - BLOCK_SIZE*(y + 2), param, True)
		blocks.append(block)
	
	time = 0
	addtime()


def restart_game(*event):
	global grav_dir, obake, time
	grav_dir = 'd'
	# クリア文字消去
	cv.delete('clear')
	# もとのインスタンスを削除
	obake.delete()
	del obake
	if hasattr(stage, 'movable_block_pos'):
		for block in blocks:
			if block.movable:
				cv.delete(block.id)
				del block
		del blocks[-len(getattr(stage, 'movable_block_pos', [])):]
	# インスタンス生成
	obake = Obake(BLOCK_SIZE*stage.obake_pos[0],
		WINDOW_HEIGHT - BLOCK_SIZE*stage.obake_pos[1] - IMG_HEIGHT/2)
	for x, y, param in getattr(stage, 'movable_block_pos', []):
		block = Block(BLOCK_SIZE*x,
			WINDOW_HEIGHT - BLOCK_SIZE*(y + 2), param, True)
		blocks.append(block)
	
	time = 0


if __name__ == '__main__':
	# ステージ
	args = sys.argv
	if len(args) >= 2 and args[1].isdigit():
		stage_class = getattr(stages, f'Stage{int(args[1])}', None)
		if stage_class is None:
			print('不正なコマンドライン引数です。1 ~ 8 の整数値を指定してください。')
			sys.exit()
		else: stage = stage_class()
	else:
		stage = stages.Stage1()
	
	# 初期描画
	root = tk.Tk()
	root.title(stage.name)
	root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+0+0')
	cv = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='white')
	cv.pack()
	cv.focus_set()

	# 画像の読み込み
	# キャラクター
	obake_img = Image.open('./img/obake.png')
	obake_img = obake_img.resize((IMG_SIZE, IMG_SIZE))
	obake_flip_img = ImageOps.flip(obake_img)		# 上下反転
	obake_mirror_img = ImageOps.mirror(obake_img)	# 左右反転（右向き）
	obake_fm_img = ImageOps.mirror(obake_flip_img)	# 上下左右反転
	obake_tkimg = ImageTk.PhotoImage(obake_img)
	obake_flip_tkimg = ImageTk.PhotoImage(obake_flip_img)
	obake_mirror_tkimg = ImageTk.PhotoImage(obake_mirror_img)
	obake_fm_tkimg = ImageTk.PhotoImage(obake_fm_img)
	# 重力ブロック
	udarrow_img = Image.open('./img/updownarrow.png')
	udarrow_img = udarrow_img.resize((BLOCK_SIZE, BLOCK_SIZE))
	udarrow2_img = udarrow_img.resize((BLOCK_SIZE*2, BLOCK_SIZE*2))
	udarrow_tkimg = ImageTk.PhotoImage(udarrow_img)
	udarrow2_tkimg = ImageTk.PhotoImage(udarrow2_img)
	# 看板
	triple_size = (BLOCK_SIZE*3, BLOCK_SIZE*3)
	dsc_J_img = Image.open(f'./img/dsc_J.png').resize(triple_size)
	dsc_K_img = Image.open(f'./img/dsc_K.png').resize(triple_size)
	dsc_L_img = Image.open(f'./img/dsc_L.png').resize(triple_size)
	dsc_dash_img = Image.open(f'./img/dsc_dash.png').resize(triple_size)
	dsc_push_img = Image.open(f'./img/dsc_push.png').resize(triple_size)
	dsc_dark_img = Image.open(f'./img/dsc_dark.png').resize(triple_size)
	dsc_gravity_img = Image.open(f'./img/dsc_gravity.png').resize(triple_size)
	dsc_J_tkimg = ImageTk.PhotoImage(dsc_J_img)
	dsc_K_tkimg = ImageTk.PhotoImage(dsc_K_img)
	dsc_L_tkimg = ImageTk.PhotoImage(dsc_L_img)
	dsc_dash_tkimg = ImageTk.PhotoImage(dsc_dash_img)
	dsc_push_tkimg = ImageTk.PhotoImage(dsc_push_img)
	dsc_dark_tkimg = ImageTk.PhotoImage(dsc_dark_img)
	dsc_gravity_tkimg = ImageTk.PhotoImage(dsc_gravity_img)
	# 画像名と画像の対応
	sign_img = {'dsc_J': dsc_J_tkimg, 'dsc_K': dsc_K_tkimg, 'dsc_L': dsc_L_tkimg,
		'dsc_dash': dsc_dash_tkimg, 'dsc_push': dsc_push_tkimg,
		'dsc_dark': dsc_dark_tkimg, 'dsc_gravity': dsc_gravity_tkimg}

	# メニューバー
	menubar = tk.Menu(root)
	root.configure(menu=menubar)
	menubar.add_command(label='RESTART', underline=0, command=restart_game)

	# キーバインド（リスタート）
	cv.bind('R', restart_game)

	# 初期化
	obake = None
	blocks = []
	init_game(stage.goal_pos, stage.obake_pos)

	# 音声の設定
	pygame.mixer.init()
	jump_snd = pygame.mixer.Sound('jump.wav')
	clear_snd = pygame.mixer.Sound('clear.wav')

	root.mainloop()
