{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ model._name() }}{% endblock %}
{% block name %}{{ model._name() }}{% endblock %}
{% block style %}no-padding{% endblock %}
{% block buttons %}
    {{ super() }}
    {% if model.operations() %}
        <ul class="drop-down operations" data-name="Operations">
            {% for operation in model.operations() %}
                <li>
                    <a href="{{ url_for('admin.operation_model', model = model._name(), operation = operation.method, next = location_f) }}">{{ operation.name }}</a>
                </li>
            {% endfor %}
        </ul>
    {% endif %}
    <div class="button button-color button-green"
         data-link="{{ url_for('admin.new_entity', model = model._name()) }}">New</div>
{% endblock %}
{% block content %}
    <table class="filter bulk" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left selection">
                    <input type="checkbox" class="square small" />
                </th>
                {% for name in model.list_names() %}
                    {% if name == page.sorter %}
                        <th class="text-left direction {{ page.direction }}">
                            <a href="{{ page.query(sorter = name) }}">{{ name }}</a>
                        </th>
                    {% else %}
                        <th class="text-left">
                            <a href="{{ page.query(sorter = name) }}">{{ name }}</a>
                        </th>
                    {% endif %}
                {% endfor %}
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for entity in entities %}
                <tr class="table-row" data-id="{{ entity._id }}">
                    <td class="text-left selection">
                        <input type="checkbox" class="square small" />
                    </td>
                    {% for name in model.list_names() %}
                        {% if loop.first %}
                            <td class="text-left">
                                <a href="{{ url_for('admin.show_entity', model = model._name(), _id = entity._id) }}">
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
    {% if page.count > 1 %}
        {{ paging(page.index, page.count, caller = page.query) }}
    {% endif %}
{% endblock %}
