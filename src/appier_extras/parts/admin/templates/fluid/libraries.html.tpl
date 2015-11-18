{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Libraries{% endblock %}
{% block name %}Libraries{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <table class="filter" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Library</th>
                <th class="text-left">Version</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for name, version in libraries %}
                <tr class="table-row">
                    <td class="text-left">
                        <strong>{{ name }}</strong>
                    </td>
                    <td class="text-left">{{ version }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
