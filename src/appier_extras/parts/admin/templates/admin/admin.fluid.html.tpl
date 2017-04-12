{% extends "admin/layout.fluid.html.tpl" %}
{% block htitle %}{{ owner.description }} / {% block title %}{% endblock %}{% endblock %}
{% block links %}
    {% if acl("admin") %}
        {% if section == "admin" %}
            <a class="selected" href="{{ url_for('admin.index') }}">home</a>
        {% else %}
            <a href="{{ url_for('admin.index') }}">home</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.options") %}
        {% if section == "options" %}
            <a class="selected" href="{{ url_for('admin.options') }}">options</a>
        {% else %}
            <a href="{{ url_for('admin.options') }}">options</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.database") %}
        {% if section == "database" %}
            <a class="selected" href="{{ url_for('admin.database') }}">database</a>
        {% else %}
            <a href="{{ url_for('admin.database') }}">database</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.social") %}
        {% if section == "social" %}
            <a class="selected" href="{{ url_for('admin.social') }}">social</a>
        {% else %}
            <a href="{{ url_for('admin.social') }}">social</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.operations") %}
        {% if section == "operations" %}
            <a class="selected" href="{{ url_for('admin.operations') }}">operations</a>
        {% else %}
            <a href="{{ url_for('admin.operations') }}">operations</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.status") %}
        {% if section == "status" %}
            <a class="selected" href="{{ url_for('admin.status') }}">status</a>
        {% else %}
            <a href="{{ url_for('admin.status') }}">status</a>
        {% endif %}
    {% endif %}
    <div class="separator"></div>
    {% for _section, models in models_d.items() %}
        {% set available = own._available(models) %}
        {% if available|length > 0 %}
            {% for _model in available %}
                {% if acl("admin.models." + _model._name()) %}
                    {% if section == "models" and model and model._name() == _model._name() %}
                        <a class="selected"
                           href="{{ url_for('admin.show_model', model = _model._name()) }}">{{ _model._name() }}</a>
                    {% else %}
                        <a href="{{ url_for('admin.show_model', model = _model._name()) }}">{{ _model._name() }}</a>
                    {% endif %}
                {% endif %}
            {% endfor %}
            <div class="separator"></div>
        {% endif %}
    {% endfor %}
{% endblock %}
