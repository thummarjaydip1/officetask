print("hello world")
if 5>2:
    print("five greater than two")
if 5>2:
        print("five is greater than two!")
if 5>2:
    print("five is greater than two")
        # print("five is greater than two")

x=5
y="hello world"
print(x)
print(y)

print("hello"); print("how are you"); print("bye bye")

print("python is fun!") #print("Really!") syntax error

print("this will work")
print('this will also work')

# print(this will cause an work)

print("hello world", end="\n\n")
print("hello world", end="     " \
"")
print("i will print on the same line")

# number
print(12345)
print(2*5)
print(2+5)
print("I am", 35, "year old.")

# comment
print("multiple line comment")
'''this is 
a multiple
line comment'''

# varable
x1 = 32
print(type(x1), x1)
y1="jaydip"
print(type(y1), y1)

x2= str(3)
print(type(x2), x2)
y2= int(3)
print(type(y2), y2)
z2= float(3)
print(type(z2), z2)

a=400
A="how are you?"
print(a)
print(A)

# variable name
myvar = "john"
my_var = "john"
_my_var = "john"
myVar = "john"
MYVAR = "john"
myvar2 = "john"

# 2myvar = "john"
# my-var = "john"
# my var = "john"

a, b, c = "apple", "banana", "orange"
print(a)
print(b)
print(c)

fruits = ["cherry", "pineapple", "mango"]
a1, b1, c1 = fruits
print(a1, b1, c1)

x = "python "
y = "is "
z = "awesome"
print(x + y + z)

# x = 5
# y = "John"
# print(x + y) syntax error

x = "awesome"
def myfun():
    print("python is:" +x)
myfun()

x = "awesome"
def myfun():
    x = "fantastic"
    print("python is:" +x)
myfun()
print("python is:" +x)

def myfun():
    global x
    x = "fantastic"
myfun()
print("python is:" +x)

x = "awesome"
def myfun():
    global x
    x = "fantastic"
myfun()
print("python is:" +x)

# datatype
x = "Hello world"
print(type(x), x)
x = 20
print(type(x), x)
x = 20.5
print(type(x), x)
x = 1j
print(type(x), x)
x = ["apple", "banana", "mango"]
print(type(x), x)
x = ("apple", "banana", "mango")
print(type(x), x)
x = range(6)
print(type(x), x)
x = {"name":"john", "age":36}
print(type(x), x)
x = {"apple", "banana", "mango"}
print(type(x), x)
x = frozenset({"apple", "banana", "cherry"})
print(type(x), x)
x = True
print(type(x), x)
x = b"Hello"
print(type(x), x)
x = bytearray(bytes(5))
print(type(x), x)
x = memoryview(bytes(5))
print(type(x), x)
x = None
print(type(x), x)

# python number
x = 1
y = 4467986564
z = -4533312
print(type(x))
print(type(y))
print(type(z))

x = 1.10
y = 1.0
z = -35.59
print(type(x))
print(type(y))
print(type(z))

x = 35e3
y = 12E4
print(type(x))
print(type(y))

x = 3+5j
y = 5j
z = -5j
print(type(x))
print(type(y))
print(type(z))

x = 1 # int
y= 2.8 # float
z = 1j # complex
a = float(x)
b = int(y)
c = complex(x)
print(type(a), a)
print(type(b), b)
print(type(c), c)

# random number
import random
print(random.randrange(1,10))

# python in casting
x=int(1)
print(x)
y=int(2.8)
print(y)
z=int("3")
print(z)

x=float(1)
print(x)
y=float("3")
print(y)

x=str(3)
print(type(x), x)
y=str(2.8)
print(type(y), y)

a = "hello world"
b = """this is 
a multiple 
line paragraph"""
print(a)
print(b)

a="hello world"
print(a[0])

for i in "banana":
    print(i)

a="hello world"
print(len(a))

txt= "the best thing in life are free!"
print("free" in txt)

txt= "the best thing in life are free!"
if "free" in txt:
    print("yes,'free' is present")

txt= "the best thing in life are free!"
print("expensive" not in txt)

txt= "the best thing in life are free!"
if "expensive" not in txt:
    print("No,'expensive' is Not present")

x = "hello word"
print(x[2:5])
print(x[:2])
print(x[3:])
print(x[-5:-2])

a = " Hello World "
print(a.upper())
print(a.lower())
print(a.strip())
print(a.replace("H", "J"))
print(a.split(","))

a="hello"
b="world"
print(a+b)
print(a+" "+b)

# formate string
# age= 35
# txt = "my name is jaydip, i am" +age
# print(txt)

age= 35
txt = f"my name is jaydip, i am year {age} old"
print(txt)

price= 59
txt = f"the price is {price:.2f} dollars"
print(txt)

txt = f"the price is {20 * 59} dollars"
print(txt)

txt = 'It\'s alright.' # quete mukva
print(txt) 

txt = "This will insert one \\ (backslash)." #slash mukva
print(txt) 

txt = "Hello\nWorld" #new line
print(txt) 

txt = "Hello\rWorld" #tab
print(txt) 

txt = "Hello \bWorld" #backspace
print(txt) 

txt = "\110\145\154\154\157" #otcal value
print(txt) 

txt = "\x48\x65\x6c\x6c\x6f" #hex value
print(txt) 

# boolean
x = "hello"
y = 15
print(bool(x))
print(bool(y))

print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool({}))
print(bool([]))

# arithmetic operator
print("arithmetic operator")
print(2+3)
print(3-2)
print(2*4)
print(4/2)
print(5%2)
print(2**5)
print(15//2)

print("assignment operator")
x=5
print(x)
x=5
x+=3
print(x)
x=5
x-=3
print(x)
x=5
x*=3
print(x)
x=5
x/=3
print(x)
x=5
x%=3
print(x)
x=5
x//=3
print(x)
x=5
x**=3
print(x)
x=5
x&=3
print(x)
x=5
x|=3
print(x)
x=5
x^=3
print(x)
x=5
x>>=3
print(x)
x=5
x<<=3
print(x)
print(x:=3)

print('compression operatior')
x=3
y=5
print(x==y)
x=3
y=5
print(x!=y)
x=3
y=5
print(x>y)
x=3
y=5
print(x<y)
x=3
y=5
print(x>=y)
x=3
y=5
print(x<=y)

print("logical operatior")
x=5
print(x>3 and x<10)
x=5
print(x>3 or x<4)
x=5
print(not(x>3 and x<10))

x = ["apple", "banana"]
y = ["apple", "banana"]
z=x
print(x is z)
print(x is y)
print(x == y)

x = ["apple", "banana"]
y = ["apple", "banana"]
z=x
print(x is not z)
print(x is not y)
print(x != y)

print("membership operator")
x = ["apple", "banana"]
print("banana" in x)
x = ["apple", "banana"]
print("banana" not in x)

print("bitwise operator")
print(6 & 3)
print(6 | 3)
print(6 ^ 3)
print(~ 3)
print(3 << 2)
print(8 >> 2)

print("operator precedence")
print(6 + 2 * 3)
