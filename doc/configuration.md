# Configuration

## Reference

The following are reserved configuration variables that modify Appier Extras behavior:

### Admin

* `ADMIN_LAYOUT` (`str`) - The base layout kind to be used (eg: `fluid`, `fixed`) (defaults to `fluid`)
* `ADMIN_THEME` (`str`) - The fonts and colors theme to be used (eg: `default`, `modern`, `flat`, `webook`) (defaults to `modern`)
* `ADMIN_STYLE` (`str`) - The sub-style to be used (think it as a sub-theme) (defaults to `romantic`)
* `ADMIN_LIBS` (`str`) - The version of the base javascript libraries to be used (eg: `current`, `legacy`, `next`, `edge`),
should be changed carefully to avoid unwanted changes (defaults to `current`)

### Email

* `BULK_EMAIL` (`bool`) - If the sent email should be marked as bulk by default (defaults to `False`)
* `UNSUBSCRIBE_EMAIL` (`bool`) - If the unsubscribe headers should be set while sending emails by default (defaults to `False`)
* `LOGO_EMAIL` (`bool`) - If the logo should be displayed for the email by default (defaults to `False`)
* `INLINE_EMAIL` (`bool`) - If by default the HTML of the email should be inlined (defaults to `False`)
* `INLINER_ENGINE` (`str`) - The name of the engine (eg: `premailer`, `toronado`, etc.) that is going to be used to inline CSS directives into HTML (defaults to `None`)
