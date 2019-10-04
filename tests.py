def succ:
    print 'give me the succ'

## Python with Kylo

# Whitespace matters
# Implicit variable declaration
# Every function is not necesarrily part of a class
# Dont need a main()
# You can end lines w/ semicolons but try to avoid it
# Interpreted language
# procedural: calling add_numbers before the definition will crash

def add_numbers(summand1, summand2):
    assert (type(summand1)==int or type(summand1)==float and type(summand2)==int or type(summand2)==float) #throws exception if var is not of set type
    sum = summand1 + summand2
    return sum

dictionary = {'a':645, 'b':123, 'c':73}
print dictionary['a']

my_set = {5, 6, False}
print 5 in my_set  #prints true

my_list = [1,5, 'cat', 6.5] #no arrays, only lists
my_list.append('bacon')

# Adding paranthesis makes something a function (verb)
# not adding makes something a noun

# == means equivelant (.equals())
# is checks for aliases (if they are the exact same object, memory address)
# // means do integer division. 6//5 = 1

# casting: print(float(1)) results in 1.0. Casting is essentially a function of the type

def multiply_nums(m1,m2 = 1): #m2 is automatically 1
    """
    this is a formal documentation comment like a javadoc comment
    you can only have one of these per function
    """
    product = m1*m2
    return product

print multiply_nums(5)  # returns 5
print multiply_nums.__doc__ # returns the doc comment

# There is no public or private stuff
# However, to consider something private, start the function name with _.
# def _private_method:

# """ String """: defining a string like this lets you enter a new line and will print it out as you space it.

# tuples: like a list but immutable, hard set, cannot change, useful for keys
my_tuple = (1,2,3)
print my_tuple[1] # returns 2

map = {(1,1):'Tacoma', (1,-1):'Olympia'}
print map[(1,1)] # returns Tacoma

def do_thing():
    # global x    global will make the following variable global, use in a function to read it
    x = 2
    print(x)
x = 20
print(x)    # 20
do_thing(x) # 2
print(x)    # 20  when using global, will print 2


#Objects
class Vector(object): # (object): whatever is in () is what you inherit from
     def __init__(self, x=0, y=0, z=0):   # every nonstatic method needs to have self in ()
        #pass: basically means there's nothing after a colon. Use in if/else, loops,...
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "<"+ str(self.x) + ", " + str.(self.y) + ", " + str(self.z) + ">"  # need to contat ints to string

    def __add__(self, other): # This will overload the '+' operator, will only work with Vector variables
        assert type(other) == Vector
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

    def __eq__(self, other):
        assert type(other) == Vector
        return self.x ==other.x and self.y == other.y and self.z = other.z

    @staticmethod
    def make_zero_vector():
        return Vector(0,0,0)



v = Vector(10,20,30)
w = Vector(7, 2, 5)
print(v) # prints <10, 20, 30>

vec = v + w
print(vec) # prints <17, 22, 35>

if v == v: # Prints just what it says below
    print 'Dude you just overloaded the == operator'

z = Vector.make_zero_vector()
print(z) # returns <0,0,0>

from math import sqrt as rooty # imports the sqrt function and calls it rooty
from math import * # use this to make them global functions so you don't need to do math.sqrt for instance
