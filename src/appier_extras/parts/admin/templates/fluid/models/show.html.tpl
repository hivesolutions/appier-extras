{% extends "partials/layout.fluid.html.tpl" %}
{% block title %}{{ model._name() }}{% endblock %}
{% block name %}{{ model._name() }}{% endblock %}
{% block style %}no-padding{% endblock %}
{% block content %}
    <div class="filter" data-no_input="1">
        <table>
            <thead>
                <tr class="table-row table-header">
                	{% for name in model.definition() %}
                		<th class="text-left">{{ name }}</th>
                	{% endfor %}
                </tr>
            </thead>
 			<tbody class="filter-contents">
 				{% for entity in entities %}
 					<tr class="table-row">
		 				{% for name in model.definition() %}
		            		<td class="text-left">{{ entity[name] }}</td>
		            	{% endfor %}
 					</tr>
	            {% endfor %}
 			</tbody>
        </table>
    </div>
{% endblock %}
