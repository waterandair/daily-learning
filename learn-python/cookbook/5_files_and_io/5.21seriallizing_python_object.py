#!/usr/bin/python3
# *_* coding utf-8 *_*
import pickle
"""
You need to serialize a python object into a byte stream so that you can do things such as
save it in to a file,store it in a database, or transmit it over a network connection
The most common approach for serializing data is to use the pickle module.
"""
class Stu:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        print ("this is {}, {} years old".format(self.name, self.age))


# To dump an object to a file :
f = open('./file/5.21_test1.txt', 'wb')
pickle.dump(Stu, f)

# To dump an object to a string to a string , use pickle.dumps():
s = pickle.dumps(Stu)
print(s)  # b'\x80\x03c__main__\nStu\nq\x00.'

"""
To re-create an object from a byte stream, use either the pickle.load() or pickle.loads() functions
"""

# restore from a file
f = open('./file/5.21_test1.txt', 'rb')
Stu1 = pickle.load(f)
stu1 = Stu1('kobe', 81)
stu1.get_info()  # this is kobe, 81 years old

Stu2 = pickle.loads(s)
stu2 = Stu2('wade', 67)
stu2.get_info()  # this is wade, 67 years old


"""
For example, if working with multiple objects, you can do this:
"""
f = open('./file/5.21_test2.txt', 'wb')
pickle.dump([1, 2, 3, 4], f)
pickle.dump('hello', f)
pickle.dump({'Apple', 'Pear', 'Banana'}, f)
f.close()

f = open('./file/5.21_test2.txt', 'rb')
print (pickle.load(f))  # [1, 2, 3, 4]
print (pickle.load(f))  # hello
print (pickle.load(f))  # {'Pear', 'Apple', 'Banana'}