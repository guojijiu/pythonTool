import sys

'''
a = ['zan san','li si','wang er ','ma zi']
for i in range(len(a)):
    print(i,a[i])
'''

'''for letter in 'database':
    if letter == 'b':
        pass
        print('aaa')
    print('vvv')
print('ccc')
'''

'''
list = [1,2,3,4,5,6]
it = iter(list)
for i in it:
    print(i,end="aa")
'''

'''
list = [
    'a1','b1','c1','d1','e1','f1','g1'
]
it = iter(list)
while True:
    try:
        print(next(it))
    except StopIteration:
        sys.exit()
'''


# 斐波拉切数列
def fibonacci(n):
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


f = fibonacci(10)
while True:
    try:
        print(next(f), end="---")
    except StopIteration:
        sys.exit()
