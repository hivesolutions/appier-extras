{% extends "admin/admin.static.html.tpl" %}
{% block title %}Models{% endblock %}
{% block name %}Models{% endblock %}
{% block content %}
    <ul>
        {% for section, models in own.admin_part.models_d.items() %}
            {% for model in models %}
                <li>{{ model._readable() }}</li>
            {% endfor %}
        {% endfor %}
    </ul>
{% endblock %}
