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
    {% set names = model.list_names() %}
    {% call(item, name, mode = "card") paging_listers(
        entities,
        model,
        page,
        names = names,
        selection = True
    ) %}
        {% set description = model.to_description(name) %}
        {% set is_first = names.index(name) == 0 %}
        {% if is_first %}
            {% if acl("admin.models." + model._under()) %}
                {% call paging_item(description, mode = mode) %}
                    <a href="{{ url_for('admin.show_entity', model = model._under(), _id = item._id) }}">
                        {{ out(item, name) }}
                    </a>
                {% endcall %}
            {% else %}
                {% call paging_item(description, mode = mode) %}
                    {{ out(item, name) }}
                {% endcall %}
            {% endif %}
        {% else %}
            {% call paging_item(description, mode = mode) %}
                {{ out(item, name) }}
            {% endcall %}
        {% endif %}
    {% endcall %}
{% endblock %}
