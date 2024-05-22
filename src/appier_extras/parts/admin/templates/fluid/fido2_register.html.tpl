{% extends "admin/admin.simple.html.tpl" %}
{% block title %}FIDO2 Registration{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel {% if error %}login-panel-message{% endif %}">
        {% if owner.logo_url %}
            <img class="login-logo" src="{{ owner.logo_url }}" />
        {% else %}
            <h1>Passkey Registration</h1>
        {% endif %}
        <h3>Follow instructions to register a new key</h3>
        {% if error %}
            <div class="quote error">{{ error }}</div>
        {% endif %}
        <form action="{{ url_for('admin.fido2_register_do') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <input type="hidden" name="credential" value="" />
            <div class="fido2-register">{{ registration_data }}</div>
        </form>
    </div>
{% endblock %}
