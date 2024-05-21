// Hive Appier Framework
// Copyright (c) 2008-2024 Hive Solutions Lda.
//
// This file is part of Hive Appier Framework.
//
// Hive Appier Framework is free software: you can redistribute it and/or modify
// it under the terms of the Apache License as published by the Apache
// Foundation, either version 2.0 of the License, or (at your option) any
// later version.
//
// Hive Appier Framework is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// Apache License for more details.
//
// You should have received a copy of the Apache License along with
// Hive Appier Framework. If not, see <http://www.apache.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2024 Hive Solutions Lda.
// __license__   = Apache License, Version 2.0

(function(jQuery) {
    jQuery.fn.uapply = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the reference to the header message elements contained
        // in the matched object and starts the proper message plugin in it
        var message = jQuery(".header-message", matchedObject);
        message.umessage();

        // retrieves the reference to the FIDO2 Auth element and registers it
        // for the base FIDO2 Auth plugin so that it's properly initialized
        var fido2 = jQuery(".fido2-auth", matchedObject);
        fido2.ufido2auth();

        // retrieves the reference to the FIDO2 Register element and registers it
        // for the base FIDO2 Register plugin so that it's properly initialized
        var fido2 = jQuery(".fido2-register", matchedObject);
        fido2.ufido2register();
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.umessage = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the contents part of the message container as it's
        // going to be used in the registration of the click handler
        var messageContents = jQuery(".message-contents", matchedObject);
        var timeout = messageContents.attr("data-timeout") || 7500;
        timeout = parseInt(timeout);

        // sets the timeout for the fade out operation of the matched
        // object that is going to be used to auto-hide the message
        setTimeout(function() {
            matchedObject.addClass("invisible");
        }, timeout);

        // registers for the click operation for the message contents
        // so that the associated header message is hidden
        messageContents.click(function() {
            var element = jQuery(this);
            var message = element.parents(".header-message");
            message.addClass("invisible");
        });
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.ufido2auth = function(options) {
        var matchedObject = this;
        matchedObject.each(function(index, element) {
            var _element = jQuery(element);
            var form = _element.parents("form");

            var authData = JSON.parse(_element.text());

            authData.publicKey.challenge = base64ToUint8Array(authData.publicKey.challenge);
            authData.publicKey.allowCredentials.forEach(function(credential) {
                credential.id = base64ToUint8Array(credential.id);
            });

            navigator.credentials.get(authData).then(function(response) {
                var responseInput = jQuery("input[type=\"hidden\"][name=\"response\"]",
                    form);
                var serializedResponse = serializePublicKeyCredential(response);
                responseInput.uxvalue(JSON.stringify(serializedResponse));
                form.submit();
            });
        });
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.ufido2register = function(options) {
        var matchedObject = this;
        matchedObject.each(function(index, element) {
            var _element = jQuery(element);
            var form = _element.parents("form");

            var registrationData = JSON.parse(_element.text());

            registrationData.publicKey.user.id = base64ToUint8Array(registrationData.publicKey.user.id);
            registrationData.publicKey.challenge = base64ToUint8Array(registrationData.publicKey.challenge);

            navigator.credentials.create(registrationData).then(function(credential) {
                var credentialInput = jQuery("input[type=\"hidden\"][name=\"credential\"]",
                    form);
                var serializedCredential = serializePublicKeyCredential(credential);
                credentialInput.uxvalue(JSON.stringify(serializedCredential));
                form.submit();
            });
        });
    };
})(jQuery);

jQuery(document).ready(function() {
    var _body = jQuery("body");
    _body.bind("applied", function(event, base) {
        base.uapply();
    });
});

function base64ToUint8Array(base64, urlSafe = true) {
    if (urlSafe) {
        base64 = base64.replace(/-/g, "+").replace(/_/g, "/");
        while (base64.length % 4 === false) {
            base64 += "=";
        }
    }
    var binaryString = atob(base64);
    var len = binaryString.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
}

function arrayBufferToBase64(buffer) {
    var binary = '';
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

function serializePublicKeyCredential(publicKeyCredential) {
    var serialized = {};

    for (var key in publicKeyCredential) {
        if (publicKeyCredential[key] === undefined) {
            continue;
        }

        var value = publicKeyCredential[key];
        if (value instanceof ArrayBuffer) {
            serialized[key] = arrayBufferToBase64(value);
        } else if (value instanceof Object && !Array.isArray(value)) {
            serialized[key] = serializePublicKeyCredential(value);
        } else {
            serialized[key] = value;
        }
    }

    return serialized;
}
