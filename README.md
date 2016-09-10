# ratatoskr

[![Build Status](https://travis-ci.org/ngergo/ratatoskr.svg?branch=master)](https://travis-ci.org/ngergo/ratatoskr)
[![Coverage Status](https://coveralls.io/repos/github/ngergo/ratatoskr/badge.svg?branch=master)](https://coveralls.io/github/ngergo/ratatoskr?branch=master)
[![Code Health](https://landscape.io/github/ngergo/ratatoskr/master/landscape.svg?style=flat)](https://landscape.io/github/ngergo/ratatoskr/master)
[![Stories in Ready](https://badge.waffle.io/ngergo/ratatoskr.svg?label=ready&title=Ready)](http://waffle.io/ngergo/ratatoskr)
[![Requirements Status](https://requires.io/github/ngergo/ratatoskr/requirements.svg?branch=master)](https://requires.io/github/ngergo/ratatoskr/requirements/?branch=master)

__Ratatoskr__ is a library written in Python to make the development of AWS Lambdas easier and more secure. It supports implementing "singleshot" operations that can be reached from an AWS Lambda function and validating the input parameters to avoid unnecessary boilerplate for argument checking. 

## How to use?

### Protect arguments

#### About __@protectron__

* awaits a callable object (`__call__` method)
    * return the `event` on <font color='green'>success</font>
    * raises `SchemaValidationException` on <font color='red'>failure</font>

#### Using your own schema validators

```python
from ratatoskr import protectron, exceptions

def is_int(event):
    for k, v in event.iteritems():
        if not isinstance(v, int):
            raise exceptions.SchemaValidationError
    return event

@protectron(is_int)
def multiply_by_two(num):
    return num * 2

multiply_by_two(42)   # returns 84
multiply_by_two("42") # raises SchemaValudationError
```

#### Using [voluptuous](https://github.com/alecthomas/voluptuous)

```python
from ratatoskr import protectron
from voluptuous import Schema

@protectron(Schema({
    'num': int
}))
def multiply_by_two(num):
    return num * 2


@protectron(Schema({
    'a': int,
    'b': int
}))
def multiply(a, b):
    return a * b


def validate_email(email):
    # ... code to validate email comes here ...


@protectron(Schema({
    'email': validate_email,
}))
def send_email(email):
    # ... code to send email comes here ...


multiply_by_two(42)     # returns 84
multiply_by_two("42")   # raises SchemaValudationError
multiply(2, 21)         # returns 42

send_email("no-reply@example.org") # OK
send_email("example.org") # raises SchemaValudationError
```

### Dispatch event

#### Managing database table

```python
from ratatoskr import dispatch_event, register_operation

@register_operation
def insert(item):
    # ... code to insert to db ...

@register_operation
def remove(item):
    # ... code to remove from db ...

def handler(event, context):
    return dispatch_event(event)
```

Assuming the following `event`, lambda will insert the item to the db.

```python
event = {
    "operation": "insert",
    "args": {
        "item": {
            "username": "batman",
            "password": "s3cR3tPaZzW0rD"
        }
    }
 }
```
## Installation

The package has not been deployed to `pip` yet.
You can install it by:

* cloning the repository/or downloading release tarball and run `pip install .`
* __OR__ run `pip install ratatoskr`

## Tests

__Writing tests is good!__ They protect you from doing things you don't want... It's not different at `ratatoskr`. Tests are written using `pytest` and run via `tox`.
`tox` also checks for style using `flake8` and does code coverage report using `coverage`.

* Run `tox` command in the root directory of the project to run all the tests. 
* You can specify which interpreters should be used by `tox -e [pyX.X]`
* Read more about [__tox__](https://testrun.org/tox/latest/)

PR's for testing new cases is always welcome!

### Contribute

* Fork the repository on GitHub.
* Write a test which shows that the bug was fixed or that the feature works as expected.

  - Use `tox` command to run all the tests in all locally available python version.
* Install `pre-commit` via `pip install pre-commit` then `pre-commit install`.
* Send a pull request and bug the maintainer until it gets merged and published. :).

For more instructions see `TESTING.rst`.

## MIT License

Copyright (c) 2016 Gergő Nagy

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
