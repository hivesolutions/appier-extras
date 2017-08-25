{% if "message" in request.params_s %}
    <div class="header-message {{ request.params_s.mtype }}">
        <div class="message-contents">{{ owner.field("message")|default("", True) }}</div>
    </div>
{% endif %}
