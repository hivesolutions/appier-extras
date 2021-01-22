{% extends owner.admin_email_layout %}
{% block title %}{{ title|default(subject, True)|default("New account", True) }}{% endblock %}
{% block content %}
    {% set account = account if account else {} %}
    <p>Hello <strong>{{ account.username }}</strong>,</p>
    <p>
        Thank you for joining {{ owner.description }}, you now have access with
        <strong>"{{ account.type_meta }}"</strong> privileges.<br/>
        Feel free to login with your account and explore all the features {{ owner.description }} has to offer.
    </p>
    {{ h2("Information") }}
    {% if owner.admin_email_account_new_link %}
        {% set account_url = url_for("admin.show_entity", model = account.__class__._under(), _id = account._id, absolute = True) %}
        {% set account_url = config.conf("ACCOUNT_URL")|default(account_url, True) %}
        {% set account_url = config.conf("NEW_ACCOUNT_URL")|default(account_url, True) %}
        <p>
            You can view all the information about your account by clicking {{ link(account_url, "here", False) }}.
        </p>
    {% endif %}
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
