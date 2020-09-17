import os
import math
from ctypes import windll
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import pygame

from stages import Stage6


# ステージ
stage = Stage6()

# 画面サイズ
DISP_W = windll.user32.GetSystemMetrics(0)
DISP_H = windll.user32.GetSystemMetrics(1)

if DISP_W < 900 or DISP_H < 900:
	# ウィンドウサイズ
	WINDOW_WIDTH = 600
	WINDOW_HEIGHT = 600

	# STAGE CLEAR テキストサイズ
	TEXT_SIZE = 60

	# ブロックサイズ
	BLOCK_SIZE = 20

	# キャラサイズ
	IMG_SIZE = 36
	IMG_WIDTH = 30
	IMG_HEIGHT = 30

	# 横移動速度
	MOVE_V = 4
	# ジャンプ初速度
	JUMP_V0 = 20
else:
	# ウィンドウサイズ
	WINDOW_WIDTH = int(600*1.5)
	WINDOW_HEIGHT = int(600*1.5)

	# STAGE CLEAR テキストサイズ
	TEXT_SIZE = int(60*1.5)

	# ブロックサイズ
	BLOCK_SIZE = int(20*1.5)

	# キャラサイズ
	IMG_SIZE = int(36*1.5)
	IMG_WIDTH = int(30*1.5)
	IMG_HEIGHT = int(30*1.5)

	# 横移動速度
	MOVE_V = 4*1.5
	# ジャンプ初速度
	JUMP_V0 = 20*1.5
	
# ジャンプブロック初速係数
JUMP_M = 6

# 重力加速度
ga = JUMP_V0/6

# 重力の方向
# u: ↑, d: ↓, l: ←, r: →
grav_dir = 'd'


# キャラクター
class Obake:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = IMG_WIDTH
		self.height = IMG_HEIGHT
		# アニメーションの時刻
		self.time_x = 0
		self.time_y = 0
		# ジャンプ中or落下中
		self.flying = False
		# ダークブロックの影響下
		self.isdark = False
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
		cv.bind("l", self.move_right)
		cv.bind("j", self.move_left)
		cv.bind("k", self.jump)

	def move_right(self, event):
		if self.time_x > 0 and self.isdark: return
		# 画像左右反転
		self.delete()
		if grav_dir == 'd':
			self.id = cv.create_image(self.x, self.y, image=obake_mirror_tkimg)
		elif grav_dir == 'u':
			self.id = cv.create_image(self.x, self.y, image=obake_fm_tkimg)
		self.time_x = 0
		self.r_move()
	
	def move_left(self, event):
		if self.time_x > 0 and self.isdark: return
		# 画像左右反転
		self.delete()
		if grav_dir == 'd':
			self.id = cv.create_image(self.x, self.y, image=obake_tkimg)
		elif grav_dir == 'u':
			self.id = cv.create_image(self.x, self.y, image=obake_flip_tkimg)
		self.time_x = 0
		self.l_move()
	
	def r_move(self):
		xtmp = self.x
		self.x += MOVE_V
		if not self.flying:
			self.fall_move()
		if hitting_block_x(self):
			self.x = xtmp
			self.time_x = 0
			cv.coords(self.id, self.x, self.y)
			return
		if self.flying or self.time_x < 5:
			self.time_x += 1
			root.after(50, self.r_move)
		else:
			self.time_x = 0
		cv.coords(self.id, self.x, self.y)
		judge_goal()
	
	def l_move(self):
		xtmp = self.x
		self.x -= MOVE_V
		if not self.flying:
			self.fall_move()
		if hitting_block_x(self):
			self.x = xtmp
			self.time_x = 0
			cv.coords(self.id, self.x, self.y)
			return
		if self.flying or self.time_x < 5:
			self.time_x += 1
			root.after(50, self.l_move)
		else:
			self.time_x = 0
		cv.coords(self.id, self.x, self.y)
		judge_goal()
	
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
	
	def jump(self, event):
		if self.flying or on_block('dark'): return
		jump_snd.play()
		self.flying = True
		self.jump_move()
	
	def jump_move(self):
		v0 = JUMP_M*JUMP_V0 if on_block('jump') else JUMP_V0
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
				root.after(50, self.jump_move)
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
				root.after(50, self.jump_move)
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

	abs(block.x - obj.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2

	  BLOCK_SIZE
		┌ x ┐
		│   │		block
	┌ ─ ┼ ─ ┼ ─ ┐
	│ x │   │ x │	obake
	└ ─ ┘ ↔ └ ─ ┘
		  IMG_WIDTH
	
	block.y + BLOCK_SIZE <= obake.y <= block.y + BLOCK_SIZE + IMG_HEIGHT/2

		┌ y ┐		↑
	  ⇡ │   │  BLOCK_SIZE
	┌ ─ ┼ ─ ┘	↑	↓
	│ y │   IMG_HEIGHT
	└ ─ ┘ 		↓
	'''
	for block in blocks:
		if (abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
				and block.y + BLOCK_SIZE <= obake.y <= block.y + BLOCK_SIZE + IMG_HEIGHT/2):
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
			obake.id = cv.create_image(obake.x, obake.y, image=obake_flip_tkimg)
			obake.y += BLOCK_SIZE
		elif grav_dir == 'u':
			grav_dir = 'd'
			obake.delete()
			obake.id = cv.create_image(obake.x, obake.y, image=obake_tkimg)
			obake.y -= BLOCK_SIZE


# システム関連の関数
def judge_goal():
	if (not stage.clear
			and abs(obake.x - cv.coords(goal)[0] + BLOCK_SIZE/2) < IMG_WIDTH
			and abs(obake.y - cv.coords(goal)[1] + BLOCK_SIZE/2) < IMG_HEIGHT):
				clear_snd.play()
				stage.clear = True
				root.title(f'{stage.name} - CLEAR!')
				cv.create_text(WINDOW_WIDTH/2, TEXT_SIZE,
						text='STAGE CLEAR!', fill='LimeGreen', font=("System", TEXT_SIZE),
						justify='center', tag='clear')
				cv.bind('N', to_next_stage)


def to_next_stage(event):
	global stage
	if stage.clear:
		stage = stage.next_stage()
		root.title(stage.name)
		init_game(stage.goal_pos, stage.obake_pos)


def init_game(goal_pos, start_pos):
	global grav_dir, goal, obake, blocks
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


def restart_game(*event):
	global grav_dir, obake
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


if __name__ == '__main__':
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
