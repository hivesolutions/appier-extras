# Models

Models that inherit from ``appier_extras.admin.Base`` are automatically added to the admin interface.
You can find more information about Appier models [here](http://appier.hive.pt/doc/models.md).

## Attributes

The admin input component for each model attribute is automatically chosen according to the attribute's data type:

* ``str``: textfield
* ``unicode``: textfield
* ``int``: textfield
* ``float``: textfield
* ``bool``: switch
* ``list``: textfield (JSON format)
* ``dict``: textfield (JSON format)
* ``appier.File``: file upload field
* ``appier.reference``: dropfield with auto-complete

Certain interface behaviours change according to other attribute modifiers besides the data type:

* ``private``: only visible in the edit view
* ``immutable``: only modifiable in the creation view

## Operations

Appier operations are picked up by the admin and made accessible through the interface. Here's an example:

```python
class Cat:

    @classmethod
    @appier.operation(name = "Meow")
    def meow(cls):
        cats = cls.find()
        for cat in cats: cat._meow()
```

To make the same operation be associated with a single instance, just apply to an instance method instead:

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
            ("Number of meows", "number_meows", int, 5),
        )
    )
    def meow(self, number_meows):
        for x in range(number_meows): self._meow()
```

## Links

Appier links are also picked up by the admin interface. Here's an example:

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
            ("Start record", "start_record", int, 0),
            ("Number of records", "number_records", int, 10)
        )
    )
    def export_csv(cls, start_record, number_records):
        return appier.get_app().url_for(
            "cat.list_csv",
            start_record = start_record,
            number_records = number_records
        )
```
