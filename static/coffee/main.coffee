$ ->
    $.ajaxSetup beforeSend: (xhr, settings) ->
        getCookie = (name) ->
            cookieValue = null
            if document.cookie and document.cookie != ''
                cookies = document.cookie.split(';')
                i = 0
                while i < cookies.length
                    cookie = jQuery.trim(cookies[i])
                    # Does this cookie string begin with the name we want?
                    if cookie.substring(0, name.length + 1) == name + '='
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                        break
                    i++
            cookieValue

        if !(/^http:.*/.test(settings.url) or /^https:.*/.test(settings.url))
            # Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader 'X-CSRFToken', getCookie('csrftoken')
        return

    $('form#verify-auth').on 'click', '.toggle-verify-auth-btn', ->
        if $('.verify-auth-block').is(':visible')
            $('.verify-auth-block').slideUp();
        else
            $('.verify-auth-block').slideDown();
        return
    
    # initial login to ensure authentication is good 
    # and account has a paid posting account id
    $('form#verify-auth').submit (e) ->
        console.log 'Verifying authentication'
        $('.verify-auth-btn').html('Verifying...');
        $.ajax(
            type: 'POST'
            url: '/cl/verify_auth'
            data: { email: $('#cl_email').val(), pass: $('#cl_password').val() }
            dataType: 'json').done((data)->
                console.log 'success'
                console.log data
                accountId = data.account_id
                $('#cl_account_num').html(accountId)
                $('#cl_account_num_input').val(accountId)
                if data.success == false
                    alert data.error
                    $('#cl_account_num').html(data.error)
                else
                    $('.verify-auth-block').slideUp();
                    $('.show-verify-auth-btn').slideDown();
                    $('form#post-job').slideDown();
                return
            ).fail((data, textStatus, errorThrown) ->
                console.log 'fail'
                console.log data
                return
            ).always (data, textStatus, errorThrown) ->
                $('.verify-auth-btn').html('Verify Credentials');
                console.log 'always'
                console.log textStatus
                console.log errorThrown
                return
        e.preventDefault e
        return