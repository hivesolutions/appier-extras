{% extends "admin/email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("Test email", True) }}{% endblock %}
{% block content %}
    {{ contents|safe }}
{% endblock %}
