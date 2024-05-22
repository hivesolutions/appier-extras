{% extends "admin/admin.simple.html.tpl" %}
{% block title %}OTP Registration{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel {% if error %}login-panel-message{% endif %}">
        {% if owner.logo_url %}
            <img class="login-logo" src="{{ owner.logo_url }}" />
        {% else %}
            <h1>OTP Registration</h1>
        {% endif %}
        <h3>Use the <strong>QR Code</strong> in your <strong>Auth App</strong></h3>
        {% if error %}
            <div class="quote error">{{ error }}</div>
        {% endif %}
        <form action="{{ next|default('', True) }}" method="get" class="form">
            <img class="otp-qrcode" src="{{ url_for('admin.otp_qrcode') }}" />
            <div class="buttons">
                <span class="button medium button-color button-blue" data-submit="true">
                    <span class="base">Return</span>
                    <span class="locked">Returning...</span>
                </span>
            </div>
        </form>
    </div>
{% endblock %}
