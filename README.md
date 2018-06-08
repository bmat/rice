[![Build Status](https://travis-ci.org/bmat/rice.svg?branch=master)](https://travis-ci.org/bmat/rice)

TLDR: By adding the **`serializable`** keyword *after* the attribute type into your `Docstrings` it will be *automagically* **serializable**. 


### Install

Install with [pip](https://pypi.org/project/pip/):

```bash
$ pip install rice
```
### What is *rice* and why use it?
**Rice** is not a new serialization/deserialization library, it use all the inherent beauty and nature of python.

**Rice** use your class documentation to infer the schema, that's it. You just need a `class`, no `metaclass`, no inheritance... 

The advantages are *double*:
* No dependencies - *you don't have to force others to use your favorite serialization library*
* Your code is documented - *everybody loves documentation*

### What do you need?
- Python version > 3.4
- Python Docstrings: [Sphinx - Google Style](http://www.sphinx-doc.org/en/master/ext/example_google.html)


### Basic example
Imagine that you have a blog `Post` with `Comments` and your model looks like this:
```python
class Post(object):
    def __init__(self, author, comments):
        self.author=author
        self.comments=comments
        
class Comment(object):
    def __init__(self, username, body):
        self.username=username
        self.body=body
```
Now you want to serialize and deserialize it easily. Buy using **rice**, just document your classes, and you are all set:
```python
class Post(object):
    """My pretty Post class
    
    Attributes:
        author (str, serializable): The author of the post
        comments ([Comment], serializable): A list of comments
    """
    def __init__(self, author, comments):
        self.author = author
        self.comments = comments


class Comment(object):
    """User comment
    
    Attributes:
        username (str, serializable): The comment author's username
        body (str, serializable): The comment body content
        rating (int, serializable): The comment rating value
    """
    def __init__(self, username, body, rating):
        self.username = username
        self.body = body
        self.rating = rating
```

Just define your attributes documentation like you do with [Sphinx](http://www.sphinx-doc.org/). By adding the **`serializable`** keyword *after* the attribute type into your `Docstrings` it will be *automagically* **serializable**. 

Of course you can inherit classes and work with any type of class (for example your `ORM` model can
inherit from this classes):

```python
comment_list = [
    Comment("user1", "Serialization made easy, thanks!", 10),
    Comment("jack_black", "Rice is Nice.", 9)
]
post = Post("John Lennon", comment_list)

print(serialize(post))
# {"author": "John Lennon", "comments": [{"username": "user1", "body": "Serialization made easy, thanks!", "rating": 10}, {"username": "jack_black", "body": "Rice is Nice.", "rating": 9}]}
```

or if you want *xml*, first install `dicttoxml`
```bash
$ pip install dicttoxml
```

```python
comment_list = [
    Comment("user1", "Serialization made easy, thanks!", 10),
    Comment("jack_black", "Rice is Nice.", 9)
]
post = Post("John Lennon", comment_list)

print(serialize(post, format="xml"))
#b'<?xml version="1.0" encoding="UTF-8" ?><data><comments type="list"><item type="dict"><body type="str">Serialization made easy, thanks!</body><rating type="int">10</rating><username type="str">user1</username></item><item type="dict"><body type="str">Rice is Nice.</body><rating type="int">9</rating><username type="str">jack_black</username></item></comments><author type="str">John Lennon</author></data>'
```

You can add as many handlers as you want. Just provide a method to convert your format to a `dict` and vice-versa

To deserialize you have to provide the source raw input (*Eg* `json` string) and the object `class` (in this case, `Post`)
```python
deserialized = deserialize(d, Post)
```


Get the full working example here
```python
from rice import serialize, deserialize

class Post(object):
    """My pretty Post class
    
    Attributes:
        author (str, serializable): The author of the post
        comments ([Comment], serializable): A list of comments
    """
    def __init__(self, author, comments):
        self.author = author
        self.comments = comments


class Comment(object):
    """User comment
    
    Attributes:
        username (str, serializable): The comment author's username
        body (str, serializable): The comment body content
        rating (int, serializable): The comment rating value
    """
    def __init__(self, username, body, rating):
        self.username = username
        self.body = body
        self.rating = rating


comment_list = [
    Comment("user1", "Serialization made easy, thanks!", 10),
    Comment("jack_black", "Rice is Nice.", 9)
]
post = Post("John Lennon", comment_list)

d = serialize(post)

deserialized = deserialize(d, Post)
a_comment_object = deserialized.comments[0]
print(a_comment_object.body)
```


### TODO
* Scope: Add scopes fields to control which fields are serialized (at this moment you can serialize all or nothing)
* Add more doc styles: At this moment only the Google style is supported
* Support for other data structures (at this moment only list and Enum are supported)


### Testing
To test **rice** type:
```bash
python rice/test/test.py
```