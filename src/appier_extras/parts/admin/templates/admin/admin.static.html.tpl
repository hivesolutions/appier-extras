{% extends "admin/layout.static.html.tpl" %}
{% block htitle %}{{ owner.description }} / {% block title %}{% endblock %}{% endblock %}
{% block links %}
    {% for model in models %}
        <a href="#">{{ model._name() }}</a>
    {% endfor %}
{% endblock %}
