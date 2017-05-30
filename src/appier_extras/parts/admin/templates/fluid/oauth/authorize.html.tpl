{% extends "admin/admin.simple.html.tpl" %}
{% block title %}Authorize{% endblock %}
{% block body_style %}{{ super() }} {% if background %}background:url({{ background }});{% endif %}{% endblock %}
{% block content %}
    <div class="login-panel {% if error %}login-panel-message{% endif %}">
        {% if owner.logo_url %}
            <img class="login-logo" src="{{ owner.logo_url }}" />
        {% else %}
            <h1>Authorize</h1>
        {% endif %}
        <h3>Allow account access from <strong>{{ oauth_client.name }}</strong></h3>
        {% if error %}
            <div class="quote error">{{ error }}</div>
        {% endif %}
        <form action="{{ url_for('admin.do_oauth_authorize') }}" method="post" class="form">
            <input type="hidden" name="client_id" value="{{ client_id }}" />
            <input type="hidden" name="redirect_uri" value="{{ redirect_uri }}" />
            <input type="hidden" name="scope" value="{{ scope }}" />
            <input type="hidden" name="response_type" value="{{ response_type }}" />
            <input type="hidden" name="state" value="{{ state }}" />
            <div class="tokens">
                {% for token in tokens %}
                    <div class="token">{{ token }}</div>
                {% endfor %}
            </div>
            <div class="buttons">
                <span class="button medium button-color button-blue" data-submit="true">Allow</span>
                <span class="button medium button-color button-red"
                      data-link="{{ url_for('admin.oauth_deny', redirect_uri = redirect_uri) }}">Deny</span>
            </div>
        </form>
    </div>
{% endblock %}
