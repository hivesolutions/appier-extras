{% extends "email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("New account", True) }}{% endblock %}
{% block content %}
    <p>
        Hello {{ account.username }},<br/><br/>
        Thank you for joining {{ owner.description }}, from now on you have
        {{ owner.type }} like access the infra-structure.
    </p>
    {{ h2("Information") }}
    <p>
        Complete account information may be consulted
        {{ link(url_for("admin.show_entity", model = account.__class__._name(), _id = account._id, absolute = True), "here", False) }}.
    </p>
    <p>
        <strong>Username:</strong> <span>{{ account.username }}</span><br/>
        <strong>E-mail:</strong> <span>{{ account.email }}</span>
    </p>
    {{ h2("Support") }}
    {% set support_email = config.conf("SUPPORT_EMAIL")|default("no-reply@appier.hive.pt", True) %}
    <p>
        You have any problem? Our team is always ready to healp at any time.<br/>
        Send us an email to {{ link("mailto:" + support_email, support_email, False) }}.
    </p>
    <p>
        Thank you,<br/>
        The {{ owner.description }} team
    </p>
{% endblock %}
