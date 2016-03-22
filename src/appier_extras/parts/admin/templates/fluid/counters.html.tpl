{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Counters{% endblock %}
{% block name %}Counter{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <table class="filter no-fixed" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Identififer</th>
                <th class="text-left">Sequence</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for counter in counters %}
                <tr class="table-row">
                    <td class="text-left">
                        <strong>{{ counter._id }}</strong>
                    </td>
                    <td class="text-left">{{ counter.seq }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
