{% extends "partials/layout.fluid.html.tpl" %}
{% block title %}{{ model._name() }} TO BE CHANGED{% endblock %}
{% block name %}{{ model._name() }} TO BE CHANGED{% endblock %}
{% block buttons %}
    {{ super() }}
    <div class="button button-color button-grey" data-link="#">Edit</div>
{% endblock %}
{% block content %}
    <div class="show-panel">
        <div class="panel-contents simple">
            <dl class="inline">
                {% for name in model.show_names() %}
                    <div class="item">
                        <dt>{{ name }}</dt>
                        <dd>{{ out(entity, name) }}</dd>
                    </div>
                {% endfor %}
            </dl>
        </div>
    </div>
{% endblock %}
