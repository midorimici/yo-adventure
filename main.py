import tkinter as tk
from PIL import Image, ImageTk

from stages import Stage3

# ウィンドウサイズ
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

# STAGE CLEAR テキストサイズ
TEXT_SIZE = 60

# ブロックサイズ
BLOCK_SIZE = 20

# キャラ幅
IMG_WIDTH = 40

# ジャンプ初速度
JUMP_V0 = 20
# 重力加速度
GA = JUMP_V0/5

# ステージ
stage = Stage3()


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
		self.id = cv.create_image(self.x, self.y, image=obake_tkimg)

	def bind(self):
		cv.bind("l", self.move_right)
		cv.bind("j", self.move_left)
		cv.bind("k", self.jump)

	def move_right(self, event):
		if self.flying: return
		self.time_x = 0
		self.r_move()
	
	def move_left(self, event):
		if self.flying: return
		self.time_x = 0
		self.l_move()
	
	def r_move(self):
		xtmp = self.x
		self.x += 4
		if not self.flying:
			self.fall_move()
		if hitting_block_x():
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
		self.x -= 4
		if not self.flying:
			self.fall_move()
		if hitting_block_x():
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
		self.y += min(GA*self.time_y, 20)
		if self.y > WINDOW_HEIGHT:
			# 画面外に出た
			restart_game()
		elif hitting_block_floor():
			# 床に乗った
			self.y = (self.y//BLOCK_SIZE)*BLOCK_SIZE
			self.time_y = 0
			self.flying = False
		else:
			self.flying = True
			self.time_y += 1
			root.after(50, self.fall_move)
		cv.coords(self.id, self.x, self.y)
		judge_goal()
	
	def jump(self, event):
		if not self.flying:
			self.flying = True
			self.jump_move()
	
	def jump_move(self):
		v0 = 6*JUMP_V0 if on_jump_block() else JUMP_V0
		self.y -= max(v0 - GA*self.time_y, -20)
		if self.y > WINDOW_HEIGHT:
			# 画面外に出た
			restart_game()
		elif hitting_block_ceil():
			# 天井に当たった
			self.fall_move()
			return
		elif hitting_block_floor():
			# 床に乗った
			self.y = (self.y//BLOCK_SIZE)*BLOCK_SIZE
			self.time_y = 0
			self.flying = False
		else:
			self.time_y += 1
			root.after(50, self.jump_move)
		cv.coords(self.id, self.x, self.y)
		judge_goal()


# ブロック
class Block:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color
		self.draw()
	
	def draw(self):
		cv.create_rectangle(self.x - BLOCK_SIZE/2, self.y - BLOCK_SIZE/2,
			self.x + BLOCK_SIZE/2, self.y + BLOCK_SIZE/2,
			fill=self.color)


def hitting_block_x():
	'''
	キャラがブロックに横からぶつかっているかどうか
	
	Returns
	-------
	bool
	'''
	for block in blocks:
		if (abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2
				and abs(block.y - obake.y) < (IMG_WIDTH + BLOCK_SIZE)/2):
			return True


def hitting_block_floor():
	'''
	キャラがブロックに上から接しているかどうか
	
	Returns
	-------
	bool
	'''
	for block in blocks:
		if (abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
				and block.y - (IMG_WIDTH + BLOCK_SIZE)/2 <= obake.y <= block.y - (BLOCK_SIZE)/2):
			return True


def hitting_block_ceil():
	'''
	キャラがブロックに下からぶつかっているかどうか
	
	Returns
	-------
	bool
	'''
	for block in blocks:
		if (abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
				and block.y + (BLOCK_SIZE)/2 <= obake.y <= block.y + (IMG_WIDTH + BLOCK_SIZE)/2):
			return True


def on_jump_block():
	'''
	キャラが黄色ブロックに上から接しているかどうか
	
	Returns
	-------
	bool
	'''
	for block in blocks:
		if (block.color == 'gold'
				and abs(block.x - obake.x) < (IMG_WIDTH + BLOCK_SIZE)/2 - 2
				and block.y - (IMG_WIDTH + BLOCK_SIZE)/2 <= obake.y <= block.y - (BLOCK_SIZE)/2):
			return True


def judge_goal():
	if (abs(obake.x - cv.coords(goal)[0] + BLOCK_SIZE/2) < IMG_WIDTH
			and abs(obake.y - cv.coords(goal)[1] + BLOCK_SIZE/2) < IMG_WIDTH):
		stage.clear = True
		cv.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/4,
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
	global goal, obake, blocks
	cv.delete('all')
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
	for y, b in blocks_dict.items():
		for i, color in enumerate(b):
			if color is not None:
				block = Block((i + 1/2)*BLOCK_SIZE,
					WINDOW_HEIGHT - (y + 1/2)*BLOCK_SIZE, color)
				blocks.append(block)


def restart_game(*event):
	global obake
	# クリア文字消去
	cv.delete('clear')
	# もとのインスタンスを削除
	obake.delete()
	del obake
	# キャラインスタンス生成
	obake = Obake(BLOCK_SIZE*stage.obake_pos[0], WINDOW_HEIGHT - BLOCK_SIZE*stage.obake_pos[1] - IMG_WIDTH/2)


if __name__ == '__main__':
	# 初期描画
	root = tk.Tk()
	root.title(stage.name)
	cv = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='white')
	cv.pack()
	cv.focus_set()

	# 画像の読み込み
	obake_img = Image.open('obake.png')
	obake_img = obake_img.resize((IMG_WIDTH, IMG_WIDTH))
	obake_tkimg = ImageTk.PhotoImage(obake_img)

	# メニューバー
	menubar = tk.Menu(root)
	root.configure(menu=menubar)
	menubar.add_command(label='RESTART', underline=0, command=restart_game)

	# キーバインド（リスタート）
	cv.bind('R', restart_game)

	# 初期化
	init_game(stage.goal_pos, stage.obake_pos, stage.blocks)

	root.mainloop()