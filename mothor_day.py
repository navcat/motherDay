#!/usr/bin/python
#coding=utf-8

import time, random
import threading
from functools import wraps


# 孕期，你懂的
PREGNANCY = [
	'今天，妈妈的体温38°，比平常高了0.5°',
	'妈妈吐得很厉害，是你捣的鬼吗？',
	'妈妈看到了你的手指，很可爱，不过看上去还有点像鸭蹼',
	'你身高8cm，但是已经有指纹了',
	'医生说看到你在吸吮自己的大拇指，我想知道，那是什么味道',
	'眉毛和眼皮都长出来了,天生就是爱运动',
	'妈妈看到你的大脑在长大，我想，你一定是个聪明的孩子',
	'你偶尔会张开双眼，似乎看到什么，又似乎没有看到',
	'妈妈看到你越来越强壮，很开心',
	'哇喔，你来了，50cm，你很开心，可妈妈很痛',
]

# 你要什么，你懂的
WHAT_I_WANTS = [
	'AD钙奶',
	'哇哈哈',
	'棒棒糖',
	'皮卡丘',
	'学钢琴',
	'自行车',
	'上北大'
]

# 母爱无穷，你懂的
WHAT_MOTHER_CARES = [
	'给你打了点生活费',
	'天冷了，多加衣',
	'天热了，买点衣服吧',
	'都10点了，还不起床',
	'快点，要迟到了',
	'有点出息行不',
	'妈妈想你了...'
]


def coroutine(func):
    ''' 协程装饰器，调用一次next，进入等待 '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return wrapper


class Person(object):
	''' 人 '''
	def __init__(self):
		self.age = 0


class Growing(object):

	def __init__(self, monther, child, condition):
		self.monther = monther
		self.child = child
		self.condition = condition

	def grow_up(self):
		''' 年龄增长，此处，我和母亲的年龄同时增长 '''
		try:
			self.condition.acquire()
			# 随机增长年龄
			age = random.randint(1,3)
			# age = 1
			self.monther.age += age
			self.child.age += age
		finally:
			self.condition.release()

	def time_lapse(self):
		''' 时间流逝 '''
		try:
			time.sleep(random.randint(1, 3))
		except InterruptedError:
			pass


class MotherGrowing(Growing):

	def __init__(self, *args, **kwargs):
		super(MotherGrowing, self).__init__(*args, **kwargs)
		self.monther.age = 22

	def growing(self):
		''' 妈妈在变老 '''
		self.grow_up()
		if self.age > 60:
			print('<<<<<<<<<<<<<<妈妈老了>>>>>>>>>')
		# print('----->妈妈【{0}】岁了'.format(self.age))

	def pregnant(self):
		''' 孕期 '''
		self.age = 22
		print('---那一年，妈妈%d 岁----' % self.age)
		# 成长周期
		for week, desc in enumerate(PREGNANCY):
			print("[第{0}月] {1}".format(week + 1, desc))
			# 这里是漫长的等待
			self.time_lapse()

	@coroutine
	def from_child(self):
		''' 你要什么，妈妈就给你什么 '''
		while True:
			something = (yield)
			self.time_lapse()
			print('[妈{0}岁, 我{1}岁]>>你说要：[{2}]， 妈妈给你 【{2}】'.format(
				self.monther.age, self.child.age, something))

	def to_child(self, cg):
		''' 对孩子的关怀 '''
		care = cg.from_monther()
		max_count = 0
		while max_count < 20:
			index = random.randint(0, len(WHAT_MOTHER_CARES) - 1)
			# 不间断的关怀
			care.send(WHAT_MOTHER_CARES[index])
			max_count += 1
			# 妈妈在变老
			self.growing()

	def say(self):
		print('{0}岁妈妈对{1}岁孩子说，你是好样的！'.format(
			self.monther.age,
			self.child.age))


class ChildGrowing(Growing):

	def __init__(self, *args, **kwargs):
		super(ChildGrowing, self).__init__(*args, **kwargs)

	def growing(self):
		''' 我长大了 '''
		self.grow_up()
		if self.child.age > 18:
			print('<<<<<<<<<<<<<<我长大了>>>>>>>>>')
		# print('-----<我【{0}】岁了'.format(self.age))

	def to_mother(self, mg):
		''' 向妈妈索取 '''
		say = mg.from_child()
		max_count = 0
		while max_count < 20:
			index = random.randint(0, len(WHAT_I_WANTS) - 1)
			# 不间断索取
			say.send(WHAT_I_WANTS[index])
			max_count += 1
			# 我在成长
			self.growing()

	@coroutine
	def from_monther(self):
		''' 来自妈妈的爱 '''
		while True:
			care = (yield)
			self.time_lapse()
			print('[我{0}岁, 妈{1}岁]<<妈妈说：{2}'.format(
				self.child.age,
				self.monther.age,
				care))

	def say(self):
		print('{0}岁的我对{1}岁的妈说：妈，您辛苦了，母亲节快乐！'.format(
			self.child.age,
			self.monther.age
			))


def main():
	monther = Person()
	me = Person()
	condition = threading.Condition()

	g_mother = MotherGrowing(monther, me, condition)
	g_mother.pregnant()

	g_me = ChildGrowing(monther, me, condition)
	# 妈妈线程
	t_mothor = threading.Thread(target=g_mother.to_child, args=(g_me,))
	# 我的线程
	t_me = threading.Thread(target=g_me.to_mother, args=(g_mother, ))

	t_mothor.start()
	t_me.start()

	t_mothor.join()
	t_me.join()

	# 我说
	g_me.say()
	# 妈妈说
	g_mother.say()

if __name__ == '__main__':
	main()