{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ account.username }}{% endblock %}
{% block name %}{{ account.username }}{% endblock %}
{% block style %}no-header{% endblock %}
{% block buttons %}
    {{ super() }}
    <ul class="drop-down drop-down-left" data-name="Operations">
        <li>
            <a href="{{ url_for('admin.otp_register', next = location_f) }}">Register OTP</a>
        </li>
        <li>
            <a href="{{ url_for('admin.fido2_register', next = location_f) }}">Register FIDO2</a>
        </li>
        {% if own.has_facebook() %}
            <li>
                {% if account.facebook_id %}
                    <a href="{{ url_for('admin.unset_facebook', next = location_f) }}">Unlink Facebook</a>
                {% else %}
                    <a href="{{ url_for('admin.facebook', next = location_f) }}">Link Facebook</a>
                {% endif %}
            </li>
        {% endif %}
        {% if own.has_github() %}
            <li>
                {% if account.github_login %}
                    <a href="{{ url_for('admin.unset_github', next = location_f) }}">Unlink GitHub</a>
                {% else %}
                    <a href="{{ url_for('admin.github', next = location_f) }}">Link GitHub</a>
                {% endif %}
            </li>
        {% endif %}
        {% if own.has_google() %}
            <li>
                {% if account.google_id %}
                    <a href="{{ url_for('admin.unset_google', next = location_f) }}">Unlink Google</a>
                {% else %}
                    <a href="{{ url_for('admin.google', next = location_f) }}">Link Google</a>
                {% endif %}
            </li>
        {% endif %}
        {% if own.has_live() %}
            <li>
                {% if account.live_id %}
                    <a href="{{ url_for('admin.unset_live', next = location_f) }}">Unlink Microsoft</a>
                {% else %}
                    <a href="{{ url_for('admin.live', next = location_f) }}">Link Microsoft</a>
                {% endif %}
            </li>
        {% endif %}
        {% if own.has_twitter() %}
            <li>
                {% if account.twitter_username %}
                    <a href="{{ url_for('admin.unset_twitter', next = location_f) }}">Unlink Twitter</a>
                {% else %}
                    <a href="{{ url_for('admin.twitter', next = location_f) }}">Link Twitter</a>
                {% endif %}
            </li>
        {% endif %}
    </ul>
{% endblock %}
{% block content %}
    <div class="show-panel">
        <div class="panel-header">
            <img class="image no-border" src="{{ url_for('admin.avatar_account', username = session.username) }}" />
            <div class="buttons">
                {{ self.buttons() }}
            </div>
            <div class="details">
                <h2>{{ account.username }}</h2>
                <h3>{{ account.email }}</h3>
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
                <div class="item">
                    <dt>OTP Enabled</dt>
                    <dd><span class="tag {% if account.otp_enabled %}green{% else %}red{% endif %}">{{ account.otp_enabled }}</span></dd>
                </div>
                <div class="item">
                    <dt>FIDO2 Enabled</dt>
                    <dd><span class="tag {% if account.fido2_enabled %}green{% else %}red{% endif %}">{{ account.fido2_enabled }}</span></dd>
                </div>
                <div class="separator"></div>
                {% if own.has_facebook() %}
                    <div class="item">
                        <dt>Facebook ID</dt>
                        <dd>{{ account.facebook_id|default("-", True) }}</dd>
                    </div>
                {% endif %}
                {% if own.has_github() %}
                    <div class="item">
                        <dt>GitHub Login</dt>
                        <dd>{{ account.github_login|default("-", True) }}</dd>
                    </div>
                {% endif %}
                {% if own.has_google() %}
                    <div class="item">
                        <dt>Google ID</dt>
                        <dd>{{ account.google_id|default("-", True) }}</dd>
                    </div>
                {% endif %}
                {% if own.has_live() %}
                    <div class="item">
                        <dt>Live ID</dt>
                        <dd>{{ account.live_id|default("-", True) }}</dd>
                    </div>
                {% endif %}
                {% if own.has_twitter() %}
                    <div class="item">
                        <dt>Twitter Username</dt>
                        <dd>{{ account.twitter_username|default("-", True) }}</dd>
                    </div>
                {% endif %}
            </dl>
        </div>
    </div>
{% endblock %}
