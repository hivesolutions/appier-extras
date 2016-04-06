{% extends "email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("Reset account", True) }}{% endblock %}
{% block content %}
    <p>
        Hello {{ account.username }},<br/>
        Please clicl here to reset you password.<br/>
    </p>
    <p>
        Thank you,<br/>
        The {{ owner.description }} team
    </p>
{% endblock %}
