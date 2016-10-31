# Configuration

## Reference

The following are reserved configuration variables that modify Appier Extras behavior:

#### Email

* `LOGO_EMAIL` (`str`) - URL of the logo to be inserted in the default email template (default to `None`)
* `INLINE_EMAIL` (`bool`) - If by default the HTML of the email should be inlined (default to `False`)
* `INLINER_ENGINE` (`str`) - The name of the engine (eg: `premailer`, `toronado`, etc.) that is going to be used to inline CSS directives into HTML (default to `None`)
