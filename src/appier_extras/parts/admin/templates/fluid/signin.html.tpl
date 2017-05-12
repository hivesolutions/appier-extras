{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Login{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel {% if error %}login-panel-message{% endif %}">
        {% if owner.logo_url %}
            <img class="login-logo" src="{{ owner.logo_url }}" />
        {% else %}
            <h1>Login</h1>
        {% endif %}
        <h3>Sign in to continue to <strong>{{ owner.description }}</strong></h3>
        {% if error %}
            <div class="quote error">{{ error }}</div>
        {% endif %}
        <form action="{{ url_for('admin.login') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <div class="input">
                <input type="text" class="text-field full focus" name="username" value="{{ username }}"
                       placeholder="username" />
            </div>
            <div class="input">
                <input type="password" class="text-field full" name="password" placeholder="password" />
            </div>
            <div class="forgot">
                <a href="{{ url_for('admin.recover') }}">Forgot your password?</a>
            </div>
            <div class="buttons">
                <span class="button medium button-color button-blue" data-submit="true">Login</span>
            </div>
            {% if owner.admin_open %}
                <div class="new">
                    <span>or</span>
                    <a href="{{ url_for('admin.new_account') }}">create new account</a>
                </div>
            {% endif %}
        </form>
    </div>
    {% if socials %}
        <div class="login-footer">
            Sign in with
            {% if socials|length == 1 %}
                <a class="no-async" href="{{ url_for('admin.' + socials[0], next = next|default('', True)) }}">{{ socials[0]|capitalize }}</a>
            {% else %}
                {% for social in socials %}{% if loop.first %}{% elif loop.last %} or {% else %}, {% endif %}<a class="no-async" href="{{ url_for('admin.' + social, next = next|default('', True)) }}">{{ social|capitalize }}</a>{% endfor %}
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
