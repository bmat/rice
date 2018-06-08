[![Build Status](https://travis-ci.org/bmat/rice.svg?branch=master)](https://travis-ci.org/bmat/rice)


# Why rice?

Rice use your class documentation to inference the schema, so you just need a simple class (no metaclases,
no inheritance...). So the advantages are 2:
* No dependencies (so you don't have to force other people to your your favourite serialization library)
* Your code is documented

# Basic example
Imagine that you have a blog post with comments and your model looks like this:
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

Now you want to serialize, deserialize it easily. Buy using rice, just document your classes

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
        username (str, serializable): The comment author
        body (str, serializable): The comment body
    """
    def __init__(self, username, body):
        self.username = username
        self.body = body
```

Just define your attributes documentation like you do for Sphinx but adding the "serializable" flag to make it
serializable. Of course you can inherit classes and work with any type of class (for example your ORM model can
inherit from this classes)

```python
comment_list = [
    Comment("yolo69", "Ey wazzup!"),
    Comment("peter", "Nice post!!")
]
post = Post("Pepe", comment_list)

print(serialize(post))
# {"author": "Pepe", "comments": [{"username": "yolo69", "body": "Ey wazzup!"}, {"username": "peter", "body": "Nice post!!"}]}

```

or if you want xml, first install dicttoxml
```bash
pip install dicttoxml
```

```python
comment_list = [
    Comment("yolo69", "Ey wazzup!"),
    Comment("peter", "Nice post!!")
]
post = Post("Pepe", comment_list)

print(serialize(post, format="xml"))
#b'<?xml version="1.0" encoding="UTF-8" ?><data><comments type="list"><item type="dict"><body type="str">Ey wazzup!</body><username type="str">yolo69</username></item><item type="dict"><body type="str">Nice post!!</body><username type="str">peter</username></item></comments><author type="str">Pepe</author></data>'

```

You can add as many handlers as you want. Just provide a method to convert your format to a dict and viceversa

And for deserializing you have to provide the source raw input (ej json string) and the object class (in this case, Post)
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
        comments ([Comment], serializable): All comments of the post
    """
    def __init__(self, author, comments):
        self.author = author
        self.comments = comments


class Comment(object):
    """User comment

    Attributes:
        username (str, serializable): The comment author
        body (str, serializable): The comment body
    """
    def __init__(self, username, body):
        self.username = username
        self.body = body


comment_list = [
    Comment("yolo69", "Ey wazzup!"),
    Comment("peter", "Nice post!!")
]
post = Post("Pepe", comment_list)

d = serialize(post)

deserialized = deserialize(d, Post)

print(deserialized.comments[0].body)
```


#TODOS
* Scope: Add scopes fields to control which fields are serialized (at this moment you can serialize all or nothing)
* Add more doc styles: At this moment only the google style is supported
* Support for other data structures (at this moment only list and enum are supported)


# Testing
Just type
```python
python rice/test/test.py
```