{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Parts{% endblock %}
{% block name %}Parts{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <table class="filter" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Part</th>
                <th class="text-left">Class</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for part in parts %}
                <tr class="table-row">
                    <td class="text-left">
                        <strong>{{ part.name }}</strong>
                    </td>
                    <td class="text-left">{{ part.class_name }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
