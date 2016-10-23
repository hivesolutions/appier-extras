{% extends "admin/layout.base.html.tpl" %}
{% block html %}
    {% include "admin/doctype.html.tpl" %}
    <head>
        {% block head %}
            {% include "admin/content_type.html.tpl" %}
            {% include "admin/includes.html.tpl" %}
            {% include "admin/meta.html.tpl" %}
            <title>{% block htitle %}{% endblock %}</title>
        {% endblock %}
    </head>
    <body class="ux wait-load simple {{ sub_layout_r }} {{ style_r }} {{ style_flags }} {% block body_class %}{% endblock %}" data-id="admin">
        <div id="overlay" class="overlay"></div>
        <div id="header" class="header">
            {% block header %}
                {% include "admin/header.html.tpl" %}
                <h1>{% block name %}{% endblock %}</h1>
            {% endblock %}
        </div>
        <div id="content" class="content {% block style %}{% endblock %}">{% block content %}{% endblock %}</div>
        <div id="footer" class="footer">
            {% block footer %}
                {% include "admin/footer.html.tpl" %}
            {% endblock %}
        </div>
    </body>
    {% include "admin/end_doctype.html.tpl" %}
{% endblock %}
