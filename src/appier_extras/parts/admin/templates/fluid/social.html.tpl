{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Social{% endblock %}
{% block name %}Social{% endblock %}
{% block content %}
    <ul class="sections-list">
        <li>
            <div class="name"><a href="{{ url_for('admin.google', next = location) }}">Google</a></div>
            <div class="description"><span>Link you Google account</span></div>
        </li>
    </ul>
{% endblock %}
