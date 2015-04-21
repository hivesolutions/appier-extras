{% if "message" in request.params_s %}
    <div class="header-message {{ request.params_s.mtype }}">
        <div class="message-contents">{{ request.params_s.message }}</div>
    </div>
{% endif %}
