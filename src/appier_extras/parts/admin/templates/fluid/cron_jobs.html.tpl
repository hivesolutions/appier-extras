{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Cron Jobs{% endblock %}
{% block name %}Cron Jobs{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <table class="filter no-fixed" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Identifier</th>
                <th class="text-left">Description</th>
                <th class="text-left">Cron</th>
                <th class="text-left">Next Run</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for cron_job in cron_jobs %}
                <tr class="table-row">
                    <td class="text-left">
                        <strong>{{ cron_job.id }}</strong>
                    </td>
                    <td class="text-left">{{ cron_job.description|default("-", True) }}</td>
                    <td class="text-left">{{ cron_job.cron }}</td>
                    <td class="text-left">{{ cron_job.next_run() }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
