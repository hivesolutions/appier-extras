{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Recover{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel {% if error %}login-panel-message{% endif %}">
        <h1>Recover password</h1>
        <h3>Use your username or email</h3>
        {% if error %}
            <div class="quote error">{{ error }}</div>
        {% endif %}
        <form action="{{ url_for('admin.recover_do') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <div class="input">
                <input type="text" class="text-field full focus" name="identifier"
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
