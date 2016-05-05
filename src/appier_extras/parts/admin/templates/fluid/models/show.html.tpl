{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ model._name() }}{% endblock %}
{% block name %}{{ model._name() }}{% endblock %}
{% block style %}no-padding{% endblock %}
{% block buttons %}
    {{ super() }}
    <ul class="drop-down links force" data-name="Links">
        {% for link in model.links() %}
            {% if not link.instance %}
                {% if link.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ link.method }}">{{ link.name }}</a>
                    </li>
                {% else %}
                    <li>
                        <a class="no-async" target="_blank"
                           href="{{ url_for('admin.link_model', model = model._name(), link = link.method, is_global = '1') }}" >{{ link.name }}</a>
                    </li>
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <ul class="drop-down globals" data-name="Globals">
        {% for operation in model.operations() %}
            {% set operation_valid = not operation.devel or own.is_devel() %}
            {% if not operation.instance and operation_valid %}
                {% if operation.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ operation.method }}">{{ operation.name }}</a>
                    </li>
                {% else %}
                    {% if operation.level > 1 %}
                        <li>
                            <a href="{{ url_for('admin.operation_model', model = model._name(), operation = operation.method, is_global = '1', next = location_f) }}"
                               class="link-confirm" data-message="Are you sure you want to [[{{ operation.name }}]] ?">{{ operation.name }}</a>
                        </li>
                    {% else %}
                        <li>
                            <a href="{{ url_for('admin.operation_model', model = model._name(), operation = operation.method, is_global = '1', next = location_f) }}">{{ operation.name }}</a>
                        </li>
                    {% endif %}
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <ul class="drop-down operations" data-name="Operations">
        {% for operation in model.operations() %}
            {% if operation.instance %}
                {% if operation.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ operation.method }}">{{ operation.name }}</a>
                    </li>
                {% else %}
                    <li>
                        <a href="{{ url_for('admin.operation_model', model = model._name(), operation = operation.method, next = location_f) }}">{{ operation.name }}</a>
                    </li>
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <div class="button button-color button-green"
         data-link="{{ url_for('admin.new_entity', model = model._name()) }}">New</div>
{% endblock %}
{% block windows %}
    {{ super() }}
    {% for link in model.links() %}
        {% if link.parameters %}
            <div id="window-{{ link.method }}" class="window window-link">
                <h1>{{ link.name }}</h1>
                <form class="form" method="post" enctype="multipart/form-data"
                      action="{{ url_for('admin.link_model', model = model._name(), link = link.method, is_global = '' if link.instance else '1') }}">
                    {% for parameter in link.parameters %}
                        {% set label, name, data_type = parameter[:3] %}
                        {% set default = parameter[3] if parameter|length > 3 else "" %}
                        <label>{{ label }}</label>
                        {{ tag_input_b("parameters", value = default, type = data_type) }}
                    {% endfor %}
                    <div class="window-buttons">
                        <span class="button button-cancel close-button">Cancel</span>
                        <span class="button button-confirm" data-submit="1">Confirm</span>
                    </div>
                </form>
            </div>
        {% endif %}
    {% endfor %}
    {% for operation in model.operations() %}
        {% if operation.parameters %}
            <div id="window-{{ operation.method }}" class="window window-operation">
                <h1>{{ operation.name }}</h1>
                <form class="form" method="post" enctype="multipart/form-data"
                      action="{{ url_for('admin.operation_model', model = model._name(), operation = operation.method, is_global = '' if operation.instance else '1', next = location_f) }}">
                    {% for parameter in operation.parameters %}
                        {% set label, name, data_type = parameter[:3] %}
                        {% set default = parameter[3] if parameter|length > 3 else "" %}
                        <label>{{ label }}</label>
                        {{ tag_input_b("parameters", value = default, type = data_type) }}
                    {% endfor %}
                    <div class="window-buttons">
                        <span class="button button-cancel close-button">Cancel</span>
                        <span class="button button-confirm" data-submit="1">Confirm</span>
                    </div>
                </form>
            </div>
        {% endif %}
    {% endfor %}
{% endblock %}
{% block content %}
    <table class="filter bulk" data-no_input="1" data-size="{{ page.size }}"
           data-total="{{ page.total }}" data-pages="{{ page.count }}">
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
