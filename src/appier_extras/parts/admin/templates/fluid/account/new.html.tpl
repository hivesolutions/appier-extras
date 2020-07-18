{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Sign Up{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel {% if error %}login-panel-message{% endif %}">
        {% if owner.logo_url %}
            <img class="login-logo" src="{{ owner.logo_url }}" />
        {% else %}
            <h1>Sign up</h1>
        {% endif %}
        <h3>Create you new account on <strong>{{ owner.description }}</strong></h3>
        {% if error %}
            <div class="quote error">{{ error }}</div>
        {% endif %}
        <form action="{{ url_for('admin.create_account') }}" method="post" class="form">
            <input type="hidden" name="next" value="{{ next|default('', True) }}" />
            <div class="input">
                <input type="text" class="text-field full focus" name="username" value="{{ account.username }}"
                       placeholder="username" data-error="{{ errors.username }}" />
            </div>
            <div class="input">
                <input type="text" class="text-field full" name="email" value="{{ account.email }}"
                       placeholder="email" data-error="{{ errors.email }}"/>
            </div>
            <div class="input">
                <input type="password" class="text-field full" name="password" placeholder="password"
                        autocomplete="new-password" data-error="{{ errors.password }}" />
            </div>
            <div class="input">
                <input type="password" class="text-field full" name="password_confirm" placeholder="confirm password"
                       autocomplete="new-password" data-error="{{ errors.password_confirm }}" />
            </div>
            <div class="buttons">
                <span class="button medium button-color button-blue" data-submit="true">Sign up</span>
            </div>
            <div class="new">
                <span>or</span>
                <a href="{{ url_for('admin.login') }}">return to sign in</a>
            </div>
        </form>
    </div>
{% endblock %}
