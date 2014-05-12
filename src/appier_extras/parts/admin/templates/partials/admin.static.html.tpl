{% extends "partials/layout.static.html.tpl" %}
{% block htitle %}{{ owner.name }} / {% block title %}{% endblock %}{% endblock %}
{% block links %}
    {% for model in models %}
        <a href="#">{{ model._name() }}</a>
    {% endfor %}
{% endblock %}
