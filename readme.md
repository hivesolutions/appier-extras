# [![Appier Framework Extras](res/logo.png)](http://appier_extras.hive.pt)

Set of extra elements for [Appier Framework](http://appier.hive.pt) infra-structure.

Here's a basic example:

```python
import appier
import appier_extras

class HelloApp(appier.WebApp):

    def __init__(self):
        appier.WebApp.__init__(
            self,
            parts = (
                appier_extras.AdminPart,
            )
        )

HelloApp().serve()
```

After running the previous examples, go to [http://localhost:8080/admin](http://localhost:8080/admin)
and login with root/root.

Models that inherit from ``appier_extras.admin.Base`` are automatically added to the admin interface.

## License

Appier Extras is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://travis-ci.org/hivesolutions/appier_extras.svg?branch=master)](https://travis-ci.org/hivesolutions/appier_extras)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/appier_extras/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/appier_extras?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/appier_extras.svg)](https://pypi.python.org/pypi/appier_extras)

## Model Operations

Operations to change the state and behavior of a model's instance can be easily added to the admin interface. The desired function should be defined in the model and decorated with the ``@appier.operation`` decorator, as shown below:

```python
@appier.operation(name = "Generate Key")
def generate_key(self):
    self.key = self._random()
    self.save()
```

This decorator accepts a ``name`` attribute that describes the operation and is shown in the interface, a ``parameters`` tuple containing the parameters to be sent to the operation where each parameter is represented by a ``tuple`` consisting of the descriptor of the parameter, it's name, type and default value. The operation's severity level can by set by specifying the ``level`` <em>keyword</em> where higher levels are more severe: 

```python
@appier.operation(
	name = "Generate Key"
	parameters = (
		("Encoding", "encoding", str, "ascii")
	),
	level = 1
)
def generate_key(self):
    self.key = self._random()
    self.save()
```

To make a class operation instead of one applicable to a specific instance then add the ``@classmethod`` decorator to the function.


