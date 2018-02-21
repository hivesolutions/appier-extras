{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Requests{% endblock %}
{% block name %}Requests{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <div class="listers">
        <div class="cards lister">
            {% for request in requests %}
                <div class="card">
                    <dl>
                        <div class="item">
                            <dt>Method</dt>
                            <dd>
                                <span class="tag {{ request.method|lower }}">{{ request.method }}</span>
                            </dd>
                        </div>
                        <div class="item">
                            <dt>Path</dt>
                            <dd>
                                <a href="{{ url_for('diag.show_request', id = request.id) }}">{{ request.path }}</a>
                            </dd>
                        </div>
                        <div class="item">
                            <dt>Status</dt>
                            <dd>{{ request.code }}</dd>
                        </div>
                        <div class="item">
                            <dt>Address</dt>
                            <dd>{{ request.address }}</dd>
                        </div>
                        <div class="item">
                            <dt>Date</dt>
                            <dd>{{ request.timestamp_d }}</dd>
                        </div>
                        <div class="item">
                            <dt>Browser</dt>
                            <dd>{{ request.browser }}</dd>
                        </div>
                    </dl>
                </div>
            {% endfor %}
        </div>
        <table class="filter lister" data-no_input="1" data-size="{{ page.size }}"
               data-total="{{ page.total }}" data-pages="{{ page.count }}">
            <thead>
                <tr class="table-row table-header">
                    {% for name in ("method", "path", "code", "address", "date", "browser") %}
                        {% set description = model.to_description(name) %}
                        {% if name == page.sorter %}
                            <th class="text-left direction {{ page.direction }}">
                                <a href="{{ page.query(sorter = name) }}">{{ description }}</a>
                            </th>
                        {% else %}
                            <th class="text-left">
                                <a href="{{ page.query(sorter = name) }}">{{ description }}</a>
                            </th>
                        {% endif %}
                    {% endfor %}
                </tr>
            </thead>
            <tbody class="filter-contents">
                {% for request in requests %}
                    <tr class="table-row">
                        <td class="text-left">
                            <span class="tag {{ request.method|lower }}">{{ request.method }}</span>
                        </td>
                        <td class="text-left">
                            <a href="{{ url_for('diag.show_request', id = request.id) }}">{{ request.path }}</a>
                        </td>
                        <td class="text-left">{{ request.code }}</td>
                        <td class="text-left">{{ request.address }}</td>
                        <td class="text-left">{{ request.timestamp_d }}</td>
                        <td class="text-left">{{ request.browser }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% if page.count > 1 %}
        {{ paging(page.index, page.count, caller = page.query) }}
    {% endif %}
{% endblock %}
