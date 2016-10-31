# Configuration

## Reference

The following are reserved configuration variables that modify Appier Extras behavior:

#### Email

* `BULK_EMAIL` (`bool`) - If the sent email should be marked as bulk by default (default `False`)
* `UNSUBSCRIBE_EMAIL` (`bool`) - If the unsubscribe headers should be set while sending emails by default (default to `False`)
* `LOGO_EMAIL` (`bool`) - If the logo should be displayed for the email by default (default to `False`)
* `INLINE_EMAIL` (`bool`) - If by default the HTML of the email should be inlined (default to `False`)
* `INLINER_ENGINE` (`str`) - The name of the engine (eg: `premailer`, `toronado`, etc.) that is going to be used to inline CSS directives into HTML (default to `None`)
