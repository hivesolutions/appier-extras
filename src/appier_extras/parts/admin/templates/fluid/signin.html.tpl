{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Login{% endblock %}
{% block content %}
    <div class="login-panel">
        <h1>Login</h1>
        <h3>Sign in to continue to <strong>{{ owner.description }}</strong></h3>
        <div class="quote error">
            {{ error }}
        </div>
        <form action="{{ url_for('admin.login') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <div class="input">
                <input type="text" class="text-field small focus" name="username" value="{{ username }}"
                       placeholder="username" />
            </div>
            <div class="input">
                <input type="password" class="text-field small" name="password" placeholder="password" />
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
                <a href="{{ url_for('admin.' + socials[0], next = next|default('', True)) }}">{{ socials[0] }}</a>
            {% else %}
                {% for social in socials %}{% if loop.first%}{% elif loop.last %} or {% else %}, {%endif%}<a href="{{ url_for('admin.' + social, next = next|default('', True)) }}">{{ social|capitalize }}</a>{% endfor %}
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
