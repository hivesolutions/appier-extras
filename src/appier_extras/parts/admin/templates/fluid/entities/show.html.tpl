{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ entity }}{% endblock %}
{% block name %}{{ entity }}{% endblock %}
{% block buttons %}
    {{ super() }}
    <ul class="drop-down links force" data-name="Links">
        {% for link in model.links() %}
            {% if link.instance %}
                {% if link.parameters %}
                    <li>
                        <a class="button" data-window_open="#window-{{ link.method }}">{{ link.name }}</a>
                    </li>
                {% else %}
                    <li>
                        <a class="no-async" target="_blank"
                           href="{{ url_for('admin.link_model', model = model._name(), link = link.method, ids = entity._id) }}" >{{ link.name }}</a>
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
                            <a href="{{ url_for('admin.operation_model', model = model._name(), operation = operation.method, ids = entity._id, next = location_f) }}"
                               class="link-confirm" data-message="Are you sure you want to [[{{ operation.name }}]] ?">{{ operation.name }}</a>
                        </li>
                    {% else %}
                        <li>
                            <a href="{{ url_for('admin.operation_model', model = model._name(), operation = operation.method, ids = entity._id, next = location_f) }}">{{ operation.name }}</a>
                        </li>
                    {% endif %}
                {% endif %}
            {% endif %}
        {% endfor %}
    </ul>
    <div class="button button-color button-grey"
         data-link="{{ url_for('admin.edit_entity', model = model._name(), _id = entity._id) }}">Edit</div>
{% endblock %}
{% block windows %}
    {{ super() }}
    {% for link in model.links() %}
        {% if link.parameters %}
            <div id="window-{{ link.method }}" class="window window-link">
                <h1>{{ link.name }}</h1>
                <form class="form" method="post" enctype="multipart/form-data"
                      action="{{ url_for('admin.link_model', model = model._name(), link = link.method, ids = entity._id) }}" >
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
                      action="{{ url_for('admin.operation_model', model = model._name(), operation = operation.method, ids = entity._id, next = location_f) }}" >
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
    <div class="show-panel">
        <div class="panel-contents simple">
            <dl class="inline">
                {% for name in model.show_names() %}
                    <div class="item">
                        <dt>{{ name }}</dt>
                        <dd>{{ out(entity, name) }}</dd>
                    </div>
                {% endfor %}
            </dl>
        </div>
    </div>
{% endblock %}
