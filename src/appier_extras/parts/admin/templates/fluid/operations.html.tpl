{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Operations{% endblock %}
{% block name %}Operations{% endblock %}
{% block windows %}
    {{ super() }}
    {% for key, value in own.admin_part._operations %}
        {% set operation_valid = not value.devel or owner.is_devel() %}
        {% if operation_valid %}
            {% if value.parameters %}
                <div id="window-{{ value.name }}" class="window window-operation">
                    <h1>{{ value.description }}</h1>
                    <form class="form" method="post" enctype="multipart/form-data"
                          action="{{ url_for(value.route, context = 'global', next = location) }}">
                        {% if value.note %}
                            <div class="description">{{ value.note|sentence|markdown }}</div>
                        {% endif %}
                        {% for parameter in value.parameters %}
                            {% set label, name, data_type = parameter[:3] %}
                            {% set default = parameter[3] if parameter|length > 3 else "" %}
                            {% set placeholder = parameter[4] if parameter|length > 4 else "" %}
                            <label>{{ label }}</label>
                            {{ tag_input_b(name, value = default, placeholder = placeholder, type = data_type) }}
                        {% endfor %}
                        <div class="window-buttons">
                            <span class="button button-cancel close-button">Cancel</span>
                            <span class="button button-confirm" data-submit="1">Confirm</span>
                        </div>
                    </form>
                </div>
            {% endif %}
        {% endif %}
    {% endfor %}
{% endblock %}
{% block content %}
    <ul class="sections-list">
        {% for key, value in own.admin_part._operations %}
            {% set operation_valid = not value.devel or owner.is_devel() %}
            {% if operation_valid %}
                <li>
                    <div class="name">
                        {% if value.parameters %}
                           <a class="button button-no-style {% if value.level > 1 %}warning{% endif %}" data-window_open="#window-{{ value.name }}">{{ value.description }}</a>
                        {% else %}
                            <a class="link {% if value.message %}link-confirm{% endif %} {% if value.level > 1 %}warning{% endif %}" href="{{ url_for(value.route, context = 'global', next = location) }}"
                                data-message="{{ value.message }}">{{ value.description }}
                            </a>
                        {% endif %}
                    </div>
                    <div class="description"><span>{{ value.note }}</span></div>
                </li>
            {% endif %}
        {% endfor %}
    </ul>
{% endblock %}
