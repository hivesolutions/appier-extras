{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Requests{% endblock %}
{% block name %}Requests{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    {% call(item, page) paging_listers(
        request,
        model,
        page,
        names = ("method", "path", "code", "address", "date", "browser")
    ) %}
        {% if page %}
            <div class="item">
                <dt>Method</dt>
                <dd>
                    <span class="tag {{ item.method|lower }}">{{ item.method }}</span>
                </dd>
            </div>
            <div class="item">
                <dt>Path</dt>
                <dd>
                    <a href="{{ url_for('diag.show_request', id = item.id) }}">{{ item.path }}</a>
                </dd>
            </div>
            <div class="item">
                <dt>Status</dt>
                <dd>{{ item.code }}</dd>
            </div>
            <div class="item">
                <dt>Address</dt>
                <dd>{{ item.address }}</dd>
            </div>
            <div class="item">
                <dt>Date</dt>
                <dd>{{ item.timestamp_d }}</dd>
            </div>
            <div class="item">
                <dt>Browser</dt>
                <dd>{{ item.browser }}</dd>
            </div>
        {% else %}
            <td class="text-left">
                <span class="tag {{ item.method|lower }}">{{ item.method }}</span>
            </td>
            <td class="text-left">
                <a href="{{ url_for('diag.show_request', id = item.id) }}">{{ item.path }}</a>
            </td>
            <td class="text-left">{{ item.code }}</td>
            <td class="text-left">{{ item.address }}</td>
            <td class="text-left">{{ item.timestamp_d }}</td>
            <td class="text-left">{{ item.browser }}</td>
        {% endif %}
    {% endcall %}
{% endblock %}
