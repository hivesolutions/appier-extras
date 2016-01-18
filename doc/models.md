# Models

Models that inherit from ``appier_extras.admin.Base`` are automatically added to the admin interface.

You can find more information about Appier models [here](http://appier.hive.pt/doc/models.md).

## Model Attributes

The admin interface has support for the attribute types provided by Appier:
* A text field is presented for attributes of type ``str``, ``unicode``, ``int`` and ``float``
* ``bool``attributes are set with a toggle switch.
* Attributes of type ``list`` or ``dict`` can be edited in JSON format.
* If the attribute is an ``appier.File`` object then a file upload input is shown. 
* For an ``appier.reference`` attribute its text field has support for autocomplete.

Attributes with the ``private`` <em>keyword</em> set to ``True`` are only shown in the model edit view.
Immutable attributes cannot be edited.

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

