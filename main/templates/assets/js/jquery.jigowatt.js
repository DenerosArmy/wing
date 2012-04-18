/* =========================================================
 * jquery.jigowatt.js
 * Author: Jigowatt
 * ========================================================= */

$(function () {
	"use strict";

    // add active class to nav links
    // =============================
    var path = location.pathname.substr(location.pathname.lastIndexOf("/") + 1);
    if (path) {
		$('#findme li a[href$="' + path + '"]').parent().attr('class', 'active');
	}

    // focus inputs on load
    // ====================
    if ($('#CurrentPass').length) {
        $('#CurrentPass').focus();
    } else if ($('#name').length) {
        $('#name').focus();
    } else if ($('#username').length) {
        $('#username').focus();
    }

});

// checkbox logic
// ==============
$('.add-on :checkbox').click(function () {
	"use strict";
    if ($(this).attr('checked')) {
        $(this).parents('.add-on').addClass('active');
    } else {
        $(this).parents('.add-on').removeClass('active');
    }
});

// forgotten password modal
// ========================
$('#forgot-form').bind('shown', function () {
	"use strict";
    $('#usernamemail').focus();
});

$('#forgot-form').bind('hidden', function () {
	"use strict";
    $('#username').focus();
});

$('#forgotform').submit(function (e) {
	"use strict";

    e.preventDefault();
    $('#forgotsubmit').button('loading');

    var post = $('#forgotform').serialize();
    var action = $(this).attr('action');

    $("#message").slideUp(350, function () {

        $('#message').hide();

        $.post(action, post, function (data) {
            $('#message').html(data);
            document.getElementById('message').innerHTML = data;
            $('#message').slideDown('slow');
            $('#usernamemail').focus();
            if (data.match('success') !== null) {
                $('#forgotform').slideUp('slow');
                $('#forgotsubmit').button('complete');
                $('#forgotsubmit').click(function (eb) {
                    eb.preventDefault();
                    $('#forgot-form').modal('hide');
                });
            } else {
                $('#forgotsubmit').button('reset');
            }
        });
    });
});

// email subscription modal
// ========================
$('.subscribe').submit(function (e) {
	"use strict";

	e.preventDefault();
	$('#sub-submit').button('loading');

    var valid = true;
    var msg = '#sub-message';
    var form = '.subscribe';
	var post = $(form).serialize();
	var action = $(this).attr('action');

	function isEmail(emailAddress) {
		var pattern = new RegExp(/^(("[\w-+\s]+")|([\w-+]+(?:\.[\w-+]+)*)|("[\w-+\s]+")([\w-+]+(?:\.[\w-+]+)*))(@((?:[\w-+]+\.)*\w[\w-+]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][\d]\.|1[\d]{2}\.|[\d]{1,2}\.))((25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\.){2}(25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\]?$)/i);
		return pattern.test(emailAddress);
	}

    if (!isEmail($('#sub-email').val())) {
        valid = false;
    }

    $(msg).slideUp(function () {
        $(msg).hide();

        if (valid) {
            $.post(action, post);
            $(msg).html("<div class='alert alert-success'>Email added to subscription list</div>");
			$('#sub-submit').button('complete');
			$('#sub-submit').click(function (eb) {
				eb.preventDefault();
				$('#sub-form').modal('hide');
			});
            $(form).slideUp('slow');
            $(msg).slideDown(750);

        } else {
			$('#sub-submit').button('reset');
            $(msg).html("<div class='alert alert-error'>Are you sure that's your email? Hm...</div>");
            $(msg).slideDown(750);
        }
    });
});