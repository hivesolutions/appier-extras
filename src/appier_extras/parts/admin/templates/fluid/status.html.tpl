{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}Status{% endblock %}
{% block name %}Status{% endblock %}
{% block style %}no-header{% endblock %}
{% block content %}
    <div class="show-panel">
        <div class="panel-header">
            <img class="image square no-border" src="{{ url_for('admin', filename = 'images/logo_96.png') }}" />
            <div class="details">
                <h2>{{ owner.description }}</h2>
            </div>
            <div class="buttons">
                {{ self.buttons() }}
            </div>
        </div>
        <div class="panel-contents">
            <dl class="inline">
                <div class="item">
                    <dt>Name</dt>
                    <dd>{{ own.info().name }}</dd>
                </div>
                <div class="item">
                    <dt>Instance</dt>
                    <dd>{{ own.info().instance|default("global", True) }}</dd>
                </div>
                <div class="item">
                    <dt>Uptime</dt>
                    <dd>{{ own.info().uptime }}</dd>
                </div>
                <div class="item">
                    <dt>Platform</dt>
                    <dd>{{ own.info().platform }}</dd>
                </div>
                <div class="item">
                    <dt>Server</dt>
                    <dd>{{ own.info().server }}</dd>
                </div>
                <div class="item">
                    <dt>Appier</dt>
                    <dd>{{ own.info().appier }}</dd>
                </div>
                <div class="item">
                    <dt>Models</dt>
                    <dd>{{ own._attached(own.models_r)|length }} models</dd>
                </div>
                <div class="item">
                    <dt>Routes</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_routes') }}">{{ own.info().routes }} routes</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Configuration</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_configs') }}">{{ own.info().configs }} items</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Libraries</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_libraries') }}">{{ own.info().libraries|length }} libraries</a>
                    </dd>
                </div>
                <div class="separator"></div>
                <div class="item">
                    <dt>Session class</dt>
                    <dd>{{ request.session_c.__name__ }}</dd>
                </div>
                <div class="item">
                    <dt>Session count</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_sessions') }}">{{ request.session_c.count() }} sessions</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Counters</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_counters') }}">{{ own._counters().count() }} counters</a>
                    </dd>
                </div>
                <div class="item">
                    <dt>Adapter class</dt>
                    <dd>{{ own.adapter.__class__.__name__ }}</dd>
                </div>
                <div class="item">
                    <dt>Manager class</dt>
                    <dd>{{ own.manager.__class__.__name__ }}</dd>
                </div>
                {% if appier.Git.is_git() %}
                    <div class="separator"></div>
                    <div class="item">
                        <dt>Branch</dt>
                        <dd>{{ appier.Git.get_branch() }}</dd>
                    </div>
                    <div class="item">
                        <dt>Commit</dt>
                        <dd>{{ appier.Git.get_commit() }}</dd>
                    </div>
                    <div class="item">
                        <dt>Origin</dt>
                        <dd>{{ appier.Git.get_origin() }}</dd>
                    </div>
                {% endif %}
            </dl>
        </div>
    </div>
{% endblock %}
