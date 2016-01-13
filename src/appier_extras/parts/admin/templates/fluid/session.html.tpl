{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ session.sid }}{% endblock %}
{% block name %}{{ session.sid }}{% endblock %}
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
            {% for key in session.sorted() %}
            	{% set value = session[key] %}
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
