#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: 张天弈


"""
Python 3.4.4
Pygame 1.9.1
基于Python及其模块Pygame实现的LongPlay音乐播放器
支持MP3, OGG, WAV格式的音频
默认随机播放
可以用上下箭头或点击音量图标控制音量
可以用左右箭头或点击前后图标切换音乐
可以用空格键开始或暂停音乐
按停止键有2.5秒淡出效果
可添加或删除音乐
有用户注册及登录功能
由正则表达式匹配用户名与密码
可选择是否注册账户
使用MD5方法进行数据加密
"""


# 导入所需模块5
import sys
import pygame
from pygame.locals import *
import os
import os.path
import hashlib
from collections import defaultdict
import re
import pickle
import pprint
import shutil


# 存放音乐文件的位置
MUSIC_PATH = 'source'


# 屏幕大小
SCREEN_SIZE = (1000, 625)


# 背景图片
background_image_filename = 'image/background.jpg'
disk_image_filename = 'image/disk.png'
stick_image_filename = 'image/stick.png'
bar_image_filename = 'image/bar.png'
circle_image_filename = 'image/circle.png'


# 设置字典初始值为N/A
db = defaultdict(lambda: 'N/A')


# 语言
class Language(object):

	def __init__(self):
		pass

	@staticmethod
	def choose(self):
		num = input('1 English, 2 中文:')
		return num


# 英文开始模式
class Select(object):

	def __init__(self):
		pass

	@staticmethod
	def choose(self):
		num = input('1 to create an account, 2 to log in, 3 to start without logging in:')
		return num


# 中文开始模式
class SelectChinese(object):

	def __init__(self):
		pass

	@staticmethod
	def choose(self):
		num = input('按1创建账户, 按2登录, 按3不登录直接启动:')
		return num


# 英文注册登录
class Registration(object):

	def __init__(self):
		self.username = ''
		self.password = ''

	# 注册
	def start(self):
		username = input(
			'Please create the username(Must be 3-10 characters or numbers, no Chinese or space allowed):')
		# 正则匹配
		if re.match(r'\w{3,10}', username):
			self.username = username
		else:
			print('Input error!')
		# 输入错误则重新输入
		while self.username != username:
			self.start()
		password = input(
			'Please create the password(Must be 6-20 characters or numbers, no Chinese or space allowed):')
		# 正则匹配
		if re.match(r'\w{6,20}', password):
			self.password = password
		# 输入错误则重新输入
		while self.password != password:
			self.start()

	# 静态方法求MD5
	@staticmethod
	def getmd5(s):
		md5 = hashlib.md5()
		md5.update(s.encode('utf-8'))
		return md5.hexdigest()

	def register(self):
		self.start()
		# MD5加密
		db[self.username] = self.getmd5(self.password + self.username)
		# 将信息通过dict类型格式化二进制存入文件中
		_file = open('info/user.pkl', 'wb')
		data = {'Username': (self.getmd5(self.username), u'Unicode'), 'Password': (self.getmd5(self.password), u'Unicode')}
		try:
			pickle.dump(data, _file)
		finally:
			_file.close()
		print('Registration successful！')

	# 登录
	def login(self):
		username = input('Please input the username:')
		password = input('Please input the password:')
		# 用中间变量测试用户信息
		data = {'Username': (self.getmd5(username), u'Unicode'), 'Password': (self.getmd5(password), u'Unicode')}
		_file = open('info/user.pkl', 'rb')
		try:
			_temp = pickle.load(_file)
		finally:
			_file.close()
		# 验证用户信息
		if data == _temp:
			print('Logging in successful！')
			return True
		else:
			print('Error！')
			return False

	def get_username(self):
		return self.username

	def get_password(self):
		return self.password

	def main_reg(self):
		print('Start registration')
		self.register()

	def main(self):
		print('Start logging in')
		d = self.login()
		while not d:
			d = self.login()


# 中文注册登录
class RegistrationChinese(object):

	def __init__(self):
		self.username = ''
		self.password = ''

	# 注册
	def start(self):
		username = input('请创建用户名(必须是3-10位英文字母或数字, 不能包含空格或中文):')
		# 正则匹配
		if re.match(r'\w{3,10}', username):
			self.username = username
		else:
			print('Input error!')
		# 输入错误则重新输入
		while self.username != username:
			self.start()
		password = input('请创建密码(必须是6-20位英文字母或数字, 不能包含空格或中文):')
		# 正则匹配
		if re.match(r'\w{6,20}', password):
			self.password = password
		# 输入错误则重新输入
		while self.password != password:
			self.start()

	def register(self):
		self.start()
		# MD5加密
		db[self.username] = self.getmd5(self.password + self.username)
		# 将信息通过dict类型格式化二进制存入文件中
		_file = open('info/user.pkl', 'wb')
		data = {'Username': (self.getmd5(self.username), u'Unicode'), 'Password': (self.getmd5(self.password), u'Unicode')}
		try:
			pickle.dump(data, _file)
		finally:
			_file.close()
		print('创建账户成功！')

	# 静态方法求MD5
	@staticmethod
	def getmd5(s):
		md5 = hashlib.md5()
		md5.update(s.encode('utf-8'))
		return md5.hexdigest()

	# 登录
	def login(self):
		username = input('请输入用户名:')
		password = input('请输入密码:')
		# 输入错误则重新输入
		data = {'Username': (self.getmd5(username), u'Unicode'), 'Password': (self.getmd5(password), u'Unicode')}
		_file = open('info/user.pkl', 'rb')
		try:
			_temp = pickle.load(_file)
		finally:
			_file.close()
		# 验证用户信息
		if data == _temp:
			print('登录成功！')
			return True
		else:
			print('错误！')
			return False

	def get_username(self):
		return self.username

	def get_password(self):
		return self.password

	def main_reg(self):
		print('开始注册')
		self.register()

	def main(self):
		print('开始登录')
		b = self.login()
		while not b:
			b = self.login()


# 初始化模块
class ModuleInit(object):

	def __init__(self):
		pass

	# 静态初始化函数
	@staticmethod
	def load(self):
		pygame.init()
		pygame.mixer.init()
		# 错误处理
		if not pygame.mixer:
			print('Warning, sound disabled!')


# 加载背景
class Background(object):

	def __init__(self):
		pass

	# 静态方法
	@staticmethod
	def load_image(self):
		_screen = pygame.display.set_mode(SCREEN_SIZE)
		# 设置标题
		pygame.display.set_caption('LongPlay')
		background = pygame.image.load_extended(background_image_filename).convert_alpha()
		disk = pygame.image.load_extended(disk_image_filename).convert_alpha()
		stick = pygame.image.load_extended(stick_image_filename).convert_alpha()
		bar = pygame.image.load_extended(bar_image_filename).convert_alpha()
		# 画出背景
		_screen.blit(background, (0, 0))
		_screen.blit(disk, (10, 10))
		_screen.blit(stick, (10, 10))
		_screen.blit(bar, (350, 415))
		# 刷新页面
		pygame.display.update()


# 按钮渲染
class Button(object):

	def __init__(self, image_filename, position):
		self.position = position
		self.image = pygame.image.load_extended(image_filename)

	def render(self, _surface):
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		_surface.blit(self.image, (x, y))

	# 如果point在自身范围内，返回True
	def is_over(self, point):
		point_x, point_y = point
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		in_x = x <= point_x < x + _w
		in_y = y <= point_y < y + _h
		return in_x and in_y


# 喜好功能
class Preference(object):

	def __init__(self, image_filename, position):
		self.position = position
		self.image = pygame.image.load_extended(image_filename)

	def render(self, _surface):
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		_surface.blit(self.image, (x, y))

	def is_over(self, point):
		point_x, point_y = point
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		in_x = x <= point_x < x + _w
		in_y = y <= point_y < y + _h
		return in_x and in_y


# 音乐播放模式
class Mode(object):

	def __init__(self, image_filename, position):
		self.position = position
		self.image = pygame.image.load_extended(image_filename)

	def render(self, _surface):
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		_surface.blit(self.image, (x, y))

	def is_over(self, point):
		point_x, point_y = point
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		in_x = x <= point_x < x + _w
		in_y = y <= point_y < y + _h
		return in_x and in_y


# 选项
class Options(object):

	def __init__(self, image_filename, position):
		self.position = position
		self.image = pygame.image.load_extended(image_filename)

	def render(self, _surface):
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		_surface.blit(self.image, (x, y))

	def is_over(self, point):
		point_x, point_y = point
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		in_x = x <= point_x < x + _w
		in_y = y <= point_y < y + _h
		return in_x and in_y


# 音量设置
class VolumeSet(object):

	def __init__(self, image_filename, position):
		self.position = position
		self.image = pygame.image.load_extended(image_filename)

	def render(self, _surface):
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		_surface.blit(self.image, (x, y))

	def is_over(self, point):
		point_x, point_y = point
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		in_x = x <= point_x < x + _w
		in_y = y <= point_y < y + _h
		return in_x and in_y


# 进度条
class ProgressBar(object):

	def __init__(self):
		self.image = pygame.image.load_extended(circle_image_filename)
		self.initial_position = (348, 413)

	def render(self, _surface):
		_surface.blit(self.image, self.initial_position)

	def is_over(self, point):
		point_x, point_y = point
		x, y = self.initial_position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		in_x = x <= point_x < x + _w
		in_y = y <= point_y < y + _h
		return in_x and in_y


# 编辑
class Edit(object):

	def __init__(self, image_filename, position):
		self.position = position
		self.image = pygame.image.load_extended(image_filename)

	def render(self, _surface):
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		_surface.blit(self.image, (x, y))

	def is_over(self, point):
		point_x, point_y = point
		x, y = self.position
		_w, _h = self.image.get_size()
		x -= _w / 2
		y -= _h / 2
		in_x = x <= point_x < x + _w
		in_y = y <= point_y < y + _h
		return in_x and in_y


# 从source文件夹读取音乐文件
class GetMusic(object):

	def __init__(self):
		pass

	# 静态方法
	@staticmethod
	def path(self, path):
		raw_file_names = os.listdir(path)
		music_files = []
		for file_name in raw_file_names:
			if file_name.lower().endswith('.mp3') or file_name.lower().endswith('.ogg') or file_name.lower().endswith('.wav'):
				music_files.append(os.path.join(MUSIC_PATH, file_name))
		return sorted(music_files)


# 语言选择
L = Language()
lan_number = L.choose(L)
# 错误处理
try:
	if lan_number == '1':
		# 用户选择
		S = Select()
		number = S.choose(S)
		R = Registration()
		# 错误处理
		try:
			if number == '1':
				# 用户注册
				R.main_reg()
			elif number == '2':
				# 用户登录
				R.main()
			elif number == '3':
				pass
		except number != '1' and number != '2' and number != '3':
			print('Input Error')
			sys.exit()
	elif lan_number == '2':
		# 用户选择
		SC = SelectChinese()
		number_c = SC.choose(SC)
		RC = RegistrationChinese()
		# 错误处理
		try:
			if number_c == '1':
				# 用户注册
				RC.main_reg()
			elif number_c == '2':
				# 用户登录
				RC.main()
			elif number_c == '3':
				pass
		except number_c != '1' and number_c != '2' and number_c != '3':
			print('Input Error')
			sys.exit()
except lan_number != '1' and lan_number != '2':
	print('Error')
	sys.exit()


# 初始化
MI = ModuleInit()
MI.load(MI)

# 坐标
x1 = 210
y1 = 480
button_width = 150

# 控制按钮
buttons = {}
pass
buttons['prev'] = Button('image/prev.png', (x1, y1))
buttons['pause'] = Button('image/pause.png', (x1 + button_width * 1, y1))
buttons['stop'] = Button('image/stop.png', (x1 + button_width * 2, y1))
buttons['play'] = Button('image/play.png', (x1 + button_width * 3, y1))
buttons['next'] = Button('image/next.png', (x1 + button_width * 4, y1))

# 喜好按钮
preferences = {}
pass
preferences['dislike'] = Preference('image/full_heart.png', (50, 550))

# 播放模式按钮
modes = {}
pass
modes['loop'] = Mode('image/loop.png', (912, 550))
modes['shuffle'] = Mode('image/shuffle.png', (942, 550))
modes['repeat'] = Mode('image/repeat.png', (970, 550))

# 选项按钮
options = {}
pass
options['option'] = Options('image/option.png', (970, 30))

# 音量按钮
volumes = {}
pass
volumes['up'] = VolumeSet('image/volume_up.png', (942, 600))
volumes['down'] = VolumeSet('image/volume_down.png', (970, 600))

# 编辑按钮
edits = {}
pass
edits['plus'] = Edit('image/plus.png', (30, 30))
edits['minus'] = Edit('image/minus.png', (60, 30))

# 加载音乐
GM = GetMusic()
music_filenames = GM.path(GM, MUSIC_PATH)
if len(music_filenames) == 0:
	print('No music files found in ', MUSIC_PATH)
	sys.exit()

# 设置字体
font = pygame.font.SysFont('Arial', 50, False)
# 错误处理
if not pygame.font:
	print('Warning, font disabled!')
label_surfaces = []

# 文件名显示
for filename in music_filenames:
	txt = os.path.split(filename)[-1]
	print('Track:', txt)
	txt = txt.split('.')[0]
	surface = font.render(txt, True, (255, 255, 255))
	label_surfaces.append(surface)

current_track = 0
max_tracks = len(music_filenames)

# 加载音乐
pygame.mixer.music.load(music_filenames[current_track])

clock = pygame.time.Clock()

# 设置播放状态
playing = False
paused = False

track_end = USEREVENT + 1
pygame.mixer.music.set_endevent(track_end)


# 主程序循环
while True:
	screen = pygame.display.set_mode(SCREEN_SIZE, 0)

	button_pressed = None
	preference_pressed = None
	option_pressed = None
	volume_pressed = None
	mode_pressed = None
	edit_pressed = None

	pressed_keys = pygame.key.get_pressed()

	# 键盘按键控制
	if pressed_keys[K_UP]:
		pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
	if pressed_keys[K_DOWN]:
		pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
	if pressed_keys[K_LEFT]:
		button_pressed = 'next'
	if pressed_keys[K_RIGHT]:
		button_pressed = 'prev'
	if pressed_keys[K_SPACE]:
		if playing:
			pygame.mixer.music.pause()
			playing = False
			paused = True
		elif paused:
			pygame.mixer.music.unpause()
			playing = True
			paused = False
		else:
			pygame.mixer.music.play()
			playing = True
			paused = False

	# 监听事件
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
		if event.type == MOUSEBUTTONDOWN:
			# 判断哪个控制按钮被按下
			for button_name, button in buttons.items():
				if button.is_over(event.pos):
					print(button_name, 'pressed')
					button_pressed = button_name
					break

			# 判断是否按下喜好按钮
			for preference_push, preference in preferences.items():
				if preference.is_over(event.pos):
					print(preference_push, 'Prefer')
					preference_pressed = preference_push
					break

			# 判断是否按下设置按钮
			for option_push, option in options.items():
				if option.is_over(event.pos):
					print(option_push, 'Option')
					option_pressed = option_push
					break

			# 判断是否按下音量按钮
			for volume_push, volume in volumes.items():
				if volume.is_over(event.pos):
					print(volume_push, 'Volume')
					volume_pressed = volume_push
					break

			# 判断是否切换播放模式
			for mode_push, mode in modes.items():
				if mode.is_over(event.pos):
					print(mode_push, 'Mode')
					mode_pressed = mode_push
					break

			# 判断是否按下编辑按钮
			for edit_push, edit in edits.items():
				if edit.is_over(event.pos):
					print(edit_push, 'Edit')
					edit_pressed = edit_push
					break

		# 如果一曲播放结束，就“模拟”按下"next"
		if event.type == track_end:
			button_pressed = 'next'

		if edit_pressed is not None:
			if edit_pressed == 'plus':
				place = input('Please input the address of the file:')
				shutil.copy(place, 'source')
			elif edit_pressed == 'minus':
				pygame.mixer.music.stop()
				os.remove(music_filenames[current_track])

		if volume_pressed is not None:
			if volume_pressed == 'up':
				pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
			elif volume_pressed == 'down':
				pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)

		if option_pressed is not None:
			file = open('info/user.pkl', 'rb')
			try:
				temp = pickle.load(file)
				pprint.pprint(temp)
			finally:
				file.close()

		if mode_pressed is not None:
			if mode_pressed == 'loop':
				current_pos = pygame.mixer.music.get_pos()
				pygame.mixer.music.play(0, current_pos)
			if mode_pressed == 'shuffle':
				current_pos = pygame.mixer.music.get_pos()
				pygame.mixer.music.play(0, current_pos)
			if mode_pressed == 'repeat':
				current_pos = pygame.mixer.music.get_pos()
				pygame.mixer.music.play(99, current_pos)

		if preference_pressed is not None:
			if preference_pressed == 'dislike':
				preferences['like'] = Preference('image/full_heart.png', (50, 550))
				preferences['like'].render(screen)
			if preference_pressed == 'like':
				# 加载背景
				_BG = Background()
				_BG.load_image(_BG)

				# 写当前歌名
				_label = label_surfaces[current_track]
				w1, h1 = _label.get_size()
				screen_w1 = SCREEN_SIZE[0]
				screen.blit(_label, ((screen_w1 - w1) / 2 + 10, 520))

				# 画控制按钮
				for button in buttons.values():
					button.render(screen)
				# 画喜好按钮
				for preference in preferences.values():
					preferences['dislike'].render(screen)
				# 画播放模式按钮
				for mode in modes.values():
					mode.render(screen)
				# 画选项按钮
				for option in options.values():
					option.render(screen)
				# 画音量按钮
				for volume in volumes.values():
					volume.render(screen)

				# 帧率设置
				clock.tick(50)

				# 页面刷新
				pygame.display.update()

		if button_pressed is not None:
			if button_pressed == 'next':
				current_track = (current_track + 1) % max_tracks
				pygame.mixer.music.load(music_filenames[current_track])
				if playing:
					pygame.mixer.music.play()

			elif button_pressed == 'prev':
				# 按下prev的逻辑：
				# 如果已经播放音乐超过了3秒，就从头开始，否则就播放上一首
				if pygame.mixer.music.get_pos() > 3000:
					pygame.mixer.music.stop()
					pygame.mixer.music.play()
				else:
					current_track = (current_track - 1) % max_tracks
					pygame.mixer.music.load(music_filenames[current_track])
					if playing:
						pygame.mixer.music.play()

			elif button_pressed == 'pause':
				if paused:
					pygame.mixer.music.unpause()
					paused = False
				else:
					pygame.mixer.music.pause()
					paused = True

			elif button_pressed == 'stop':
				# 淡出效果
				pygame.mixer.music.fadeout(2500)
				playing = False

			elif button_pressed == 'play':
				if paused:
					pygame.mixer.music.unpause()
					paused = False
				else:
					if not playing:
						pygame.mixer.music.play()
						playing = True

	# 加载背景
	BG = Background()
	BG.load_image(BG)

	# 写当前歌名
	label = label_surfaces[current_track]
	w, h = label.get_size()
	screen_w = SCREEN_SIZE[0]
	screen.blit(label, ((screen_w - w) / 2 + 10, 520))

	# 画控制按钮
	for button in buttons.values():
		button.render(screen)
	# 画喜好按钮
	for preference in preferences.values():
		preferences['dislike'].render(screen)
	# 画播放模式按钮
	for mode in modes.values():
		mode.render(screen)
	# 画选项按钮
	for option in options.values():
		option.render(screen)
	# 画音量按钮
	for volume in volumes.values():
		volume.render(screen)
	# 画编辑按钮
	for edit in edits.values():
		edit.render(screen)

	# 画进度条
	PB = ProgressBar()
	PB.render(screen)

	# 帧率设置
	clock.tick(50)

	# 页面刷新
	pygame.display.update()
