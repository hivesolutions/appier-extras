{% extends owner.admin_layout_static %}
{% block htitle %}{{ owner.description }} / {% block title %}{% endblock %}{% endblock %}
{% block links %}
    {% for model in models %}
        <a href="#">{{ model._readable() }}</a>
    {% endfor %}
{% endblock %}
