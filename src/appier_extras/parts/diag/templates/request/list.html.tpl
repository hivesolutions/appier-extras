{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Requests{% endblock %}
{% block name %}Requests{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    {% call(item, name, mode = "card") paging_listers(
        requests,
        model,
        page,
        names = ("method", "path", "code", "address", "date", "browser")
    ) %}
        {% set description = model.to_description(name) %}
        {% if name == "code" %}
            {% set description = "Status" %}
        {% elif name == "date" %}
            {% set name = "timestamp_d" %}
        {% endif %}
        {% set value = item[name] %}

        {% if name == "method" %}
            {% call paging_item(description, mode = mode) %}
                <span class="tag {{ value|lower }}">{{ value }}</span>
            {% endcall %}
        {% elif name == "path" %}
            {% call paging_item(description, mode = mode) %}
                <a href="{{ url_for('diag.show_request', id = item.id) }}">{{ value }}</a>
            {% endcall %}
        {% else %}
            {{ paging_item(description, value, mode = mode) }}
        {% endif %}
    {% endcall %}
{% endblock %}
