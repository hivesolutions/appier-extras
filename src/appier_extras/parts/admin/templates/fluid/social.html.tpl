{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Social{% endblock %}
{% block name %}Social{% endblock %}
{% block content %}
    {% if socials %}
        <ul class="sections-list">
            {% if "facebook" in socials %}
                <li>
                    <div class="name"><a href="{{ url_for('admin.facebook', context = 'global', next = location) }}">Link Facebook account</a></div>
                    <div class="description"><span>Enable acces to you social Facebbok information</span></div>
                </li>
            {% endif %}
            {% if "github" in socials %}
                <li>
                    <div class="name"><a href="{{ url_for('admin.github', context = 'global', next = location) }}">Link GitHub account</a></div>
                    <div class="description"><span>Enable access to you GitHub developer profile</span></div>
                </li>
            {% endif %}
            {% if "google" in socials %}
                <li>
                    <div class="name"><a href="{{ url_for('admin.google', context = 'global', next = location) }}">Link Google account</a></div>
                    <div class="description"><span>Enable access to you Google account data and files</span></div>
                </li>
            {% endif %}
            {% if "live" in socials %}
                <li>
                    <div class="name"><a href="{{ url_for('admin.live', context = 'global', next = location) }}">Link Microsoft Live account</a></div>
                    <div class="description"><span>Enable access to you Microsoft profile</span></div>
                </li>
            {% endif %}
            {% if "twitter" in socials %}
                <li>
                    <div class="name"><a href="{{ url_for('admin.twitter', context = 'global', next = location) }}">Link Twitter account</a></div>
                    <div class="description"><span>Enable acces to you social Twitter information</span></div>
                </li>
            {% endif %}
        </ul>
    {% else %}
        <div class="quote">No social accounts enabled and/or available.</div>
    {% endif %}
{% endblock %}
