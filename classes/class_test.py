#ENCAPSULATION
class Base:
	def __init__(self):
		self.a = "test" #Public
		self._b = "test2" #Protected
		self.__c = "test3" #Private

class Derived(Base):
	def __init__(self):
		Base.__init__(self)
		print("Calling Base")
		print(self._b)

test1 = Base()
print(test1.a)

test2 = Derived()
print(test2.a)		
self._a = "test2"
