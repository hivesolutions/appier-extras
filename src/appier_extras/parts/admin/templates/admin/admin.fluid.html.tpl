{% extends "admin/layout.fluid.html.tpl" %}
{% block htitle %}{{ owner.description }} / {% block title %}{% endblock %}{% endblock %}
{% block links %}
    <h3>Settings</h3>
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
    {% if own.admin_part._sections %}
        {% for _section, items in own.admin_part._sections %}
            <div class="separator"></div>
            <h3>{{ _section }}</h3>
            {% for name, route in items %}
                {% if acl(route) %}
                    {% if section == "section:" + _section|lower|replace(" ", "_") + ":" + name|lower|replace(" ", "_") %}
                        <a class="selected" href="{{ url_for(route) }}">{{ name }}</a>
                    {% else %}
                        <a href="{{ url_for(route) }}">{{ name }}</a>
                    {% endif %}
                {% endif %}
            {% endfor %}
        {% endfor %}
    {% endif %}
    {% for _section, models in own.admin_part.models_d.items() %}
        {% set available = own.admin_part._available(models) %}
        {% if available|length > 0 %}
            <div class="separator"></div>
            <h3>{{ appier.underscore_to_readable(_section, capitalize = True) }}</h3>
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
        {% endif %}
    {% endfor %}
{% endblock %}
