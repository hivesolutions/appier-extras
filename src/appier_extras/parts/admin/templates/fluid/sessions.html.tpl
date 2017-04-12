{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Sessions{% endblock %}
{% block name %}Sessions{% endblock %}
{% block style %}no-padding{% endblock %}
{% block buttons %}
    {{ super() }}
    <div class="button button-color button-red button-confirm"
         data-message="Do you really want to [delete all sessions] ?"
         data-link="{{ url_for('admin.empty_sessions') }}">Empty</div>
{% endblock %}
{% block content %}
    <table class="filter no-fixed" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                <th class="text-left">Session ID</th>
                <th class="text-left">Creation</th>
                <th class="text-left">Expiration</th>
                <th class="text-left">IP Addresss</th>
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for sid in sessions %}
                {% set _session = sessions[sid] %}
                {% if _session.sid %}
                    <tr class="table-row">
                        <td class="text-left">
                            <strong>
                                <a href="{{ url_for('admin.show_session', sid = _session.sid) }}">{{ _session.sid }}</a>
                            </strong>
                            {% if _session.sid == session.sid %}
                                <strong>(current)</strong>
                            {% endif %}
                        </td>
                        <td class="text-left">{{ date_time(_session.create, format = "%d %b %Y %H:%M:%S") }}</td>
                        <td class="text-left">{{ date_time(_session.expire, format = "%d %b %Y %H:%M:%S") }}</td>
                        <td class="text-left">{{ _session.address }}</td>
                    </tr>
                {% endif %}
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
