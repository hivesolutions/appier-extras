{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Parts{% endblock %}
{% block name %}Parts{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <table class="filter" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Part</th>
                <th class="text-left">Version</th>
                <th class="text-left no-mobile">Class</th>
                <th class="text-left">Status</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for part in parts %}
                {% set _part = part.part %}
                <tr class="table-row">
                    <td class="text-left">
                        <strong>
                            <a href="{{ url_for('admin.show_part', name = part.name) }}">{{ part.name }}</a>
                        </strong>
                    </td>
                    <td class="text-left">{{ part.version }}</td>
                    <td class="text-left no-mobile">{{ part.class_name }}</td>
                    <td class="text-left">
                        {% if _part.is_loaded() %}
                            <span class="tag green">Loaded</span>
                        {% else %}
                            <span class="tag red">Unloaded</span>
                        {% endif %}
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
