list(set(a))
map(fn,x)
reduce(fn,x)
filter(fn,x)
r 只读 w 写 会覆盖  a追加 b 二进制 +可读写模式 x 如果存在报异常 
fs.close
with open(filename,a) as fn:
	fn.write()
fn.close()
try:
	pass
except Exception as e:
	raise
else:
	pass
finally:
	pass

issubclass  一个类是不是第二个的子类
(1). __init__：用于初始化对象
(2). __new__：用于创建对象
(3).__call_：使对象变得可调用
(4). __dict__：把类中的属性组成一个字典，属性名作为key， 属性值作为value
(5).__class__：用于查看对象是由哪个类创建的
(1).x：公有变量；
(2)._x：单个前置下划线，私有化方法或属性，from some_module import *是不能导入的,只有类和对象可以访问;
(3).__x：双前置下划线，避免与子类中的属性命名冲突，外部无法访问，但是可以通过特殊的方式(obj._类名__xx)访问到
(4).__x__：双前后下划线，用户名字空间的魔法方法后属性。最好不要用这种命名方式！
(5).x_：单后置下划线，用于避免与Python关键词冲突！不要使用哦！
super()类似于protype __mro__