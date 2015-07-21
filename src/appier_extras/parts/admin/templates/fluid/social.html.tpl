{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Social{% endblock %}
{% block name %}Social{% endblock %}
{% block content %}
    <ul class="sections-list">
        <li>
            <div class="name"><a href="{{ url_for('admin.facebook', context = 'global', next = location) }}">Link Facebook account</a></div>
            <div class="description"><span>Enable acces to you socia Facebbok information</span></div>
        </li>
        <li>
            <div class="name"><a href="{{ url_for('admin.google', context = 'global', next = location) }}">Link Google account</a></div>
            <div class="description"><span>Enable access to you Google account data and files</span></div>
        </li>
    </ul>
{% endblock %}
