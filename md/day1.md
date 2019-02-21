##1.类的标识符
     以单下划线开头的_foo代表不能直接访问类属性，需要通过类提供的接口进行访问，不能用from xxx import * 导入；
     以双下划线开头的__foo 代表类的私有成员；
     以双下划线开头和结尾的__foo__代表Python里特殊方法专用的标识，如__ini__()代表类的构造函数
     
##2.多行语句
     一般以新行作为语句的结束符，但可以通过（\）将一行语句分为多行显示
     
##3引号
     三个单引号或者双引号包围的是注释
     
##4.print输出
     print默认输出是换行的,如果实现不换行需要在变量末尾上加上end=""
     
##5.import 和 from...improt
    将整个模块(somemodule)导入，格式为： import somemodule
    从某个模块中导入某个函数,格式为： from somemodule import somefunction
    从某个模块中导入多个函数,格式为： from somemodule import firstfunc, secondfunc, thirdfunc
    将某个模块中的全部函数导入，格式为： from somemodule import *
    
##6.数据类型
     Number(数字)，String(字符串)，List(列表)，Tuple(元组)，Sets(集合)，Dictionary(字典)
     (1)Number(数字)
            int,float,bool,complex(复数)
            可以通过type()来查看数据类型，也可以通过isinstance()来判断是否为某种类型
            可以同时为多个变量赋值：a,b = 1,2

     (2)String(字符串)
            截取字符串：变量[头下标:尾下标]
            索引值以 0 为开始值，-1 为从末尾的开始位置
            加号 (+) 是字符串的连接符， 星号 (*) 表示复制当前字符串，紧跟的数字为复制的次数
            使用反斜杠(\)转义特殊字符，如果你不想让反斜杠发生转义，可以在字符串前面添加一个 r
     (3)List(列表)
            截取列表：变量[头下标:尾下标]
            加号 (+) 是列表的连接符， 星号 (*) 表示复制当前值，紧跟的数字为复制的次数
     (4)Tuple(元组)
           元组（tuple）与列表类似，不同之处在于元组的元素不能修改。元组写在小括号(())里，元素之间用逗号隔开
           可以把字符串看作一种特殊的元组
           string、list和tuple都属于sequence（序列）
     (5)Sets(集合)
            集合（set）是一个无序不重复元素的序列
            可以使用大括号 { } 或者 set() 函数创建集合，注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典
     (6)Dictionary(字典)
            列表是有序的对象结合，字典是无序的对象集合。两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取
            字典是一种映射类型，字典用"{ }"标识，它是一个无序的键(key) : 值(value)对集合
            键(key)必须使用不可变类型，在同一个字典中，键(key)必须是唯一的
            构造函数 dict() 可以直接从键值对序列中构建字典
            
##7.数据类型转换
    |     类型                       |    说明                                                  |
    | :--------                      |    :--:                                                  |
    |     int(x [,base])             |    将x转换为一个整数                                     |
    |     float(x)                   |    将x转换到一个浮点数                                   |
    |     complex(real [,imag])      |    创建一个复数                                          |
    |     str(x)                     |    将对象 x 转换为字符串                                 |
    |     repr(x)                    |    将对象 x 转换为表达式字符串                           |
    |     eval(str)                  |    用来计算在字符串中的有效Python表达式,并返回一个对象   |
    |     eval(str)                  |    用来计算在字符串中的有效Python表达式,并返回一个对象   |
    |     tuple(s)                   |    将序列 s 转换为一个元组                               |
    |     list(s)                    |    将序列 s 转换为一个列表                               |
    |     set(s)                     |    转换为可变集合                                        |
    |     dict(d)                    |    创建一个字典。d 必须是一个序列 (key,value)元组。      |
    |     frozenset(s)               |    转换为不可变集合                                      |
    |     unichr(x)                  |    将一个整数转换为Unicode字符                           |
    |     ord(x)                     |    将一个字符转换为它的整数值                            |
    |     hex(x)                     |    将一个整数转换为一个十六进制字符串                    |
    |     oct(x)                     |    将一个整数转换为一个八进制字符串                      |

##8.运算符
    算术运算符 比较运算符 赋值运算符 位运算符 逻辑运算符 成员运算符 身份运算符
    