/*
children() 返回所有下一级匹配的子元素 immediate children
find() 返回所有匹配的子元素 descendants
*/

jQuery(document).ready(function() {

    // Fullscreen background
    $.backstretch("/static/assets/img/backgrounds/1.jpg");

    $('#top-navbar-1').on('shown.bs.collapse', function(){
    	$.backstretch("resize");
    });
    $('#top-navbar-1').on('hidden.bs.collapse', function(){
    	$.backstretch("resize");
    });
    

    // Form
    $('.registration-form:first-child fieldset').fadeIn('slow');
    
    $('.registration-form input[type="text"], .registration-form input[type="password"], .registration-form input[type="email"]').on('focus', function() {
    	$(this).removeClass('input-error');
    });

    // submit
    $('.registration-form').on('submit', function(e) {
        $(this).find('input[type="text"], input[type="password"], input[type="email"]').each(function() {
            if( $(this).val() == "" ) {
                e.preventDefault();
                $(this).addClass('input-error');
            }
            else {
                $(this).removeClass('input-error');
            }
        });
    });

    // next step
    $('.registration-form .btn-next').click(function() {
    	var parentRegistrationForm = $(this).parents('.registration-form');
    	var nextStep = false;
    	
        $(this).parents(".registration-form").find("iframe").load(function() {
            nextStep = true;
    
        	parentRegistrationForm.find('input[type="text"], input[type="password"], input[type="email"]').each(function() {
        		if( $(this).val() == "" ) {
        			$(this).addClass('input-error');
        			nextStep = false;
        		}
        		else {
        			$(this).removeClass('input-error');
        		}
        	});

        	if(nextStep) {
        		parentRegistrationForm.children('fieldset').fadeOut(400, function() {
    	    		parentRegistrationForm.next().children("fieldset").fadeIn();
    	    	});
        	}
    	});

    });
    
    // previous step
    $('.registration-form .btn-previous').click(function() {
        var parentRegistrationForm = $(this).parents('.registration-form');
    	parentRegistrationForm.children('fieldset').fadeOut(400, function() {
            parentRegistrationForm.prev().children("fieldset").fadeIn();
        });
    });

    // clear
    $('.registration-form .btn-clear').click(function() {
        $(this).parents('.form-bottom').find('input').val("");
    });

    // password validate
    $(".registration-form[target='for_submit_refresh_3']").find("input[name='password_confirm']").keyup(function () {
        var pw1 = document.getElementsByName("password")[0].value;
        var pw2 = document.getElementsByName("password_confirm")[0].value;
        if(pw2.length < 6){
            document.getElementById("message").innerHTML="<font color='red'>Password must be longer than or equal to 6 digts.</font>";
            document.getElementById("sign_me_up_button").disabled = true;
        }
        else if(! /^(?=.*[a-z])[a-z0-9]+/ig.test(pw2)){
            document.getElementById("message").innerHTML="<font color='red'>Password may contain only letters or numbers.</font>";
            document.getElementById("sign_me_up_button").disabled = true;
        }
        else if(pw1 == pw2) {
            document.getElementById("message").innerHTML="<font color='green'>Password confirmed.</font>";
            document.getElementById("sign_me_up_button").disabled = false;
        } else {
            document.getElementById("message").innerHTML="<font color='red'>Passwords mismatch.</font>";
            document.getElementById("sign_me_up_button").disabled = true;
        }
    });
    
});
