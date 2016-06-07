{% extends "admin/email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("New account", True) }}{% endblock %}
{% block content %}
    <p>Hello <strong>{{ account.username }}</strong>,</p>
    <p>
        Thank you for joining {{ owner.description }}, you now have access with
        <strong>"{{ account.type_meta }}"</strong> privileges.<br/>
        Feel free to login with your account and explore all the features {{ owner.description }} has to offer.
    </p>
    {{ h2("Information") }}
    <p>
        You can view all the information about your account by clicking
        {{ link(url_for("admin.show_entity", model = account.__class__._name(), _id = account._id, absolute = True), "here", False) }}.
    </p>
    <p>
        <strong>Username:</strong> <span>{{ account.username }}</span><br/>
        <strong>E-mail:</strong> <span>{{ link("mailto:" + account.email, account.email, False) }}</span>
        {% if account_password %}
            <br/><strong>Password:</strong> <span>{{ account_password }}</span>
        {% endif %}
    </p>
    {% if not account.enabled and account.confirmation_token %}
        {{ h2("Confirmation") }}
        <p>
            Please visit this address to activate your account:
            {{ link(url_for("admin.confirm", confirmation_token = account.confirmation_token, absolute = True), "Confirm Account", False) }}.
        </p>
    {% endif %}
    {{ h2("Support") }}
    {% set support_email = config.conf("SUPPORT_EMAIL")|default("no-reply@appier.hive.pt", True) %}
    <p>
        Are you having any trouble? We are here to help.<br/>
        Feel free to send us an email to {{ link("mailto:" + support_email, support_email, False) }} and we'll get in touch.
    </p>
    <p>
        Thank you,<br/>
        The {{ owner.description }} team
    </p>
{% endblock %}
