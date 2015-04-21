{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Routes{% endblock %}
{% block name %}Routes{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <table class="filter" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Methods</th>
                <th class="text-left">URL</th>
                <th class="text-left">Name</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for route in routes %}
                {% set methods = route[0] %}
                {% set opts = route[3] if route|length > 3 else {} %}
                <tr class="table-row">
                    <td class="text-left">
                        {% for method in methods %}
                            <span class="tag {{ method|lower }}">{{ method }}</span>
                        {% endfor %}
                    </td>
                    <td class="text-left">
                        <strong>{{ opts.base }}</strong>
                    </td>
                    <td class="text-left">
                        <strong>{{ opts.name }}</strong>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
