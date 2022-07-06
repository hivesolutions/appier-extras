{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Recover{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
{% set param_next = request.args.get("next")[0] %}
{% set url_signin = url_for("admin.login", next = param_next) if param_next else url_for("admin.login") %}
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
                <span class="button medium button-color button-blue" data-submit="true">
                    <span class="base">Recover</span>
                    <span class="locked">Recovering...</span>
                </span>
            </div>
            <div class="new">
                <span>or</span>
                <a href="{{ url_signin }}">return to sign in</a>
            </div>
        </form>
    </div>
{% endblock %}
