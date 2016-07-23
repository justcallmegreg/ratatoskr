# ratatoskr

### Getting started...

#### Register LocalOperation

```python

@register_operation
def foo(a):
    print a


@register_operation
def bar(a):
    return a


def handler(event, context):
    dispatch_operation(event)

```

##### Example `event`

```json

{
  "operation": "foo",
  "args" : {
    "a": 42
  }
}

```

#### Renaming operation

```python

@register_operation(LocalOperation('dummy_operation'))
def foo(a):
    print a


@register_operation
def bar(a):
    return a


def handler(event, context):
    dispatch_operation(event)

```

##### Example `event`

```json

{
  "operation": "dummy_operation",
  "args" : {
    "a": 42
  }
}

```

#### Register RemoteOperation (AWSLambdaOperation)

##### DummyLambdaFunction
```python

@register_operation(AWSLambdaOperation(region='eu-central-1', lambda_function='AnotherLambdaFunction'))
def foo(a):
    pass


@register_operation
def bar(a):
    return a


def handler(event, context):
    dispatch_operation(event)

```

##### AnotherLambdaFunction
```python

@register_operation
def foo(a):
    print a


def handler(event, context):
    dispatch_operation(event)

```


##### Example `event`

```json

{
  "operation": "foo",
  "args" : {
    "a": 42
  }
}

```

#### Validating inputs (using voluptuous)

```python

@register_operation
@protectron(voluptuous.Schema(int))
def foo(a):
    print a


def handler(event, context):
    dispatch_operation(event)

```

##### Matching `event`

```json

{
  "operation": "foo",
  "args" : {
    "a": 42
  }
}

```

##### Unmatching `event`

The following payload will result `voluptuous.Invalid` exception.


```json

{
  "operation": "foo",
  "args" : {
    "a": "42"
  }
}

```

#### Write your own validator...

Validator object must:

* have `__call__` method defined
* raise exception on failed validation (preferred schema.SchemaValidationError)
* return the value on success

```python

def is_int(n):
    if not isinstance(n, int):
        raise SchemaValidationError
    return n


@register_operation
@protectron(is_int)
def foo(a):
    print a


def handler(event, context):
    dispatch_operation(event)

```

#### Validating outputs (using voluptuous)

```python

@register_operation
@protectron(input_schema=voluptuous.Schema(int), output_schema=voluptuous.Schema(int))
def bar(a):
    return a


def handler(event, context):
    dispatch_operation(event)

```

