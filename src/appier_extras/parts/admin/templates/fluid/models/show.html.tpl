{% extends "partials/layout.fluid.html.tpl" %}
{% block title %}{{ model._name() }}{% endblock %}
{% block name %}{{ model._name() }}{% endblock %}
{% block style %}no-padding{% endblock %}
{% block buttons %}
    {{ super() }}
    <div class="button button-color button-grey"
         data-link="{{ url_for('admin.new_entity', model = model._name()) }}">New</div>
{% endblock %}
{% block content %}
    <table class="filter" data-no_input="1">
        <thead>
            <tr class="table-row table-header">
                {% for name in model.list_names() %}
                    <th class="text-left">{{ name }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody class="filter-contents">
            {% for entity in entities %}
                <tr class="table-row">
                    {% for name in model.list_names() %}
                        <td class="text-left">{{ out(entity, name) }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
