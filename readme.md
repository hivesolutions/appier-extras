# [![Appier Framework Extras]](res/logo.png)](http://appier_extras.hive.pt)

Set of extra elements for [Appier Framework](https://github.com/hivesolutions/appier) infra-structure.

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

    def start(self):
        appier.WebApp.start(self)

HelloApp().serve()
```

## Build Automation

[![Build Status](https://travis-ci.org/hivesolutions/appier_extras.png?branch=master)](https://travis-ci.org/hivesolutions/appier_extras)
