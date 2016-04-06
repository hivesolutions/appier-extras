{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Operations{% endblock %}
{% block name %}Operations{% endblock %}
{% block content %}
    <ul class="sections-list">
        <li>
            <div class="name">
                <a class="link link-confirm warning" href="{{ url_for('admin.build_index', context = 'global', next = location) }}"
                    data-message="Are you really sure you want to build the search index ?">Build Search Index
                </a>
            </div>
            <div class="description"><span>Re-building the complete search index may take some time</span></div>
        </li>
        <li>
            <div class="name">
                <a class="link" href="{{ url_for('admin.test_email', context = 'global', next = location) }}">Send test email</a>
            </div>
            <div class="description"><span>Sending this email is going to use loaded SMTP configuration</span></div>
        </li>
        <li>
            <div class="name">
                <a class="link" href="{{ url_for('admin.test_event', context = 'global', next = location) }}">Trigger test event</a>
            </div>
            <div class="description"><span>All handlers for the event are going to be triggered</span></div>
        </li>
    </ul>
{% endblock %}
