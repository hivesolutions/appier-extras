{% extends "admin/layout.fluid.html.tpl" %}
{% block htitle %}{{ owner.description }} / {% block title %}{% endblock %}{% endblock %}
{% block links %}
    {% if acl("admin") %}
        {% if section == "admin" %}
            <a class="selected" href="{{ url_for('admin.index') }}">Home</a>
        {% else %}
            <a href="{{ url_for('admin.index') }}">Home</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.options") %}
        {% if section == "options" %}
            <a class="selected" href="{{ url_for('admin.options') }}">Options</a>
        {% else %}
            <a href="{{ url_for('admin.options') }}">Options</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.database") %}
        {% if section == "database" %}
            <a class="selected" href="{{ url_for('admin.database') }}">Database</a>
        {% else %}
            <a href="{{ url_for('admin.database') }}">Database</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.social") %}
        {% if section == "social" %}
            <a class="selected" href="{{ url_for('admin.social') }}">Social</a>
        {% else %}
            <a href="{{ url_for('admin.social') }}">Social</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.operations") %}
        {% if section == "operations" %}
            <a class="selected" href="{{ url_for('admin.operations') }}">Operations</a>
        {% else %}
            <a href="{{ url_for('admin.operations') }}">Operations</a>
        {% endif %}
    {% endif %}
    {% if acl("admin.status") %}
        {% if section == "status" %}
            <a class="selected" href="{{ url_for('admin.status') }}">Status</a>
        {% else %}
            <a href="{{ url_for('admin.status') }}">Status</a>
        {% endif %}
    {% endif %}
    <div class="separator"></div>
    {% for _section, models in models_d.items() %}
        {% set available = own._available(models) %}
        {% if available|length > 0 %}
            {% for _model in available %}
                {% if acl("admin.models." + _model._under()) %}
                    {% if section == "models" and model and model._under() == _model._under() %}
                        <a class="selected"
                           href="{{ url_for('admin.show_model', model = _model._under()) }}">{{ _model._readable(plural = True) }}</a>
                    {% else %}
                        <a href="{{ url_for('admin.show_model', model = _model._under()) }}">{{ _model._readable(plural = True) }}</a>
                    {% endif %}
                {% endif %}
            {% endfor %}
            <div class="separator"></div>
        {% endif %}
    {% endfor %}
{% endblock %}
