# [![Appier Framework Extras](res/logo.png)](http://appier-extras.hive.pt)

**Appier on Steroids**

Appier Extras is a set of extra elements for [Appier Framework](http://appier.hive.pt).
Amongst other features, it brings an admin interface that is automatically generated
by inspecting the application models, allowing the developer to easily have a way to manage
the data and processes for an instance.

Here's how to launch a minimal app with Appier Extras:

```python
import appier
import appier_extras

class HelloApp(appier.WebApp):

    def __init__(self):
        appier.WebApp.__init__(self, parts=(appier_extras.AdminPart,))

HelloApp().serve()
```

Running it is just as simple:

```bash
pip install appier appier_extras
python hello.py
```

You can now go to [http://localhost:8080/admin](http://localhost:8080/admin) and login with root/root.

## Learn more

* [Models](doc/models.md) - extra model features
* [Configuration](doc/configuration.md) - how to configure Appier Extras

## License

Appier Extras is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://app.travis-ci.com/hivesolutions/appier-extras.svg?branch=master)](https://travis-ci.com/github/hivesolutions/appier-extras)
[![Build Status GitHub](https://github.com/hivesolutions/appier-extras/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/appier-extras/actions)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/appier-extras/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/appier-extras?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/appier-extras.svg)](https://pypi.python.org/pypi/appier-extras)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
