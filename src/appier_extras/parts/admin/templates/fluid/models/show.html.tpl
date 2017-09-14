{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ model._readable(plural = True) }}{% endblock %}
{% block name %}{{ model._readable(plural = True) }}{% endblock %}
{% block style %}no-padding{% endblock %}
{% block buttons %}
    {{ super() }}
    <ul class="drop-down views" data-name="Views">
        {% for view in model.views() %}
            {% set view_valid = not view.devel or own.is_devel() %}
            {% if not view.instance and view_valid %}
                {% if view.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ view.method }}">{{ view.name }}</a>
                    </li>
                {% else %}
                    <li>
                        <a href="{{ url_for('admin.view_model', model = model._under(), view = view.method) }}">{{ view.name }}</a>
                    </li>
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <ul class="drop-down links" data-name="Links">
        {% for link in model.links() %}
            {% set link_valid = not link.devel or own.is_devel() %}
            {% if not link.instance and link_valid %}
                {% if link.parameters %}
                    <li>
                        <a class="button {% if link.context %}context{% endif %}" data-window_open="#window-{{ link.method }}">{{ link.name }}</a>
                    </li>
                {% else %}
                    <li>
                        <a class="no-async {% if link.context %}context{% endif %}" target="_blank"
                           href="{{ url_for('admin.link_model', model = model._under(), link = link.method, is_global = '1') }}">{{ link.name }}</a>
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
                            <a href="{{ url_for('admin.operation_model', model = model._under(), operation = operation.method, is_global = '1', next = location_f) }}"
                               class="link-confirm" data-message="Are you sure you want to [[{{ operation.name }}]] ?">{{ operation.name }}</a>
                        </li>
                    {% else %}
                        <li>
                            <a href="{{ url_for('admin.operation_model', model = model._under(), operation = operation.method, is_global = '1', next = location_f) }}">{{ operation.name }}</a>
                        </li>
                    {% endif %}
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <ul class="drop-down operations" data-name="Operations">
        {% for operation in model.operations() %}
            {% set operation_valid = not operation.devel or own.is_devel() %}
            {% if operation.instance and operation_valid %}
                {% if operation.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ operation.method }}">{{ operation.name }}</a>
                    </li>
                {% else %}
                    <li>
                        <a href="{{ url_for('admin.operation_model', model = model._under(), operation = operation.method, next = location_f) }}">{{ operation.name }}</a>
                    </li>
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <div class="button button-color button-green"
         data-link="{{ url_for('admin.new_entity', model = model._under()) }}">New</div>
{% endblock %}
{% block windows %}
    {{ super() }}
    {% for view in model.views() %}
        {% if view.parameters %}
            <div id="window-{{ view.method }}" class="window window-view">
                <h1>{{ view.name }}</h1>
                <form class="form" method="get"
                      action="{{ url_for('admin.view_model', model = model._under(), view = view.method) }}">
                    {% if view.description %}
                        <div class="description">{{ view.description|sentence|markdown }}</div>
                    {% endif %}
                    {% for parameter in view.parameters %}
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
    {% for link in model.links() %}
        {% if link.parameters %}
            <div id="window-{{ link.method }}" class="window window-link">
                <h1>{{ link.name }}</h1>
                <form class="form {% if not link.instance and link.context %}context{% endif %}" method="post" enctype="multipart/form-data"
                      action="{{ url_for('admin.link_model', model = model._under(), link = link.method, is_global = '' if link.instance else '1') }}">
                    {% if link.description %}
                        <div class="description">{{ link.description|sentence|markdown }}</div>
                    {% endif %}
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
                      action="{{ url_for('admin.operation_model', model = model._under(), operation = operation.method, is_global = '' if operation.instance else '1', next = location_f) }}">
                    {% if operation.description %}
                        <div class="description">{{ operation.description|sentence|markdown }}</div>
                    {% endif %}
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
    <div class="shortcuts">
        <div class="key" data-key="78" data-url="{{ url_for('admin.new_entity', model = model._under()) }}"></div>
    </div>
    <div class="listers">
        <div class="cards lister">
            {% for entity in entities %}
                <div class="card">
                    <dl>
                        {% for name in model.list_names() %}
                            <div class="item">
                                {% set description = model.to_description(name) %}
                                <dt>{{ description }}</dt>
                                {% if loop.first %}
                                    {% if acl("admin.models." + model._under()) %}
                                        <dd>
                                            <a href="{{ url_for('admin.show_entity', model = model._under(), _id = entity._id) }}">
                                                {{ out(entity, name) }}
                                            </a>
                                        </dd>
                                    {% else %}
                                        <dd class="text-left">{{ out(entity, name) }}</dd>
                                    {% endif %}
                                {% else %}
                                    <dd class="text-left">{{ out(entity, name) }}</dd>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </dl>
                </div>
            {% endfor %}
        </div>
        <table class="filter bulk lister" data-no_input="1" data-size="{{ page.size }}"
               data-total="{{ page.total }}" data-pages="{{ page.count }}">
            <thead>
                <tr class="table-row table-header">
                    <th class="text-left selection">
                        <input type="checkbox" class="square small" />
                    </th>
                    {% for name in model.list_names() %}
                        {% set description = model.to_description(name) %}
                        {% if name == page.sorter %}
                            <th class="text-left direction {{ page.direction }}">
                                <a href="{{ page.query(sorter = name) }}">{{ description }}</a>
                            </th>
                        {% else %}
                            <th class="text-left">
                                <a href="{{ page.query(sorter = name) }}">{{ description }}</a>
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
                                {% if acl("admin.models." + model._under()) %}
                                    <td class="text-left">
                                        <a href="{{ url_for('admin.show_entity', model = model._under(), _id = entity._id) }}">
                                            {{ out(entity, name) }}
                                        </a>
                                    </td>
                                {% else %}
                                    <td class="text-left">{{ out(entity, name) }}</td>
                                {% endif %}
                            {% else %}
                                <td class="text-left">{{ out(entity, name) }}</td>
                            {% endif %}
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% if page.count > 1 %}
        {{ paging(page.index, page.count, caller = page.query) }}
    {% endif %}
{% endblock %}
