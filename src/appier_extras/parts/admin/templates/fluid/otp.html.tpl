{% extends "admin/admin.simple.html.tpl" %}
{% block title %}OTP Login{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel {% if error %}login-panel-message{% endif %}">
        {% if owner.logo_url %}
            <img class="login-logo" src="{{ owner.logo_url }}" />
        {% else %}
            <h1>OTP Login</h1>
        {% endif %}
        <h3>Find you <strong>OTP code</strong> in the <strong>Auth App</strong></h3>
        {% if error %}
            <div class="quote error">{{ error }}</div>
        {% endif %}
        <form action="{{ url_for('admin.otp_login') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <div class="input">
                <input type="text" class="text-field full focus" name="otp" value="{{ otp }}"
                       placeholder="OTP code" />
            </div>
            <div class="buttons">
                <span class="button medium button-color button-blue" data-submit="true">
                    <span class="base">Login</span>
                    <span class="locked">Logging in...</span>
                </span>
            </div>
        </form>
    </div>
{% endblock %}
