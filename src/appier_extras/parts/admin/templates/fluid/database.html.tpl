{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Database{% endblock %}
{% block name %}Database{% endblock %}
{% block content %}
    <ul class="sections-list">
        <li>
            <div class="name"><a href="{{ url_for('admin.database_import') }}">Import</a></div>
            <div class="description"><span>Import data from a database file</span></div>
        </li>
        <li>
            <div class="name"><a class="no-async" href="{{ url_for('admin.database_export') }}">Export</a></div>
            <div class="description"><span>Export your current database into an external file</span></div>
        </li>
        <li>
            <div class="name">
                <a class="link link-confirm warning" href="{{ url_for('admin.database_reset') }}"
                   data-message="Are you really sure you want to reset the database ?">Reset
                </a>
            </div>
            <div class="description"><span>Reset the database this as extremly dangerous operation</span></div>
        </li>
    </ul>
{% endblock %}
