{% extends "partials/admin.fluid.html.tpl" %}
{% block title %}{{ entity }}{% endblock %}
{% block name %}{{ entity }}{% endblock %}
{% block buttons %}
    {{ super() }}
    <div class="button button-color button-grey"
         data-link="{{ url_for('admin.edit_entity', model = model._name(), _id = entity._id) }}">Edit</div>
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
