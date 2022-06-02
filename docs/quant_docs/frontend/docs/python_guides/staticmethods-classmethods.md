---
id: staticmethods-classmethods
title: Staticmethods and Classmethods
sidebar_label: Staticmethods and Classmethods
slug: /staticmethods-classmethods
---

### Original [source](https://stackabuse.com/pythons-classmethod-and-staticmethod-explained/)
- We are preserving the content here for the benefit of future analysts

### The @classmethod Decorator
- This decorator exists so you can create class methods that are passed the actual class object within the function call, much like <code>self</code> is passed to any other ordinary instance method in a class.

- In those instance methods, the <code>self</code> argument is the class instance object itself, which can then be used to act on instance data. <code>@classmethod</code> methods also have a mandatory first argument, but this argument isn't a class instance, it's actually the uninstantiated class itself. So, while a typical class method might look like this:

```python 
class Student(object):

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

scott = Student('Scott',  'Robinson')
```
- A similar <code>@classmethod</code> method would be used like this instead:

```python
class Student(object):

    @classmethod
    def from_string(cls, name_str):
        first_name, last_name = map(str, name_str.split(' '))
        student = cls(first_name, last_name)
        return student

scott = Student.from_string('Scott Robinson')
```

- This follows the [static factory pattern](https://stackoverflow.com/questions/929021/what-are-static-factory-methods/929273#929273) very well, encapsulating the parsing logic inside of the method itself.

- The above example is a very simple one, but you can imagine more complicated examples that make this more attractive. Imagine if a <code>Student</code> object could be serialized in to many different formats. You could use this same strategy to parse them all:

```python
class Student(object):

    @classmethod
    def from_string(cls, name_str):
        first_name, last_name = map(str, name_str.split(' '))
        student = cls(first_name, last_name)
        return student

    @classmethod
    def from_json(cls, json_obj):
        # parse json...
        return student

    @classmethod
    def from_pickle(cls, pickle_file):
        # load pickle file...
        return student
```

- The decorator becomes even more useful when you realize its usefulness in sub-classes. Since the class object is given to you within the method, you can still use the same <code>@classmethod</code> for sub-classes as well.

### The @staticmethod Decorator

- The <code>@staticmethod</code> decorator is similar to <code>@classmethod</code> in that it can be called from an uninstantiated class object, although in this case there is no <code>cls</code> parameter passed to its method. So an example might look like this:

```python
class Student(object):

    @staticmethod
    def is_full_name(name_str):
        names = name_str.split(' ')
        return len(names) > 1

Student.is_full_name('Scott Robinson')   # True
Student.is_full_name('Scott')            # False
```

- Since no <code>self</code> object is passed either, that means we also don't have access to any instance data, and thus this method can not be called on an instantiated object either.

- These types of methods aren't typically meant to create/instantiate objects, but they may contain some type of logic pertaining to the class itself, like a helper or utility method.

### @classmethod vs @staticmethod
- The most obvious thing between these decorators is their ability to create static methods within a class. These types of methods can be called on uninstantiated class objects, much like classes using the <code>static</code> keyword in Java.

- There is really only one difference between these two method decorators, but it's a major one. You probably noticed in the sections above that <code>@classmethod</code> methods have a cls parameter sent to their methods, while <code>@staticmethod</code> methods do not.

- This <code>cls</code> parameter is the class object we talked about, which allows <code>@classmethod</code> methods to easily instantiate the class, regardless of any inheritance going on. The lack of this <code>cls</code> parameter in <code>@staticmethod</code> methods make them true static methods in the traditional sense. They're main purpose is to contain logic pertaining to the class, but that logic should not have any need for specific class instance data.

### A Longer Example

- Now let's see another example where we use both types together in the same class:
```python
# static.py

class ClassGrades:

    def __init__(self, grades):
        self.grades = grades

    @classmethod
    def from_csv(cls, grade_csv_str):
        grades = map(int, grade_csv_str.split(', '))
        cls.validate(grades)
        return cls(grades)


    @staticmethod
    def validate(grades):
        for g in grades:
            if g < 0 or g > 100:
                raise Exception()

try:
    # Try out some valid grades
    class_grades_valid = ClassGrades.from_csv('90, 80, 85, 94, 70')
    print 'Got grades:', class_grades_valid.grades

    # Should fail with invalid grades
    class_grades_invalid = ClassGrades.from_csv('92, -15, 99, 101, 77, 65, 100')
    print class_grades_invalid.grades
except:
    print 'Invalid!'
```

```bash
$ python static.py
Got grades: [90, 80, 85, 94, 70]
Invalid!
```
- Notice how the static methods can even work together with <code>from_csv</code> calling <code>validate</code> using the <code>cls</code> object. Running the code above should print out an array of valid grades, and then fail on the second attempt, thus printing out "Invalid!".

### Conclusion
- You've now seen how both the <code>@classmethod</code> and <code>@staticmethod</code> decorators work in Python, some examples of each in action, and how they differ from each other. Hopefully now you can apply them to your own projects and use them to continue to improve the quality and organization of your own code.