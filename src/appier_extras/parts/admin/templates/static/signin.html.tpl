{% extends "partials/layout.simple.html.tpl" %}
{% block content %}
    <div class="login-panel">
        <h1>Login</h1>
        <h3>Sign in to continue to webook</h3>
        <div class="quote error">
            {{ error }}
        </div>
        <form action="{{ url_for('base.login') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <div class="input">
                <input type="text" class="small focus" name="username" value="{{ username }}" placeholder="username" />
            </div>
            <div class="input">
                <input type="password" class="small" name="password" placeholder="password"  />
            </div>
            <div class="forgot">
                <a href="#">Forgot your password?</a>
            </div>
            <div class="buttons">
                <span class="button medium button-color button-blue" data-submit="true">Login</span>
            </div>
            <div class="new">
                <span>or</span>
                <a href="{{ url_for('account.new') }}">create new account</a>
            </div>
        </form>
    </div>
{% endblock %}
