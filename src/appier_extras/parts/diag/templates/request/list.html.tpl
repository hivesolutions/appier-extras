{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Requests{% endblock %}
{% block name %}Requests{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    {% call(item, name, mode = "card") paging_listers(
        request,
        model,
        page,
        names = ("method", "path", "code", "address", "date", "browser")
    ) %}
        {% set reference = name|capitalize %}
        {% if name == "code" %}
            {% set reference = "Status" %}
        {% elif name == "date" %}
            {% set name = "timestamp_d" %}
        {% endif %}

        {% if name == "method" %}
            {% call paging_item("Method", mode = mode) %}
                <span class="tag {{ item.method|lower }}">{{ item.method }}</span>
            {% endcall %}
        {% elif name == "path" %}
            {% call paging_item("Path", mode = mode) %}
                <a href="{{ url_for('diag.show_request', id = item.id) }}">{{ item.path }}</a>
            {% endcall %}
        {% else %}
            {{ paging_item(reference, item[name], mode = mode) }}
        {% endif %}
    {% endcall %}
{% endblock %}
