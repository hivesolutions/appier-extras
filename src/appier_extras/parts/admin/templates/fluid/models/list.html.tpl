{% extends "partials/layout.fluid.html.tpl" %}
{% block title %}Admin{% endblock %}
{% block name %}Site administration{% endblock %}
{% block content %}
    <div>
        <ul>
            {% for model in models %}
                <li>
                    <a href="{{ url_for('admin.show_model', model = model._name()) }}">{{ model._name() }}</a>
                </li>
            {% endfor %}
        </ul>
    </div>
{% endblock %}
