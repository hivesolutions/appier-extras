{% extends "admin/layout.base.html.tpl" %}
{% block html %}
    {% include "admin/doctype.html.tpl" %}
    <head>
        {% block head %}
            {% include "admin/content_type.html.tpl" %}
            {% include "admin/includes.html.tpl" %}
            <title>{% block htitle %}{% endblock %}</title>
        {% endblock %}
    </head>
    <body class="ux wait-load fluid grey no-footer {{ sub_layout_r }} {{ style_r }} {{ style_flags }} {% block body_class %}{% endblock %}" data-id="admin">
        {% block extras %}
            {% include "admin/extras.html.tpl" %}
        {% endblock %}
        <div id="overlay" class="overlay"></div>
        <div id="bar" class="bar">
            {% include "admin/bar.html.tpl" %}
        </div>
        <div id="header" class="header">
            {% block header %}
                {% include "admin/header.html.tpl" %}
                <div class="side-links">
                    {% block links %}{% endblock %}
                </div>
            {% endblock %}
        </div>
        <div id="content" class="content {% block style %}{% endblock %}">
            <div class="content-header">
                <h1>{% block name %}{% endblock %}</h1>
                <div class="content-buttons">
                    {% block buttons %}{% endblock %}
                </div>
            </div>
            {% include "admin/message.html.tpl" %}
            <div class="content-container">
                {% block content %}{% endblock %}
            </div>
        </div>
        <div id="footer" class="footer">
            {% block footer %}
                {% include "admin/footer.html.tpl" %}
            {% endblock %}
        </div>
        <div id="windows" class="windows">
            {% block windows %}{% endblock %}
        </div>
    </body>
    {% include "admin/end_doctype.html.tpl" %}
{% endblock %}
