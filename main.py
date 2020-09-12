import os
import math
import tkinter as tk
from PIL import Image, ImageTk
import pygame

from stages import Stage5


# ステージ
stage = Stage5()

# ウィンドウサイズ
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

# STAGE CLEAR テキストサイズ
TEXT_SIZE = 60

# ブロックサイズ
BLOCK_SIZE = 20

# キャラ幅
IMG_WIDTH = 40

# 横移動速度
MOVE_V = 4
# ジャンプ初速度
JUMP_V0 = 22
# 重力加速度
GA = JUMP_V0/5
# ジャンプブロック初速係数
JUMP_M = 5.5

# 重力の方向
# u: ↑, d: ↓, l: ←, r: →
glav_dir = 'd'


# キャラクター
class Obake:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		# アニメーションの時刻
		self.time_x = 0
		self.time_y = 0
		# ジャンプ中or落下中
		self.flying = False
		self.draw()
		self.bind()
	
	def delete(self):
		cv.delete(self.id)

	def draw(self):
		'''
		一辺の長さ IMG_WIDTH の正方形
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
		if self.flying: return
		if self.time_x > 0 and on_dark_block(): return
		self.time_x = 0
		self.r_move()
	
	def move_left(self, event):
		if self.flying: return
		if self.time_x > 0 and on_dark_block(): return
		self.time_x = 0
		self.l_move()
	
	def r_move(self):
		xtmp = self.x
		self.x += MOVE_V
		if not self.flying:
			self.fall_move()
		if hitting_block_x(self, IMG_WIDTH):
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
		if hitting_block_x(self, IMG_WIDTH):
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
		dy = min(GA*self.time_y, 20)
		if glav_dir == 'd':
			self.y += dy
			if self.y > WINDOW_HEIGHT:
				# 画面外に出た
				restart_game()
			elif hitting_block_floor(self, IMG_WIDTH):
				# 床に乗った
				self.y = math.floor(self.y/BLOCK_SIZE)*BLOCK_SIZE
				self.time_y = 0
				self.flying = False
			else:
				self.flying = True
				self.time_y += 1
				root.after(50, self.fall_move)
		elif glav_dir == 'u':
			self.y -= dy
			if self.y < 0:
				# 画面外に出た
				restart_game()
			elif hitting_block_ceil():
				# 床に乗った
				self.y = math.ceil(self.y/BLOCK_SIZE)*BLOCK_SIZE
				self.time_y = 0
				self.flying = False
			else:
				self.flying = True
				self.time_y += 1
				root.after(50, self.fall_move)
		cv.coords(self.id, self.x, self.y)
		judge_goal()
	
	def jump(self, event):
		if self.flying or on_dark_block(): return
		jump_snd.play()
		self.flying = True
		self.jump_move()
	
	def jump_move(self):
		v0 = JUMP_M*JUMP_V0 if on_jump_block() else JUMP_V0
		dy = max(v0 - GA*self.time_y, -20)
		if glav_dir == 'd':
			self.y -= dy
			if self.y > WINDOW_HEIGHT:
				# 画面外に出た
				restart_game()
			elif hitting_block_ceil():
				# 天井に当たった
				self.fall_move()
				return
			elif hitting_block_floor(self, IMG_WIDTH):
				# 床に乗った
				self.y = math.floor(self.y/BLOCK_SIZE)*BLOCK_SIZE
				self.time_y = 0
				self.flying = False
			else:
				self.time_y += 1
				root.after(50, self.jump_move)
		elif glav_dir == 'u':
			self.y += dy
			if self.y < 0:
				# 画面外に出た
				restart_game()
			elif hitting_block_floor(self, IMG_WIDTH):
				# 天井に当たった
				self.fall_move()
				return
			elif hitting_block_ceil():
				# 床に乗った
				self.y = math.ceil(self.y/BLOCK_SIZE)*BLOCK_SIZE
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
			self.id = cv.create_rectangle(self.x - BLOCK_SIZE, self.y,
				self.x + BLOCK_SIZE, self.y + 2*BLOCK_SIZE,
				fill=self.param)
		else:
			if 'arrow' in self.param:
				if self.param == 'udarrow': _img = udarrow_tkimg
				cv.create_image(self.x, self.y, image=_img)
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
		if hitting_block_x(self, 2*BLOCK_SIZE):
			self.x = xtmp
		cv.coords(self.id, self.x - BLOCK_SIZE, self.y,
			self.x + BLOCK_SIZE, self.y + 2*BLOCK_SIZE)
	
	def fall_move(self):
		self.y += min(GA*self.time_y, 20)
		if self.y > WINDOW_HEIGHT:
			# 画面外に出た
			cv.delete(self.id)
		elif hitting_block_floor(self, 2*BLOCK_SIZE):
			# 床に乗った
			self.y = (self.y//BLOCK_SIZE)*BLOCK_SIZE
			self.time_y = 0
		else:
			self.time_y += 1
			root.after(50, self.fall_move)
		cv.coords(self.id, self.x - BLOCK_SIZE, self.y,
			self.x + BLOCK_SIZE, self.y + 2*BLOCK_SIZE)


# ブロックとの関係を判定する関数
def hitting_block_x(obj, width):
	'''
	キャラがブロックに横からぶつかっているかどうか

	Parameters
	----------
	obj : obj -> Obake | Block
		obake または動かせるブロックのオブジェクト．
	width : int > 0
		obj の幅．
	
	Returns
	-------
	bool

	Notes
	-----
	if 文条件式の図

	abs(block.x - obj.x) < (width + BLOCK_SIZE)/2
	
	width
	┌ x ┐ ↔ ┌ x ┐
	│ x │   │ x │	obj
	└ ─ ┼ x ┼ ─ ┘
	    │   │		block
	    └ ─ ┘
	  BLOCK_SIZE
	
	-(h + BLOCK_SIZE) < block.y - obj.y < width/2
	(obj.y - block.y < h + BLOCK_SIZE) and (block.y - obj.y < width - h)

	     obj  block
	h ↕ ┌ y ┐     ↑
	  ⇣ │ y │   width
	    └ ─ ┼ y ┐ ↓   ↑
	      ↕ │   │ BLOCK_SIZE
	h ↕ ┌ y ┼ ─ ┘     ↓
	  ⇣ │ y │
	    └ ─ ┘
	'''
	for block in blocks:
		if obj == block: continue
		# obj が動かせるブロックのとき、高さの当たり判定を0に
		if getattr(obj, 'movable', False):
			h = 0
		else:
			h = width/2
		if (abs(block.x - obj.x) < (width + BLOCK_SIZE)/2
				and -(h + BLOCK_SIZE) < block.y - obj.y < width - h):
			if block.movable:
				# ブロックが動かせるとき
				block.slide_move()
			return True


def hitting_block_floor(obj, width):
	'''
	キャラや動かせるブロックがブロックに上から接しているかどうか

	Parameters
	----------
	obj : obj -> Obake | Block
		obake または動かせるブロックのオブジェクト．
	width : int > 0
		obj の幅．
	
	Returns
	-------
	bool

	Notes
	-----
	if 文条件式の図

	abs(block.x - obj.x) < (width + w)/2 - 2

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
			h = width
		else:
			h = width/2
		if (abs(block.x - obj.x) < (width + w)/2 - 2
				and block.y - h <= obj.y <= block.y):
			if (block.param == 'udarrow'
					and not getattr(obj, 'movable', False)
					and glav_dir == 'u'):
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
	
	block.y + BLOCK_SIZE <= obake.y <= block.y + BLOCK_SIZE + IMG_WIDTH/2

		┌ y ┐		↑
	  ⇡ │   │  BLOCK_SIZE
	┌ ─ ┼ ─ ┘	↑	↓
	│ y │   IMG_WIDTH
	└ ─ ┘ 		↓
	'''
	for block in blocks:
		if (abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
				and block.y + BLOCK_SIZE <= obake.y <= block.y + BLOCK_SIZE + IMG_WIDTH/2):
			if block.param == 'udarrow' and glav_dir == 'd':
				change_gravity('ud')
			return True


def on_jump_block():
	'''
	キャラが黄色ブロックに上から接しているかどうか
	
	Returns
	-------
	bool
	'''
	for block in blocks:
		if (block.param in 'gold2'
				and abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
				and block.y - (IMG_WIDTH + BLOCK_SIZE)/2 <= obake.y <= block.y - (BLOCK_SIZE)/2):
			return True


def on_dark_block():
	'''
	キャラが紫色ブロックに上から接しているかどうか
	
	Returns
	-------
	bool
	'''
	for block in blocks:
		if (block.param in ['purple4', 'MediumPurple4']
				and abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
				and block.y - (IMG_WIDTH + BLOCK_SIZE)/2 <= obake.y <= block.y - (BLOCK_SIZE)/2):
			return True


def change_gravity(kind):
	'''重力の方向を変える
	
	Parameters
	----------
	kind : str -> 'ud' | 'cw' | 'acw'
		方向変化の種類．
	'''
	global glav_dir
	if kind == 'ud':
		if glav_dir == 'd':
			glav_dir = 'u'
			obake.delete()
			obake.id = cv.create_image(obake.x, obake.y, image=obake_180_tkimg)
			obake.y += BLOCK_SIZE
		elif glav_dir == 'u':
			glav_dir = 'd'
			obake.delete()
			obake.id = cv.create_image(obake.x, obake.y, image=obake_tkimg)
			obake.y -= BLOCK_SIZE


# システム関連の関数
def judge_goal():
	if (not stage.clear
			and abs(obake.x - cv.coords(goal)[0] + BLOCK_SIZE/2) < IMG_WIDTH
			and abs(obake.y - cv.coords(goal)[1] + BLOCK_SIZE/2) < IMG_WIDTH):
                clear_snd.play()
                stage.clear = True
                cv.create_text(WINDOW_WIDTH/2, TEXT_SIZE,
                        text='STAGE CLEAR!', fill='LimeGreen', font=("System", TEXT_SIZE),
                        justify='center', tag='clear')
                cv.bind('N', to_next_stage)


def to_next_stage(event):
	global stage
	if stage.clear:
		stage = stage.next_stage()
		root.title(stage.name)
		init_game(stage.goal_pos, stage.obake_pos, stage.blocks)


def init_game(goal_pos, start_pos, blocks_dict):
	global glav_dir, goal, obake, blocks
	glav_dir = 'd'
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
	obake = Obake(BLOCK_SIZE*start_pos[0], WINDOW_HEIGHT - BLOCK_SIZE*start_pos[1] - IMG_WIDTH/2)
	# ブロック
	blocks = []
	for y, row in blocks_dict.items():
		for i, param in enumerate(row):
			if param is not None:
				block = Block(BLOCK_SIZE*(i + 1/2),
					WINDOW_HEIGHT - BLOCK_SIZE*(y + 1), param)
				blocks.append(block)
	if hasattr(stage, 'movable_block_pos'):
		for x, y, param in stage.movable_block_pos:
			block = Block(BLOCK_SIZE*x,
				WINDOW_HEIGHT - BLOCK_SIZE*(y + 2), param, True)
			blocks.append(block)


def restart_game(*event):
	global glav_dir, obake
	glav_dir = 'd'
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
		del blocks[-len(stage.movable_block_pos):]
	# インスタンス生成
	obake = Obake(BLOCK_SIZE*stage.obake_pos[0], WINDOW_HEIGHT - BLOCK_SIZE*stage.obake_pos[1] - IMG_WIDTH/2)
	if hasattr(stage, 'movable_block_pos'):
		for x, y, param in stage.movable_block_pos:
			block = Block(BLOCK_SIZE*x,
				WINDOW_HEIGHT - BLOCK_SIZE*(y + 2), param, True)
			blocks.append(block)


if __name__ == '__main__':
	# 初期描画
	root = tk.Tk()
	root.title(stage.name)
	cv = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='white')
	cv.pack()
	cv.focus_set()

	# 画像の読み込み
	# キャラクター
	obake_img = Image.open('obake.png')
	obake_img = obake_img.resize((IMG_WIDTH, IMG_WIDTH))
	obake_180_img = obake_img.rotate(180)
	obake_tkimg = ImageTk.PhotoImage(obake_img)
	obake_180_tkimg = ImageTk.PhotoImage(obake_180_img)
	# 重力ブロック
	udarrow_img = Image.open('updownarrow.png')
	udarrow_img = udarrow_img.resize((BLOCK_SIZE, BLOCK_SIZE))
	udarrow_tkimg = ImageTk.PhotoImage(udarrow_img)

	# メニューバー
	menubar = tk.Menu(root)
	root.configure(menu=menubar)
	menubar.add_command(label='RESTART', underline=0, command=restart_game)

	# キーバインド（リスタート）
	cv.bind('R', restart_game)

	# 初期化
	obake = None
	blocks = []
	init_game(stage.goal_pos, stage.obake_pos, stage.blocks)

	# 音声の設定
	pygame.mixer.init()
	jump_snd = pygame.mixer.Sound('jump.wav')
	clear_snd = pygame.mixer.Sound('clear.wav')

	root.mainloop()
