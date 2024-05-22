{% extends "admin/admin.simple.html.tpl" %}
{% block title %}OTP Register{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel {% if error %}login-panel-message{% endif %}">
        {% if owner.logo_url %}
            <img class="login-logo" src="{{ owner.logo_url }}" />
        {% else %}
            <h1>OTP</h1>
        {% endif %}
        <h3>Registering OTP</h3>
        {% if error %}
            <div class="quote error">{{ error }}</div>
        {% endif %}
        <form>
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <img class="otp-qrcode" src="{{ url_for('admin.otp_qrcode') }}" />
        </form>
    </div>
{% endblock %}
