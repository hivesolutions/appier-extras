{% for request in requests %}
    {{ request.method }} {{ request.path }}<br/>
{% endfor %}
