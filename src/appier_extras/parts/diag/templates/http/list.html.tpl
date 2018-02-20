{% for request in requests %}
    {{ request.method }} {{ request.path }} {{ request.timestamp_d }}<br/>
{% endfor %}
