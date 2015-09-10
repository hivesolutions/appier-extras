{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Social{% endblock %}
{% block name %}Social{% endblock %}
{% block content %}
    {% if socials %}
        <ul class="sections-list">
            {% if "facebook" in socials %}
                {% if "facebook" in linked %}
                    <li>
                        <div class="name"><a class="warning" href="{{ url_for('admin.unlink_facebook', context = 'global', next = location) }}">Unlink Facebook account</a></div>
                        <div class="description"><span>You're currently linked to Facebook under <strong>{{ linked.facebook }}</strong></span></div>
                    </li>
                {% else %}
                    <li>
                        <div class="name"><a href="{{ url_for('admin.facebook', context = 'global', next = location) }}">Link Facebook account</a></div>
                        <div class="description"><span>Enable access to you social Facebbok information</span></div>
                    </li>
                {% endif %}
            {% endif %}
            {% if "github" in socials %}
                {% if "github" in linked %}
                    <li>
                        <div class="name"><a class="warning" href="{{ url_for('admin.unlink_github', context = 'global', next = location) }}">Unlink GitHub account</a></div>
                        <div class="description"><span>You're currently linked to GitHub under <strong>{{ linked.github }}</strong></span></div>
                    </li>
                {% else %}
                    <li>
                        <div class="name"><a href="{{ url_for('admin.github', context = 'global', next = location) }}">Link GitHub account</a></div>
                        <div class="description"><span>Enable access to you GitHub developer profile</span></div>
                    </li>
                {% endif %}
            {% endif %}
            {% if "google" in socials %}
                {% if "google" in linked %}
                    <li>
                        <div class="name"><a class="warning" href="{{ url_for('admin.unlink_google', context = 'global', next = location) }}">Unlink Google account</a></div>
                        <div class="description"><span>You're currently linked to Google under <strong>{{ linked.google }}</strong></span></div>
                    </li>
                {% else %}
                    <li>
                        <div class="name"><a href="{{ url_for('admin.google', context = 'global', next = location) }}">Link Google account</a></div>
                        <div class="description"><span>Enable access to you Google account data and files</span></div>
                    </li>
                {% endif %}
            {% endif %}
            {% if "live" in socials %}
                {% if "live" in linked %}
                    <li>
                        <div class="name"><a class="warning" href="{{ url_for('admin.unlink_live', context = 'global', next = location) }}">Unlink Microsoft profile</a></div>
                        <div class="description"><span>You're currently linked to Microsoft under <strong>{{ linked.live }}</strong></span></div>
                    </li>
                {% else %}
                    <li>
                        <div class="name"><a href="{{ url_for('admin.live', context = 'global', next = location) }}">Link Microsoft Live account</a></div>
                        <div class="description"><span>Enable access to you Microsoft profile</span></div>
                    </li>
                {% endif %}
            {% endif %}
            {% if "twitter" in socials %}
                {% if "twitter" in linked %}
                    <li>
                        <div class="name"><a class="warning" href="{{ url_for('admin.unlink_twitter', context = 'global', next = location) }}">Unlink Twitter information</a></div>
                        <div class="description"><span>You're currently linked to Twitter under <strong>{{ linked.twitter }}</strong></span></div>
                    </li>
                {% else %}
                    <li>
                        <div class="name"><a href="{{ url_for('admin.twitter', context = 'global', next = location) }}">Link Twitter account</a></div>
                        <div class="description"><span>Enable access to you social Twitter information</span></div>
                    </li>
                {% endif %}
            {% endif %}
        </ul>
    {% else %}
        <div class="quote">No social accounts enabled and/or available.</div>
    {% endif %}
{% endblock %}
