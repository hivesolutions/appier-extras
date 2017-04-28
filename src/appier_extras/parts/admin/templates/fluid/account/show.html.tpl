{% extends "admin/admin.fluid.html.tpl" %}
{% block title %}{{ account.username }}{% endblock %}
{% block name %}{{ account.username }}{% endblock %}
{% block style %}no-header{% endblock %}
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
                    <dd>{{ account.last_login_meta }}</dd>
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
                    <dt>Twitter Username</dt>
                    <dd>{{ account.twitter_username|default("-", True) }}</dd>
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
                    <dt>GiHub Login</dt>
                    <dd>{{ account.github_login|default("-", True) }}</dd>
                </div>
            </dl>
        </div>
    </div>
{% endblock %}
