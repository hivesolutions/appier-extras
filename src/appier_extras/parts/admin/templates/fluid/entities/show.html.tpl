{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ entity }}{% endblock %}
{% block name %}
    {% if own._is_available(model) %}
        <a href="{{ url_for('admin.show_model', model = model._under()) }}">
            {{ model._readable(plural = True) }}
        </a>
    {% else %}
        <span>{{ model._readable(plural = True) }}</span>
    {% endif %}
    <span>/</span>
    <span>{{ entity }}</span>
{% endblock %}
{% block buttons %}
    {{ super() }}
    <ul class="drop-down views force" data-name="Views">
        {% for view in model.views() %}
            {% set view_valid = not view.devel or own.is_devel() %}
            {% if view.instance and view_valid %}
                {% if view.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ view.method }}">{{ view.name }}</a>
                    </li>
                {% else %}
                    <li>
                        <a href="{{ url_for('admin.view_model', model = model._under(), view = view.method, id = entity._id) }}">{{ view.name }}</a>
                    </li>
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <ul class="drop-down links force" data-name="Links">
        {% for link in model.links() %}
            {% set link_valid = not link.devel or own.is_devel() %}
            {% if (link.instance or link.context) and link_valid %}
                {% if link.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ link.method }}">{{ link.name }}</a>
                    </li>
                {% else %}
                    <li>
                        {% if link.context %}
                            <a class="no-async" target="_blank"
                               href="{{ url_for('admin.link_model', model = model._under(), link = link.method, context = entity._id) }}">{{ link.name }}</a>
                        {% else %}
                            <a class="no-async" target="_blank"
                               href="{{ url_for('admin.link_model', model = model._under(), link = link.method, ids = entity._id) }}">{{ link.name }}</a>
                        {% endif %}
                    </li>
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <ul class="drop-down operations force" data-name="Operations">
        {% for operation in model.operations() %}
            {% set operation_valid = not operation.devel or own.is_devel() %}
            {% if operation.instance and operation_valid %}
                {% if operation.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ operation.method }}">{{ operation.name }}</a>
                    </li>
                {% else %}
                    {% if operation.level > 1 %}
                        <li>
                            <a href="{{ url_for('admin.operation_model', model = model._under(), operation = operation.method, ids = entity._id, next = location_f) }}"
                               class="link-confirm" data-message="Are you sure you want to [[{{ operation.name }}]] ?">{{ operation.name }}</a>
                        </li>
                    {% else %}
                        <li>
                            <a href="{{ url_for('admin.operation_model', model = model._under(), operation = operation.method, ids = entity._id, next = location_f) }}">{{ operation.name }}</a>
                        </li>
                    {% endif %}
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <div class="button button-color button-blue"
         data-link="{{ url_for('admin.edit_entity', model = model._under(), _id = entity._id) }}">Edit</div>
{% endblock %}
{% block windows %}
    {{ super() }}
    {% for view in model.views() %}
        {% if view.parameters %}
            <div id="window-{{ view.method }}" class="window window-view">
                <h1>{{ view.name }}</h1>
                <form class="form" method="get"
                      action="{{ url_for('admin.view_model', model = model._under(), view = view.method, id = entity._id) }}">
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
            {% if link.context %}
                {% set form_url = url_for('admin.link_model', model = model._under(), link = link.method, context = entity._id) %}
            {% else %}
                {% set form_url = url_for('admin.link_model', model = model._under(), link = link.method, ids = entity._id) %}
            {% endif %}
            <div id="window-{{ link.method }}" class="window window-link">
                <h1>{{ link.name }}</h1>
                <form class="form" method="post" enctype="multipart/form-data"
                      action="{{ form_url }}">
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
                      action="{{ url_for('admin.operation_model', model = model._under(), operation = operation.method, ids = entity._id, next = location_f) }}">
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
        <div class="key" data-key="76" data-url="{{ url_for('admin.show_model', model = model._under()) }}"></div>
        <div class="key" data-key="69" data-url="{{ url_for('admin.edit_entity', model = model._under(), _id = entity._id) }}"></div>
        {% if previous_url %}<div class="previous-url hidden">{{ previous_url }}</div>{% endif %}
        {% if next_url %}<div class="next-url hidden">{{ next_url }}</div>{% endif %}
    </div>
    <div class="show-panel">
        <div class="panel-contents simple">
            <dl class="inline">
                {% for name in model.show_names() %}
                    {% set description = model.to_description(name) %}
                    {% set observations = model.to_observations(name) %}
                    <div class="item">
                        <dt>
                            {% if observations %}
                                <div class="balloon balloon-observations">
                                    <span class="baloon-icon">{{ description }}</span>
                                    <div class="balloon-contents">{{ observations|sentence|markdown }}</div>
                                </div>
                            {% else%}
                                <span>{{ description }}</span>
                            {% endif %}
                        </dt>
                        <dd>{{ out(entity, name) }}</dd>
                    </div>
                {% endfor %}
            </dl>
        </div>
    </div>
{% endblock %}
