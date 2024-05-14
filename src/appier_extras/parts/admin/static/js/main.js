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

        // retrieves the reference to the FIDO2 element and registers it
        // for the base FIDO2 plugin so that it's properly initialized
        var fido2 = jQuery(".fido2", matchedObject);
        fido2.ufido2();
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
    jQuery.fn.ufido2 = function(options) {
        // sets the jquery matched object
        var matchedObject = this;
        matchedObject.each(function(index, element) {
            var _element = jQuery(element);
            var form = _element.parents("form");

            var contents = JSON.parse(_element.text());

            //@TODO: need to soft-code this
            debugger;
            contents.publicKey.user.id = base64ToUint8Array(contents.publicKey.user.id);
            contents.publicKey.challenge = base64ToUint8Array(contents.publicKey.challenge);

            navigator.credentials.create(contents).then(function(credential) {
                //@TODO tenho d emeter a credentail em algum sitio
                debugger;
                form.submit();
            });
        });
    };
})(jQuery);

function base64ToUint8Array(base64) {
    var binaryString = atob(base64);
    var len = binaryString.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
}

jQuery(document).ready(function() {
    var _body = jQuery("body");
    _body.bind("applied", function(event, base) {
        base.uapply();
    });
});
