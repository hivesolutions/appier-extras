{% extends "admin/email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("Reset account", True) }}{% endblock %}
{% block content %}
    <p>Hello <strong>{{ account.username }}</strong>,</p>
    <p>
        You're receiving this email because someone requested a
        password reset for your user account at {{ owner.description }}.
    </p>
    <p>
        To reset your password just {{ link(url_for("admin.reset", reset_token = account.reset_token, absolute = True), "click here", False) }}
        and follow the instructions.
    </p>
    {{ h2("Support") }}
    {% set support_email = config.conf("SUPPORT_EMAIL")|default("no-reply@appier.hive.pt", True) %}
    <p>
        Are you having any trouble? We are here to help.<br/>
        Feel free to send us an email to {{ link("mailto:" + support_email, support_email, False) }} and we'll get in touch.
    </p>
    <p>
        Thank you,<br/>
        The {{ owner.description }} team
    </p>
{% endblock %}
