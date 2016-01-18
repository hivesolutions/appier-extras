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


## Model Operations

To add an operation accessible from the the admin interface be executed on a model, add this to the model definition:

```python
class Cat:

    @classmethod
    @appier.operation(name = "Meow")
    def meow(cls):
        cats = cls.find()
        for cat in cats: cat._meow()
```

To make the same operation be associated with a single instance, just to apply to an instance method instead:

```python
    @appier.operation(name = "Meow")
    def meow(self):
        self._meow()
```

An operation can receive parameters that will be sent to the handler method:

```python
    @appier.operation(
        name = "Meow",
       	parameters = (
            ("Number of meows", "number_meows", int),
        )
    )
    def meow(self, number_meows = 5):
        for x in range(number_meows): self._meow()
```

## Model Links

To add a link from the model list page in the admin interface to anywhere else, add this to the model definition:

```python
class Cat

    @classmethod
    @appier.link(name = "Export Cats (CSV)")
    def export_csv(cls):
    	return appier.get_app().url_for("cat.list_csv")
```

In the same way, if the link is just for a particular instance, just use an instance method:

```python
    @appier.link(name = "Export Cat (CSV)")
    def export_csv(self):
    	return self.get_app().url_for("cat.show_csv")
```

Links can receive parameters as well:

```python
    @classmethod
    @appier.link(
        name = "Export Cats (CSV)",
       	parameters = (
            ("Start record", "start_record", int),
            ("Number of records", "number_records", int)
        )
    )
    def export_csv(cls, start_record = 0, number_records = 10):
    	return appier.get_app().url_for(
            "cat.list_csv", 
            start_record = start_record, 
            number_records = number_records
        )
```

## License

Appier Extras is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://travis-ci.org/hivesolutions/appier_extras.svg?branch=master)](https://travis-ci.org/hivesolutions/appier_extras)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/appier_extras/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/appier_extras?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/appier_extras.svg)](https://pypi.python.org/pypi/appier_extras)
