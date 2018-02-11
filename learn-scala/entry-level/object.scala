/**
  * object 相当于 class 的单个实例,通常在一些静态的 field 或者 method
  * 第一次调用 object 的方法时, 就会执行 object 的 constructor , 也就是 object 内部不在 method 中的代码
  * object 不能定义接受参数的 constructor
  * object 的 constructor 只会在其第一次被调用的时候执行一次,以后再次调用就不会再次执行了
  * object 通常用于单例模式的实现,或者放 class 的静态成员, 比如工具方法
  */

/**
  * 伴生对象
  * 如果有一个class，还有一个与class同名的object，那么就称这个object是class的伴生对象，class是object的伴生类
  * 伴生类和伴生对象必须存放在一个.scala文件之中
  * 伴生类和伴生对象，最大的特点就在于，互相可以访问private field
  */

/**
  * apply 方法
  * object中非常重要的一个特殊方法，就是apply方法
  * 通常在伴生对象中实现apply方法，并在其中实现构造伴生类的对象的功能
  * 而创建伴生类的对象时，通常不会使用new Class的方式，而是使用Class()的方式，隐式地调用伴生对象得apply方法，这样会让对象创建更加简洁
  * 比如，Array类的伴生对象的apply方法就实现了接收可变数量的参数，并创建一个Array对象的功能
  */