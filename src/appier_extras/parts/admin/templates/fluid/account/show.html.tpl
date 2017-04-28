{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ account.username }}{% endblock %}
{% block name %}{{ account.username }}{% endblock %}
{% block style %}no-header{% endblock %}
{% block buttons %}
    {{ super() }}
    <ul class="drop-down" data-name="Operations">
        <li>
            {% if account.facebook_id %}
                <a href="{{ url_for('admin.unlink_facebook') }}">Unlink Facebook</a>
            {% else %}
                <a href="{{ url_for('admin.facebook') }}">Link Facebook</a>
            {% endif %}
        </li>
        <li>
            {% if account.github_login %}
                <a href="{{ url_for('admin.unlink_github') }}">Unlink GitHub</a>
            {% else %}
                <a href="{{ url_for('admin.github') }}">Link GitHub</a>
            {% endif %}
        </li>
        <li>
            {% if account.google_id %}
                <a href="{{ url_for('admin.unlink_google') }}">Unlink Google</a>
            {% else %}
                <a href="{{ url_for('admin.google') }}">Link Google</a>
            {% endif %}
        </li>
        <li>
            {% if account.live_id %}
                <a href="{{ url_for('admin.unlink_live') }}">Unlink Live</a>
            {% else %}
                <a href="{{ url_for('admin.live') }}">Link Live</a>
            {% endif %}
        </li>
        <li>
            {% if account.twitter_username %}
                <a href="{{ url_for('admin.unlink_twitter') }}">Unlink Twitter</a>
            {% else %}
                <a href="{{ url_for('admin.twitter') }}">Link Twitter</a>
            {% endif %}
        </li>
    </ul>
{% endblock %}
{% block content %}
    <div class="show-panel">
        <div class="panel-header">
            <img class="image no-border" src="{{ url_for('admin.avatar_account', username = session.username) }}" />
            <div class="details">
                <h2>{{ account.username }}</h2>
                <h3>{{ account.email }}</h3>
            </div>
            <div class="buttons">
                {{ self.buttons() }}
            </div>
        </div>
        <div class="panel-contents">
            <dl class="inline">
                <div class="item">
                    <dt>Username</dt>
                    <dd>{{ account.username }}</dd>
                </div>
                <div class="item">
                    <dt>Email</dt>
                    <dd>{{ account.email }}</dd>
                </div>
                <div class="item">
                    <dt>Last Login</dt>
                    <dd>{{ account.last_login_meta|default("-", True) }}</dd>
                </div>
                <div class="item">
                    <dt>Type</dt>
                    <dd><span class="tag">{{ appier.underscore_to_readable(account.type_meta, capitalize = True) }}</span></dd>
                </div>
                <div class="separator"></div>
                <div class="item">
                    <dt>Facebook ID</dt>
                    <dd>{{ account.facebook_id|default("-", True) }}</dd>
                </div>
                <div class="item">
                    <dt>GiHub Login</dt>
                    <dd>{{ account.github_login|default("-", True) }}</dd>
                </div>
                <div class="item">
                    <dt>Google ID</dt>
                    <dd>{{ account.google_id|default("-", True) }}</dd>
                </div>
                <div class="item">
                    <dt>Live ID</dt>
                    <dd>{{ account.live_id|default("-", True) }}</dd>
                </div>
                <div class="item">
                    <dt>Twitter Username</dt>
                    <dd>{{ account.twitter_username|default("-", True) }}</dd>
                </div>
            </dl>
        </div>
    </div>
{% endblock %}
