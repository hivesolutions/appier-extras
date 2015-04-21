{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Recover{% endblock %}
{% block content %}
    <div class="login-panel">
        <h1>Recover password</h1>
        <h3>Use your username or email</h3>
        <div class="quote error">
            {{ error }}
        </div>
        <form action="{{ url_for('admin.recover_do') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <div class="input">
                <input type="text" class="text-field small focus" name="identifier"
                       value="{{ identifier }}" placeholder="username or email" />
            </div>
            <div class="buttons">
                <span class="button medium button-color button-blue" data-submit="true">Recover</span>
            </div>
            <div class="new">
                <span>or</span>
                <a href="{{ url_for('admin.login') }}">return to sign in</a>
            </div>
        </form>
    </div>
{% endblock %}
