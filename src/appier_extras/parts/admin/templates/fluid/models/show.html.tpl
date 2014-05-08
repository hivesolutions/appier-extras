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
                    <th class="text-left">
                    	<a href="?{{ page.query(sorter = name) }}">{{ name }}</a>
                    </th>
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
    {% if page.count > 1 %}
	    <div class="pages">
	    	{% if page.index == 1 %}
	    		<span class="page disabled">&#8592;</span>
	    	{% else %}
	    		<a href="?{{ page.query(page = page.index - 1) }}" class="page">&#8592;</a>
	    	{% endif %}
			{% for index in range(page.count) %}
				{% set index = index + 1 %}
				{% if index == page.index %}
					<span class="page selected">{{ index}}</span>
				{% else %}
					<a href="?{{ page.query(page = index) }}" class="page">{{ index}}</a>
				{% endif %}
			{% endfor %}
			{% if page.index == page.count %}
				<span class="page disabled">&#8594;</span>
			{% else %}
				<a href="?{{ page.query(page = page.index + 1) }}" class="page">&#8594;</a>
			{% endif %}
		</div>
	{% endif %}
{% endblock %}
