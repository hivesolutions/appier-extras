{% extends "partials/admin.simple.html.tpl" %}
{% block title %}Recover{% endblock %}
{% block content %}
    <div class="login-panel">
        <h1>Recover password</h1>
        <h4>You'll receive an email for account recovery</h4>
        <div class="new">
            <a href="{{ url_for('admin.index') }}">return to {{ owner.name }}</a>
        </div>
    </div>
{% endblock %}
