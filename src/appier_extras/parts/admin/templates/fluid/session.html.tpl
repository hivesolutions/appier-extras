{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ session_s.sid }}{% endblock %}
{% block name %}{{ session_s.sid }}{% endblock %}
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
            {% for key in session_s.sorted() %}
                {% set value = session_s[key] %}
                <tr class="table-row">
                    <td class="text-left">
                        <strong>{{ key }}</strong>
                    </td>
                    <td class="text-left">{{ value }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
