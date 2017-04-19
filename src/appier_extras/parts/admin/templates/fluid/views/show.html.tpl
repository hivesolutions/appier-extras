{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ entity }} :: {{ definition.name }}{% endblock %}
{% block name %}{{ entity }} :: {{ definition.name }}{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <table class="filter bulk" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left selection">
                    <input type="checkbox" class="square small" />
                </th>
                {% for name in names or model.list_names() %}
                    {% set description = target.to_description(name) %}
                    <th class="text-left">
                        <a href="{{ name }}">{{ description }}</a>
                    </th>
                {% endfor %}
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for entity in entities %}
                <tr class="table-row" data-id="{{ entity._id }}">
                    <td class="text-left selection">
                        <input type="checkbox" class="square small" />
                    </td>
                    {% for name in names or target.list_names() %}
                        {% if loop.first %}
                            <td class="text-left">
                                <a href="{{ url_for('admin.show_entity', model = target._name(), _id = entity._id) }}">
                                    {{ out(entity, name) }}
                                </a>
                            </td>
                        {% else %}
                            <td class="text-left">{{ out(entity, name) }}</td>
                        {% endif %}
                    {% endfor %}
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
