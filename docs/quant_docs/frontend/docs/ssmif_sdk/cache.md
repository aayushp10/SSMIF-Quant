---
id: cache-overview
title: Cache Overview
sidebar_label: Cache Overview
slug: /cache-overview
---

## What is a cache?

A cache is a hardware or software component that stores data so that it can be
retrieved quickly for later use. Ideally, one would save the result of a 
computationally expensive function in the cache so that they can retrieve the 
output instead of computing it again. The SDK uses redis as a cache.

## What is redis?

On the surface, you can think of redis as a Python dictionary. You assign a
unique key, such as a string, to some data. That key can then be used to access
the data later on. For more information, click [here](https://redis.io/).

## How do I use it?

We have developed a class, CacheData, that interacts with the redis cache and
handles the tricky parts of using redis, such as generating a unique key.

First, you must include the following line of code in your file:

```python
from ssmif_sdk.utils.cache import CacheFunctionType, CacheData
```

Second, check to see that CacheFunctionType includes the name of the function
that you want to add caching to. If it does not, feel free to add it. You don't
have to copy paste the name of the function. You probably shouldn't if the name
is really long. Pick something simple. Make sure other users will be able to 
identify which function the name refers to, though.

```python
class CacheFunctionType(BaseEnum):
    get_nav = auto()
```

After that, there is just a few lines of code that you have to add to your
function. At the top, add the following lines:

```python
redis_element = CacheData(CacheFunctionType.get_nav, [args])
if redis_element.is_cached:
    return redis_element.data
```

Make sure the list contains the same number of arguments as the function
itself.

Lastly, before the return statement(s), add this line as well:

```python
redis_element.store(your_function_result)
```

That's all there is to do!

## Design Choices (not finished)

This section will explain our design choices for CacheData. Read this before
making any changes to cache.py.

### CacheData

The main purpose of CacheData is to abstract away the creation of the key.
We have to ensure that given a function and set of arguments produces the same
key is generated so that the data within the cache is accessible. We also want 
the key to be unique so that we do not overwrite other data. The 
CacheFunctionType and arguments list that are passed into the constructor are
used to create the key.

The key is JSON of the name of the function from CacheFunctionType and a list of
the SHA1 hash codes of the arguments.

We do not use Python's builtin hash function since it gave us different hash
values for the same parameters.
