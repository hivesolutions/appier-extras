{% extends "partials/admin.fluid.html.tpl" %}
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
                    <dd>{{ own.models_r|length }} models</dd>
                </div>
                <div class="item">
                    <dt>Routes</dt>
                    <dd>
                        <a href="{{ url_for('admin.list_routes') }}">{{ own.info().routes }} routes</a>
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
                        <a href="#">{{ request.session_c.count() }} sessions</a>
                    </dd>
                </div>
            </dl>
        </div>
    </div>
{% endblock %}
