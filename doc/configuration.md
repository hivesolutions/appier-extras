# Configuration

## Reference

The following are reserved configuration variables that modify Appier Extras behavior:

### Admin

* `ADMIN_LAYOUT` (`str`) - The base layout kind to be used (eg: `fluid`, `fixed`) (defaults to `fluid`)
* `ADMIN_THEME` (`str`) - The fonts and colors theme to be used (eg: `default`, `modern`, `flat`, `webook`) (defaults to `flat`)
* `ADMIN_STYLE` (`str`) - The sub-style to be used, think of it as a sub-theme (eg: `romantic`) (defaults to ``)
* `ADMIN_LIBS` (`str`) - The version of the base javascript libraries to be used (eg: `current`, `legacy`, `next`, `edge`),
should be changed carefully to avoid unwanted changes (defaults to `current`)
* `ADMIN_BACKGROUND` (`str`) - The URL of the image to be used as background for simple pages (defaults to `None`)
* `ADMIN_OPEN` (`bool`) - If the administration interface should be open and available to end-users (defaults to `False`)
* `ADMIN_OAUTH` (`bool`) - If OAuth 2.0 support should be enabled for the administration interface (defaults to `True`)
* `ADMIN_AVATAR_DEFAULT` (`bool`) - If a new default image should be set for an account's avatar if none is set (defaults to `False`)

### Social

* `ADMIN_SOCIAL_LIBS` (`list`) - List of social agents that should have their libraries ensured to be installed (using `pip`) at loading,
note that this should be an expensive on load operation (defaults to `[]`)

### Email

* `BULK_EMAIL` (`bool`) - If the sent email should be marked as bulk by default (defaults to `False`)
* `UNSUBSCRIBE_EMAIL` (`bool`) - If the unsubscribe headers should be set while sending emails by default (defaults to `False`)
* `LOGO_EMAIL` (`bool`) - If the logo should be displayed for the email by default (defaults to `False`)
* `INLINE_EMAIL` (`bool`) - If by default the HTML of the email should be inlined (defaults to `False`)
* `INLINER_ENGINE` (`str`) - The name of the engine (eg: `premailer`, `toronado`, etc.) that is going to be used to inline CSS directives into HTML (defaults to `None`)
