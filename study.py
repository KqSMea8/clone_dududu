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

Python和多线程（multi-threading）。这是个好主意码？列举一些让Python代码以并行方式运行的方法。
答案
Python并不支持真正意义上的多线程。Python中提供了多线程包，但是如果你想通过多线程提高代码的速度，使用多线程包并不是个好主意。Python中有一个被称为Global Interpreter Lock（GIL）的东西，它会确保任何时候你的多个线程中，只有一个被执行。线程的执行速度非常之快，会让你误以为线程是并行执行的，但是实际上都是轮流执行。经过GIL这一道关卡处理，会增加执行的开销。这意味着，如果你想提高代码的运行速度，使用threading包并不是一个很好的方法。
不过还是有很多理由促使我们使用threading包的。如果你想同时执行一些任务，而且不考虑效率问题，那么使用这个包是完全没问题的，而且也很方便。但是大部分情况下，并不是这么一回事，你会希望把多线程的部分外包给操作系统完成（通过开启多个进程），或者是某些调用你的Python代码的外部程序（例如Spark或Hadoop），又或者是你的Python代码调用的其他代码（例如，你可以在Python中调用C函数，用于处理开销较大的多线程工作）。
为什么提这个问题
因为GIL就是个混账东西（A-hole）。很多人花费大量的时间，试图寻找自己多线程代码中的瓶颈，直到他们明白GIL的存在。

如果我们不确定要往函数中传入多少个参数，或者我们想往函数中以列表和元组的形式传参数时，那就使要用*args；如果我们不知道要往函数中传入多少个关键词参数，或者想传入字典的值作为关键词参数时，那就要使用**kwargs。
args和kwargs这两个标识符是约定俗成的用法，你当然还可以用*bob和**billy，但是这样就并不太妥。

Python在内存中存储了每个对象的引用计数（reference count）。如果计数值变成0，那么相应的对象就会小时，分配给该对象的内存就会释放出来用作他用。
偶尔也会出现引用循环（reference cycle）。垃圾回收器会定时寻找这个循环，并将其回收。举个例子，假设有两个对象o1和o2，而且符合o1.x == o2和o2.x == o1这两个条件。如果o1和o2没有其他代码引用，那么它们就不应该继续存在。但它们的引用计数都是1。
Python中使用了某些启发式算法（heuristics）来加速垃圾回收。例如，越晚创建的对象更有可能被回收。对象被创建之后，垃圾回收器会分配它们所属的代（generation）。每个对象都会被分配一个代，而被分配更年轻代的对象是优先被处理的。

urllib
urllib2

yield
GIL线程全局锁

1	－2
1	－2
1	2
1	2

广义第二价格GSP（Generalized Second Price）
和传统第二密封竞价类似，出价高者得，需要支付出价第二高着提出的报价再加上一个最小值。

此时：
A的实际出价为4+0.01=4.01
B的实际出价为2+0.01=2.01
C竞价失败

(1) netstat
典型用法：

netstat -apn
说明：可查看系统正在使用的端口信息，以及相关的进程号。

(2) lsof
典型用法：

lsof  filename  # 显示打开指定文件的所有进程
lsof -i :8421  # 显示占用8421端口号的进程


者看到这可能会问，要是这样的话，union与class还有什么区别吗？区别当然还是有的

c++++++++++++++++++++++++++++++++++++++c+++++++++++++++++++++++++++++++++++++++++++c++++++++++++++++++++++++++++++++++++++++c++++++++++++++++++++++++++++++++++++++++++++

1. union不支持继承。也就是说，union既不能有父类，也不能作为别人的父类。
2. union中不能定义虚函数。
3.在没有指定成员的访问权限时,union中默认为public权限
4.union中的成员类型比class少,具体见2.2.1节


tensor object as eval