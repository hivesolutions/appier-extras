{% extends "email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("Reset account", True) }}{% endblock %}
{% block content %}
    <p>
        Hello {{ account.username }},<br/>
        You're receiving this email because someone requested a
        password reset for your user account at {{ owner.description }}.<br/>
        To reset your password just {{ link(url_for("admin.reset", reset_token = account.reset_token, absolute = True), "click here", False) }}.
    </p>
    <p>
        Thank you,<br/>
        The {{ owner.description }} team
    </p>
{% endblock %}
