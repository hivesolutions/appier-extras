{% extends "admin/email/layout.html.tpl" %}
{% block title %}{{ title|default(subject, True)|default("Test email", True) }}{% endblock %}
{% block content %}
    <p>
        This is a simple test email for the {{ owner.description }} infra-structure.<br/>
        If you're reading this message the message has been correctly processed and delivered using <strong>{{ config.conf("SMTP_HOST") }}:{{ config.conf("SMTP_PORT", "25") }}</strong>.
    </p>
    <p>
        If you're receiving this message and it's marked as SPAM please contact your system administrator immediately.<br/>
        Please beware that the fact that you're receiving this email using your provider does not guarantee that other providers will receive the same email.
    </p>
    <p>
        For other questions regarding SMTP email sending please refer to you system administrator.
    </p>
    <p>
        An now for something completely different here comes a joke ...<br/>
        Wife: "How would you describe me?"<br/>
        Husband: "ABCDEFGHIJK." <br/>
        Wife: "What does that mean?"<br/>
        Husband: "Adorable, beautiful, cute, delightful, elegant, fashionable, gorgeous, and hot."<br/>
        Wife: "Aw, thank you, but what about IJK?" <br/>
        Husband: "I'm just kidding!"
    </p>
    <p>
        And now another joke...<br/>
        A teacher is teaching a class and she sees that Johnny isn't paying attention, so she asks him,
        "If there are three ducks sitting on a fence, and you shoot one, how many are left?"
        Johnny says, "None." The teacher asks, "Why?" Johnny says, "Because the shot scared them all off."
        The teacher says, "No, two, but I like how you're thinking." Johnny asks the teacher, "If you see
        three women walking out of an ice cream parlor, one is licking her ice cream, one is sucking her
        ice cream, and one is biting her ice cream, which one is married?" The teacher says,
        "The one sucking her ice cream." Johnny says, "No, the one with the wedding ring, but I like how
        you're thinking!"
    </p>
{% endblock %}
