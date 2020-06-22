#!/usr/bin/env python
# coding: utf-8

# # Object-Oriented Programming (III)

# ## Class Interface Techniques
# #### Abstact class
# 일부가 미구현 된 method(**abstract method**)가 존재한다. Class instance를 만들어 사용하려는 목적이 아니라 상속할 틀을 만드는 super class를 말한다.  
# 
# Abstract class는 
# - 구현은 subclass에게 위임한다. 
# - 후손이 동일한 interface를 유지하기 위한 목적.

# In[3]:


class Super:
    """An abstract class
    to be implemented later"""
    def method(self):
        print('in Super.method') # Default behavior
    def delegate(self):
        self.action()            #여기서 action을 취하도록 했는데 지금 현재 action()을 보면 아무것도 정의한게 없으므로 
                                 #그냥 notimplementederror가 뜨게 하도록 했음 그냥.
    def action(self):            # 그래서 이걸 구동해보면 NotImplementedError('action: not implemented')라고 에러발생했다고 창이뜸.
        raise NotImplementedError('action: not implemented')

s = Super()
s.method()
#s.delegate()   # Error 이건 쓰면 안되는거네.
#이 abstract class는 method는 interface를 통일시키라는 guide만 후손들에게 제공했고 후손들에게 구현을 맡김.


# #### 상속자
# 조상으로 부터 모든 attribute과 method를 상속받아 사용한다. 
# - 본인이 이룬게 없다. 모든 것이 조상 덕...

# In[7]:


class Inheritor(Super):   #(SUPER)는 조상클래스로부터 그대로 물려받아온다는 뜻을 가진것.
                           #pass를 써서 class마무리 지어야함.
    pass 

i = Inheritor()
i.method()  # call super method
i.delegate()


# #### 대체자
# 조상으로 부터 상속 받되 일부 method는 대체한다. 
# - 조상의 method를 자손이 완전히 Override.

# In[11]:


#Override한다 = 덮어쓴다. Override하면 조상의 method는 무효화가 됨.
class Replacer(Super):
    def method(self):
        print('in Replace.method')

r = Replacer()
s = Super()
r.method()
s.method()
for obj in (r, s):
    obj.method()


# #### 확장자
# 조상으로 부터 상속받은 method를 활용하되 더 확장하여 발전시킨다.
# - 조상 method를 이용하지만, 확장하여 override

# In[16]:


class Extender(Super):   #여기서는 Super로 class 상속.
    def method(self):
        print('Starting Extender.method')
        #Super.method(self)    #여기서 self를 넣지않으면 정확하게 super class 의 method를 불러올 수 없기 때문에 안됨.
        #근데 보통은 이렇게 하기보다 좀 더 정확하게한다면.
        super().method()   # super()는 할아비 아비등 누가있든 나한테서 가장가까운 조상으로부터 가지고오겠다는 것.
        #누구든 신경안쓰고 가장 가까운 조상중에서 def method()를 가지고 있는 사람으로 부터 가지고오겠다는 것.
        print('ending Extender.method')

e = Extender()
e.method()


# #### 제공자
# 조상(abstact class)이 이루지 못한(구현을 위임한) method를 구현하여 제공한다.
# - implementing `delegate` method by providing `action` method

# In[17]:


class Provider(Super):
    def action(self):
        print('in Provider.action')
#조상class에서 action이 구현이 되어있지 않았으나 action(self)를 여기서 구현해서 조상class를 불러와 거기에 override했다고 보면된다.
        
p = Provider()
p.method()   #p.method()는 단순히 method()를 조상으로 부터 불러와 실행시킨것이니 그대로 결과가 나오고
p.delegate() #p.delegate는 action()를 여기서 구현을 했으므로 불러온 조상class의 내용에다가 action()를 override했다고 보면된다.


# 참고: **Polymorphism (다형성)**
# > 하나의 interface를 통해 서로 다른 여러 타입을 제공하는 것을 의미한다.<br> 
# > 보통 OOP 에서 말하는 다형성은 클래스에 선언된 method가 subclass에서 같은 이름으로 **overriding** 되어 여러 형태로 동작함을 의미한다.

# 주의:  **function overloading in Python**
# > C나 Java에서는 function signature(function name, parameter type과 갯수)가 다르면
# 다른 function이다. 다시 말해, function name을 같이 사용하지만 사실은 언어적으로
# 다른 function (signature)인 것이다. 
# 
# Python에서 다음과 같이 적으면 meth는 마지막 define한 meth만 유효 뿐이다.
# 
# ```Python
# class C:
#     def meth(self, x):
#         ...
#     def meth(self, x, y, z):  # 이것이 유효하다.
#         ...
# 
# c = C()
# c.meth(1)        #  TypeError. 파라미터 y, z가 없다.   
# c.meth(1, 2, 3)  # OK
# ```
# 
# 1) Default argument value로 쓰거나 
# ```Python
#     def meth(self, x, y=0, z=None)
# ```
# 2) 다음과 같이 Variable argument list로 받아야 한다.

# In[ ]:


"""c에서는 parameter이 갯수가 다르고 이름이 같아도 다른function으로 구분하지만
파이썬은 이름으로만 구분하기 때문에 parameter가 다르더라도 같다고 생각해야한다.
그러면 위에 예시에서 마지막에 정의 한 meth만 유효하게 된다.
첫번째 def meth(self,x)는 없는셈친다."""


# In[18]:


#Use variable arguments list, instead.
class C:
    def meth(self, *args):
        print(args)
        for arg in args:
            if isinstance(arg, int):
                print(f'{arg}: handle int')
            elif isinstance(arg, str):
                print(f'{arg}: handle str')
                           
c = C()
c.meth(1, 'a', 'b')


# ### A stream processor

# In[20]:



# Abstract class
class Processor():
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
    
    def process(self):
        for line in self.reader:#self.reader에서부터 read line을 부른것. 그럼 소환된 것이 line으로 들어간것. self.reader.read(line)
            data = self.converter(line) #읽어온 line을 conversion하고
            self.writer.write(data) #writer에다가 write method를 써서 write를 함.
    
       
    def converter(self, data):       # delegates implementation
        raise NotImplemented('converter must be defined') #conversion한것은 매번 다를 수 있으니 여기서의 구현은 자손class에 맡기는것.


# In[21]:


from abc import ABCMeta, abstractmethod

# Abstract class #class도 사실 instance가 될 수 있음 metaclass가 class를 만들어주는 창조주같은 역할.
class Processor(metaclass=ABCMeta):  #abstract method라고 python에 선언해주는것 애가 instance를 만들지 못하게 하는것?
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
    
    def process(self):
        for line in self.reader:
            data = self.converter(line)
            self.writer.write(data)
    
    @abstractmethod #이 데코와 ABCmeta저걸 통해서 def converter를 추상class로 만들었고 후손들은 이 추상class를 반드시 정의하지않음
                    #사용이 아예 불가능 하도록 강제한것. 후손class에서 converter를 꼭 정의해야한다.
    def converter(self, data):       # delegates implementation
        raise NotImplemented('converter must be defined')


# In[26]:


# Provider overriding converter()
class UpperCase(Processor):
    def converter(self, data):
        return data.upper()
    
class ToKorean(Processor):
    korean_dict = {'a': '하나의', 'abacus': '곁눈질', 
                   'abandon': '버리다', 'abandonment': '포기' }
    def converter(self, data):
        return ToKorean.korean_dict.get(data.strip(), "<unknown>") + '\n'
    #여기서 unknown이라는 break를 쓰면 dict안에 원하는 단어가 없으면 exception발동해서 끝나버림.
import sys, io

buf = '\n'.join(['a', 'abacus', 'abandon', 'abandoned']) + '\n'
file = io.StringIO(buf)   # file-like object in memory buffer 
upper = UpperCase(file, sys.stdout) #부모 class의def __init__에서
                                    #file을 reader로지정 후 읽고, sys.stdout이라는 writer로 파일을 써준다고보면된다.
upper.process() #여기서 process불렀고 그럼 조상의 process에서 converter를 부르고 그럼 내가 제공한 converter를 사용하게된다.

file.seek(0)        # rewind the file
korean = ToKorean(file, sys.stdout)
korean.process()


# ### Example: Extending Types by Embedding
# list object을 이용하여 `Set` class 만들기

# In[58]:


class Set:
    #들어온값을 value 라는 list형식으로 만든다. 그후 cooncat을 이용해서 value list안에있는 값들을 manage해서 data list안에 투입.
    def __init__(self, value = []):    # Constructor
        self.data = []                 # Manages a list
        self.concat(value)             #같은 value가 들어오면 append하지 않는것.

    def intersection(self, other):        # other is any sequence
        res = []                       # self is the subject
        for x in self.data:
            if x in other:             # Pick common items
                res.append(x)
        return Set(res)                # Return a new Set

    def union(self, other):            # other is any sequence
        res = self.data[:]             # Copy of my list
        for x in other:                # Add items in other
            if not x in res:
                res.append(x)
        return Set(res)

    def concat(self, value):
        for x in value:                
            if not x in self.data:     # Removes duplicates
                self.data.append(x)

    def __len__(self):          return len(self.data)        # len(self)
    def __getitem__(self, key): return self.data[key]        # self[i], self[i:j]
    def __and__(self, other):   return self.intersection(other) # self & other
    def __or__(self, other):    return self.union(other)     # self | other
    def __repr__(self):         return 'Set({})'.format(repr(self.data))  
    def __iter__(self):         return iter(self.data)       # for x in self:
    
    def issubset(self,other):
        res = other.data[:]
        if len(other) < len(self):
            return ("{} is not subset of {}".format(self, other))
        elif len(other) >= len(self):
            for x in self:
                if not x in res:
                    return ("{} is not subset of {}".format(self,other))
                else:
                    pass
                return("{}is subset of {}".format(self, other))

    def issuperset(self, other):
        res = other.data[:]
        res2 = self.data[:]
        if len(self) >= len(other):
            for x in res:
                if x in res2:
                    pass
                elif not x in res2:
                    res2.append(x)
                    print(res2)
                    return ("{} is not a superset of {}".format(self, other))
        elif len(self) < len(other):
            return("{} is not a superset of {}".format(self, other))
        
    def intersection_update(self, other):
        res = other.data[:]
        res2 = []
        for x in res:
            if x in self:
                res2.append(x)
            elif not x in self:
                pass
        return res2
        
    def difference_update(self, other):
        res = other.data[:]
        res2 = self.data [:]
        for x in res:
            if x in self:
                res2.remove(x)
            elif not x in self:
                pass
        return res2
    def symmetric_difference_update(self, other):
        res = other.data[:]
        res2 = self.data[:]
        for x in res:
            if x in res2:
                res.remove(x)
                res2.remove(x)
            else:
                pass
            
        return res.extend(res2)
    
x = Set([1,3,5,7, 1, 3])
y = Set([2,1,4,5,6])
a = Set([1,2,3,4,5])
b = Set([1,3,5,8,9])
print(x, y, len(x))
print(x.intersection(y), y.union(x))
print(x & y, x | y)
print(x[2], y[:2])
for element in x:
    print(element, end=' ')
print()
print(3 not in y)  # membership test
print(list(x))   # convert to list because x is iterable
print(b.issubset(a))
print(a.issuperset(b))
print(a.intersection_update(b))
print(a.difference_update(b))
print(a.symmetric_difference_update(b))


# ## Exercise. Set class에 methods 추가
# Python `set` type에 쓰이는 다음의 method나 operator를 Set class에 추가하고, `set` 처럼 쓰이는지 시험하라.
# 
# self.issubset(other)
# 
# self <= other
# > Test whether every element in the set is in other.
# 
# self < other
# > Test whether the set is a proper subset of other, that is, set <= other and set != other.
# 
# self.issuperset(other)
# 
# self >= other
# > Test whether every element in other is in the set.
# 
# self > other
# 
# >Test whether the set is a proper superset of other, that is, set >= other and set != other.
# 
# self |= other
# > Update the set, adding elements from all others.
# 
# self.intersection_update(others)
# 
# self &= other
# > Update the set, keeping only elements found in it and all others.
# 
# self.difference_update(others)
# 
# self -= other
# > Update the set, removing elements found in others.
# 
# self.symmetric_difference_update(other)
# 
# self ^= other
# > Update the set, keeping only elements found in either set, but not in both.
# 
# self.add(elem)
# 
# > Add element elem to the set.
# 
# self.remove(elem)
# 
# > Remove element elem from the set. Raises KeyError if elem is not contained in the set.

# In[ ]:




