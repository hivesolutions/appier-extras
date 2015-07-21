{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Social{% endblock %}
{% block name %}Social{% endblock %}
{% block content %}
    {% if socials %}
        <ul class="sections-list">
            {% if "facebook" in socials %}
                <li>
                    <div class="name"><a href="{{ url_for('admin.facebook', context = 'global', next = location) }}">Link Facebook account</a></div>
                    <div class="description"><span>Enable acces to you socia Facebbok information</span></div>
                </li>
            {% endif %}
            {% if "google" in socials %}
                <li>
                    <div class="name"><a href="{{ url_for('admin.google', context = 'global', next = location) }}">Link Google account</a></div>
                    <div class="description"><span>Enable access to you Google account data and files</span></div>
                </li>
            {% endif %}
        </ul>
    {% else %}
        <div class="quote">No social accounts available for admin.</div>
    {% endif %}
{% endblock %}
