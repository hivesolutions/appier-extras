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
    </ul>
{% endblock %}
