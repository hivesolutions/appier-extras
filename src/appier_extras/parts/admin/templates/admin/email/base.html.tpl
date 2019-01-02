{% extends owner.admin_email_layout %}
{% block title %}{{ title|default(subject, True)|default("Test email", True) }}{% endblock %}
{% block content %}
    {{ contents|safe }}
{% endblock %}
