# Configuration

## Reference

The following are reserved configuration variables that modify Appier Extras behavior:

### Admin

| Name | Type | Description |
| ----- | ----- | ----- |
| **ADMIN_LAYOUT** | `str` | The base layout kind to be used (eg: `fluid`, `fixed`) (defaults to `fluid`). |
| **ADMIN_THEME** | `str` | The fonts and colors theme to be used (eg: `default`, `modern`, `flat`, `webook`) (defaults to `flat`). |
| **ADMIN_STYLE** | `str` | The sub-style to be used, think of it as a sub-theme (eg: `romantic`) (defaults to ``). |
| **ADMIN_LIBS** | `str` | The version of the base javascript libraries to be used (eg: `current`, `legacy`, `next`, `edge`), should be changed carefully to avoid unwanted changes (defaults to `current`). |
| **ADMIN_BACKGROUND** | `str` | The URL of the image to be used as background for simple pages (defaults to `None`). |
| **ADMIN_AVAILABLE** | `bool` | If the administration interface should be available/accessible to end-users (defaults to `True`). |
| **ADMIN_OPEN** | `bool` | If the administration interface should be open (for registration) to end-users (defaults to `False`). |
| **ADMIN_OAUTH** | `bool` | If OAuth 2.0 support should be enabled for the administration interface (defaults to `True`). |
| **ADMIN_AVATAR_DEFAULT** | `bool` | If a new default image should be set for an account's avatar if none is set (defaults to `False`). |

### Diag

| Name | Type | Description |
| ----- | ----- | ----- |
| **DIAG_STORE** | `bool` | If the multiple HTTP requests in diagnostics should be store in the data source (defaults to `False`). |
| **DIAG_LOGGLY** | `bool` | If the Loggly based logging should be used (defaults to `False`). |
| **DIAG_LOGSTASH** | `bool` | If the Logstash based logging should be used (defaults to `False`). |
| **DIAG_OUTPUT** | `bool` | If each of the HTTP requests should be printed to the stdout (defaults to `True`). |
| **DIAG_STDOUT** | `bool` | Same as `DIAG_OUTPUT`. |
| **DIAG_GEO** | `bool` | If the Geo IP resolution process should take place (extra CPU usage) for the processing of geographic information taken out of the IP address (defaults to `False`) . |
| **DIAG_LEVEL** | `str` | The level of verbosity to be used in the logging (eg: `minimal`, `normal`, `verbose` or `debug`) (defaults to `normal`). |
| **DIAG_VERBOSE** | `bool` | If the log output should be as verbose (extended) as possible (defaults to `False`). |
| **DIAG_MINIMAL** | `bool` | If the minimalistic version of the logging information should be used instead of the more verbose one (defaults to `False`). |
| **DIAG_FORMAT** | `str` | The format to be used while outputting the HTTP request (defaults to `combined`). |
| **DIAG_EMPTY** | `bool` | If the complete set of stored request entities should be removed from the data store on part load, use this value carefully to avoid unwanted results (defaults to `False`). |

### CMS

| Name | Type | Description |
| ----- | ----- | ----- |
| **CMS_CACHE_ENGINE** | `str` | The generic name of the cache engine to be used for CMS access (defaults to `memory`). |
| **CONTENTFUL_CACHE_ENGINE** | `str` | The name of the cache engine to be used for `Contentful` takes precedence over `CMS_CACHE_ENGINE`. |
| **PRISMIC_CACHE_ENGINE** | `str` | The name of the cache engine to be used for `Prismic CMS` takes precedence over `CMS_CACHE_ENGINE`. |

### Social

| Name | Type | Description |
| ----- | ----- | ----- |
| **ADMIN_SOCIAL_LIBS** | `list` | List of social agents that should have their libraries ensured to be installed (using `pip`) at loading, note that this should be an expensive on load operation (defaults to `[]`). |

### OAuth

| Name | Type | Description |
| ----- | ----- | ----- |
| **OAUTH_DURATION** | `int` | The default duration (in seconds) of the access token until it has to be refreshed (defaults to `3600`). |

### Email

| Name | Type | Description |
| ----- | ----- | ----- |
| **BULK_EMAIL** | `bool` | If the sent email should be marked as bulk by default (defaults to `False`). |
| **UNSUBSCRIBE_EMAIL** | `bool` | If the unsubscribe headers should be set while sending emails by default (defaults to `False`). |
| **LOGO_EMAIL** | `bool` | If the logo should be displayed for the email by default (defaults to `False`). |
| **INLINE_EMAIL** | `bool` | If by default the HTML of the email should be inlined (defaults to `False`). |
| **INLINER_ENGINE** | `str` | The name of the engine (eg: `premailer`, `toronado`, etc.) that is going to be used to inline CSS directives into HTML (defaults to `None`). |

### Loggly

| Name | Type | Description |
| ----- | ----- | ----- |
| **LOGGLY_LOG** | `bool` | If the Loggly based logging handler should be activated on part load (defaults to `False`). |
| **LOGGLY_BUFFER_SIZE** | `int` | The size of the buffer (in number of entries) until the buffer is flushed (defaults to `128`). |
| **LOGGLY_TIMEOUT** | `int` | The timeout in seconds in seconds until the buffer is flushed (defaults to `30`). |

### Sematext

| Name | Type | Description |
| ----- | ----- | ----- |
| **SEMATEXT_LOG** | `bool` | If the Sematext based logging handler should be activated on part load (defaults to `False`). |
| **SEMATEXT_BUFFER_SIZE** | `int` | The size of the buffer (in number of entries) until the buffer is flushed (defaults to `128`). |
| **SEMATEXT_TIMEOUT** | `int` | The timeout in seconds in seconds until the buffer is flushed (defaults to `30`). |

### Preflight

| Name | Type | Description |
| ----- | ----- | ----- |
| **PREFLIGHT_DATA** | `str` | The default data for the response to be returned to the `OPTIONS` request (defaults to ``). |
| **PREFLIGHT_MAX_AGE** | `int` | The number of seconds to be used in cache infvalication for the `Cache-Control` headers to be returned to the `OPTIONS` request (defaults to `86400`). |
