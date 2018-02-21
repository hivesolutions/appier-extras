{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Requests / {{ request.id }}{% endblock %}
{% block name %}
    <a href="{{ url_for('diag.list_requests') }}">Requests</a>
    <span>/</span>
    <span>{{ request.id }}</span>
{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <table class="filter" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Key</th>
                <th class="text-left">Value</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for key in request.__class__.fields() %}
                {% set value = request[key] %}
                <tr class="table-row">
                    <td class="text-left">
                        <strong>{{ key }}</strong>
                    </td>
                    <td class="text-left">{{ value|default("-", True) }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
