
class Set:
    def __init__(self, value = []):    # Constructor
        self.data = []                 # Manages a list
        self.concat(value)

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
    
    def add(self, other):
        res = []
        for x in other:
            res.apppend(x)
        return res
    
    
    
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
print(a.add(b))

