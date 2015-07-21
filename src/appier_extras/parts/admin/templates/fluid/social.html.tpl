{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Social{% endblock %}
{% block name %}Social{% endblock %}
{% block content %}
    <ul class="sections-list">
        <li>
            <div class="name"><a href="{{ url_for('admin.google', context = 'global', next = location) }}">Link Google account</a></div>
            <div class="description"><span>Acces you Google account data and files</span></div>
        </li>
    </ul>
{% endblock %}
