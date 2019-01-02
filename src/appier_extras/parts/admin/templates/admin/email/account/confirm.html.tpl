{% extends owner.admin_email_layout %}
{% block title %}{{ title|default(subject, True)|default("Confirm account", True) }}{% endblock %}
{% block content %}
    {% set account = account if account else {} %}
    <p>Hello <strong>{{ account.username }}</strong>,</p>
    <p>
        You're receiving this email because you account has just
        been confirmed. You can now start using your account.
    </p>
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
