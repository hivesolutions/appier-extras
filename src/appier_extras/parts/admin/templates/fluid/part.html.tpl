{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Parts / {{ info.name }}{% endblock %}
{% block name %}
    <a href="{{ url_for('admin.list_parts') }}">Parts</a>
    <span>/</span>
    <span>{{ info.name }}</span>
{% endblock %}
{% block style %}no-padding{% endblock %}
{% block buttons %}
    {{ super() }}
    {% if part.is_loaded() %}
        <div class="button button-color button-red"
             data-link="{{ url_for('admin.unload_part', name = info.name) }}">Unload</div>
    {% else %}
        <div class="button button-color button-green"
             data-link="{{ url_for('admin.load_part', name = info.name) }}">Load</div>
    {% endif %}
{% endblock %}
{% block content %}
    <table class="filter" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Key</th>
                <th class="text-left">Value</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for key in info_l %}
                {% set value = info[key] %}
                {% set value = "-" if value in (None, "") else value %}
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
