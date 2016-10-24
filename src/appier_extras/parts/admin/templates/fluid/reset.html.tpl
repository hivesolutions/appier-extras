{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Recover{% endblock %}
{% block content %}
    <div class="login-panel">
        <h1>Reset password</h1>
        <h3>Define a new password for you account</h3>
        <div class="quote error">
            {{ error|default("", True) }}
        </div>
        <form action="{{ url_for('admin.reset_do') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <input type="hidden" name="reset_token" value="{{ reset_token }}" />
            <div class="input">
                <input type="password" class="text-field full focus" name="password"
                       value="{{ password }}" placeholder="password" />
            </div>
            <div class="input">
                <input type="password" class="text-field full" name="password_confirm"
                       value="{{ password_confirm }}" placeholder="confirm password" />
            </div>
            <div class="buttons">
                <span class="button medium button-color button-blue" data-submit="true">Reset</span>
            </div>
        </form>
    </div>
{% endblock %}
