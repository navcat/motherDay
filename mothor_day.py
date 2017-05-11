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
	'快点，要吃迟到了',
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


class Common(object):
	''' 公共类 '''
	def __init__(self):
		self.age = 0

	def time_lapse(self):
		''' 时间流逝 '''
		try:
			time.sleep(random.randint(1, 3))
		except InterruptedError:
			pass

	def growing_old(self):
		''' 妈妈在变老，我在长大 '''
		self.age += random.randint(1, 3)


class Mother(Common):

	def growing(self):
		''' 妈妈在变老 '''
		self.growing_old()
		if self.age > 60:
			print('<<<<<<<<<<<<<<妈妈老了>>>>>>>>>')
		print('----->妈妈【{0}】岁了'.format(self.age))

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
			print('>>你说要：[%s]， 妈妈给你 【%s】' % (something, something))

	def to_child(self, my_child):
		''' 对孩子的关怀 '''
		care = my_child.from_monther()
		max_count = 0
		while max_count < 50:
			index = random.randint(0, len(WHAT_MOTHER_CARES) - 1)
			# 不间断的关怀
			care.send(WHAT_MOTHER_CARES[index])
			max_count += 1
			# 妈妈在变老
			self.growing()

	def say(self):
		print('妈妈对孩子说，你是好样的！')


class Me(Common):

	def growing(self):
		''' 我长大了 '''
		self.growing_old()
		if self.age > 18:
			print('<<<<<<<<<<<<<<我长大了>>>>>>>>>')
		print('-----<我【{0}】岁了'.format(self.age))

	def to_mother(self, my_mothoer):
		''' 向妈妈索取 '''
		say = my_mothoer.from_child()
		max_count = 0
		while max_count < 50:
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
			print('<<妈妈说：{}'.format(care))

	def say(self):
		print('我说：妈，您辛苦了，母情节快乐！')


def main():
	monther = Mother()
	me = Me()
	monther.pregnant()

	# 妈妈线程
	t_mothor = threading.Thread(target=monther.to_child, args=(me,))
	# 我的线程
	t_me = threading.Thread(target=me.to_mother, args=(monther,))

	t_mothor.start()
	t_me.start()

	t_mothor.join()
	t_me.join()

	# 我说
	me.say()
	# 妈妈说
	monther.say()

if __name__ == '__main__':
	main()