{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Operations{% endblock %}
{% block name %}Operations{% endblock %}
{% block content %}
    <ul class="sections-list">
        {% for key, value in own.admin_part._operations %}
            <li>
                <div class="name">
                    <a class="link {% if value.message %}link-confirm{% endif %} {% if value.level > 1 %}warning{% endif %}" href="{{ url_for(value.route, context = 'global', next = location) }}"
                        data-message="{{ value.message }}">{{ value.description }}
                    </a>
                </div>
                <div class="description"><span>{{ value.note }}</span></div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
