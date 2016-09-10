#ratatoskr

[![Build Status](https://travis-ci.org/ngergo/ratatoskr.svg?branch=master)](https://travis-ci.org/ngergo/ratatoskr)
[![Coverage Status](https://coveralls.io/repos/github/ngergo/ratatoskr/badge.svg?branch=master)](https://coveralls.io/github/ngergo/ratatoskr?branch=master)
[![Code Health](https://landscape.io/github/ngergo/ratatoskr/master/landscape.svg?style=flat)](https://landscape.io/github/ngergo/ratatoskr/master)
[![Stories in Ready](https://badge.waffle.io/ngergo/ratatoskr.svg?label=ready&title=Ready)](http://waffle.io/ngergo/ratatoskr)
[![Requirements Status](https://requires.io/github/ngergo/ratatoskr/requirements.svg?branch=master)](https://requires.io/github/ngergo/ratatoskr/requirements/?branch=master)

__Ratatoskr__ is a library written in Python to make the development of AWS Lambdas easier and more secure. It supports implementing "singleshot" operations that can be reached from an AWS Lambda function and validating the input parameters to avoid unnecessary boilerplate for argument checking. 

## How to use?

### Protect arguments

```python

from ratatoskr import protectron
from ratatoskr.schema import SchemaValidationError


def is_int(n):
    if not isinstance(n, int):
        raise SchemaValidationError
    return n


@protectron(is_int)
def multiple_by_two(num):
    return 2 * num


multiple_by_two(42) ====> 42
multiple_by_two("42") ====> Exception: SchemaValidationError("expected int for data['num']"

```

### Dispatch event

```python

from ratatoskr import register_operation, dispatch_event


@register_operation
def return_me(a):
    return a


@register_operation
def return_24():
    return 24


### AWS Lambda handler
def handler(event, context):
    return dispatch_event(event)


### Example event and handler call

example_event = {
    'operation': 'return_me',
    'args': {
        'a': 42
    }
}

handler(exampe_event, context)  ===> returns 42

another_example_event = {
    'operation': 'return_24',
    'args': {}
}

handler(another_example_event, context)  ===> returns 24
```

## Installation

The package has not been deployed to `pip` yet.
You can install it by:

* cloning the repository and run `pip install -t .`
* __OR__ run `pip install git+https://github.com/ngergo/ratatoskr.git`

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

  - Use ``tox`` command to run all the tests in all locally available python version.
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
