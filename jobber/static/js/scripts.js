function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

jQuery.validate = function validate(thisEl) {
    let requiredInput = $(thisEl).parentsUntil("form, div.page-container").find('input.required');
    let isValError = false;
    requiredInput.each(function () {
        let reqParent = $(this).parent();
        if (!($(this).val())) {
            isValError = true;
            reqParent.css('display', 'inline-block');
            reqParent.css('border-style', 'solid');
            reqParent.css('border-color', 'indianred');
        } else {
            reqParent.css('display', 'inline');
            reqParent.css('border-style', 'none');
        }
    })

    if (isValError) {
        if (!($(thisEl).siblings('#input-error')).length) {
            let failMsg = $('<p id="input-error">Not Yet!  Please check that required fields are filled.</p>');
            $(thisEl).parent().append(failMsg);
        }
    }

    return isValError
}

jQuery.removePopup = function removePopup(thisEl) {
    thisEl.css('display', 'none')
    let popupForm = $(thisEl).parent();
    popupForm.trigger("reset");
    let requiredInput = $(popupForm).find('input.required');
    requiredInput.each(function () {
        let reqParent = $(this).parent();
        reqParent.css('display', 'inline');
        reqParent.css('border-style', 'none');
    })

    if (($(this).siblings('#input-error')).length) {
        let failMsg = $(this).siblings('#input-error');
        $(failMsg).remove();
    }
}

jQuery.searchArticles = function searchArticles(thisEl, searchPhrase) {
    if (searchPhrase === 'resume') {
        $('div.search-results-page').append(
            '    <div class="topic-box">\n' +
            '        <div class="content-box">\n' +
            '            <p class="search-header"><a href="#">Resume Tips: How Many Pages Is Right For You?</a></p>\n' +
            '            <p class="search-subtext">When building your resume, your goal is to put as much relevant ' +
            'experience as possible. Sometimes though you need more than one page to do so, but conventional wisdom is ' +
            'that resumes should fit in one page..</p>\n' +
            '        </div> <!-- search-result -->\n' +
            '    </div> <!-- topic-box -->'
        );
    } else {
        $('div.search-results-page').append(
            '<p class="sorry-message"><strong>Sorry!</strong> We cannot find anything related to your search for <em>' +
            searchPhrase + '</em>.  Try another search phrase!</p>'
        )
    }
}

$(document).ready(function () {

    /* Delete item alarm */
    $(document).on("click", 'button.delete', function (e) {
        if (!confirm("Are you sure you want to delete this?  You cannot undo.")) {
            e.preventDefault();
        }
    })

    /* Validation of required fields */
    $(document).on("click", 'button[type*="submit"]:not(div.popup-form button)', function (e) {
        let isError = $.validate($(this));
        if (isError) {
            e.preventDefault();
        }
    })


    /* Validation of required fields - remove flag when filled */
    $('div.topic-box').on('blur', 'input.required', function () {
        if (($(this).val())) {
            /* update style */
            let reqParent = $(this).parent();
            reqParent.css('display', 'inline');
            reqParent.css('border-style', 'none');
        }
    })

    /* Show Add Contact form */
    $('button.add-contact').on('click', function () {
        /* get which input is being added to */
        let contactSelect = $(this).prev().prev().children('select');
        let inputName = contactSelect.attr('name');
        /* add new contact form */
        let popupDiv = $(document).find('div.popup-form');
        popupDiv.css('display', 'block');
        /* modify form input to reflect which contact type */
        let whichForm = popupDiv.children("input[id*='formname']");
        whichForm.attr("value", inputName);
    });

    /* Submit new contact */
    $('div.popup-form').on('click', 'button#contact-submit', function (e) {
        let isError = $.validate($(this));
        if (isError) {
            e.preventDefault();
        } else {
            e.preventDefault();
            let ajax_url = $(this).attr("data-ajax-url");
            let curForm = $(this).prev();
            let contact_email = curForm.children('input').val();
            curForm = $(curForm).prev();
            let contact_phone = curForm.children('input').val();
            curForm = $(curForm).prev();
            let contact_title = curForm.children('input').val();
            curForm = $(curForm).prev();
            let contact_company = curForm.children('input').val();
            curForm = $(curForm).prev();
            let contact_name = curForm.children('input').val();
            curForm = $(curForm).prev();
            let formname = curForm.val();
            $.ajax({

                // The URL for the request
                url: ajax_url,

                // The data to send (will be converted to a query string)
                data: {
                    formname: formname,
                    contact_add_name: contact_name,
                    contact_add_company: contact_company,
                    contact_add_title: contact_title,
                    contact_add_phone: contact_phone,
                    contact_add_email: contact_email
                },

                // Whether this is a POST or GET request
                type: "POST",

                // The type of data we expect back
                dataType: "json",

                // CSRF
                headers: {'X-CSRFToken': csrftoken},

                context: this
            })
                // Code to run if the request succeeds (is done);
                // The response is passed to the function
                .done(function (json) {
                    if (json.success == 'success') {
                        let contacts = $(document).find('select[name*="' + json.contact_type + '"]');
                        let new_contact = $('<option value="' + json.contact_id + '">' + json.contact_name + '</option>')
                        new_contact.css('background-color', 'lightgreen')
                        contacts.append(new_contact);
                        let popupDiv = $(this).parent()
                        $.removePopup(popupDiv)
                    }
                })
                // Code to run if the request fails; the raw request and
                // status codes are passed to the function
                .fail(function (xhr, status, errorThrown) {
                    alert("Sorry, there was a problem!");
                    console.log("Error: " + errorThrown);
                })
                // Code to run regardless of success or failure;
                .always(function (xhr, status) {
                });
        }
    })

    /* Cancel New Contact Popup Form */
    $('div.popup-form').on('click', '#contact-cancel', function () {

        let popupDiv = $(document).find('div.popup-form')
        $.removePopup(popupDiv)

    })


    /* Contact Info Popup */
    $('ul.contact-list li a').on({
        mouseenter: function (e) {
            let ajax_url = $(this).parent().attr("data-ajax-url");
            let contact_id = $(this).parent().attr("data-contact");
            let popupDiv = $(document).find('div.popup-info')
            $.ajax({

                // The URL for the request
                url: ajax_url,

                // The data to send (will be converted to a query string)
                data: {
                    contact_id: contact_id
                },

                // Whether this is a POST or GET request
                type: "GET",

                // The type of data we expect back
                dataType: "json",

                // CSRF
                headers: {'X-CSRFToken': csrftoken},

                context: this
            })
                // Code to run if the request succeeds (is done);
                // The response is passed to the function
                .done(function (json) {
                    if (json.success == 'success') {
                        popupDiv.css('display', 'block');
                        let currentA = popupDiv.children('p').first();
                        $(currentA).children('span').text(json.contact_name);
                        currentA = currentA.next();
                        $(currentA).children('span').text(json.contact_title);
                        currentA = currentA.next();
                        $(currentA).children('span').text(json.contact_company);
                        currentA = currentA.next();
                        $(currentA).children('span').text(json.contact_phone);
                        currentA = currentA.next();
                        $(currentA).children('span').text(json.contact_email);
                    }
                })
                // Code to run if the request fails; the raw request and
                // status codes are passed to the function
                .fail(function (xhr, status, errorThrown) {
                    alert("Sorry, there was a problem!");
                    console.log("Error: " + errorThrown);
                })
                // Code to run regardless of success or failure;
                .always(function (xhr, status) {
                });
        },
        mouseleave: function (e) {
            let popupDiv = $(document).find('div.popup-info')
            popupDiv.css('display', 'none');
            let currentA = popupDiv.children('p').first();
            $(currentA).children('span').text('');
            currentA = currentA.next();
            $(currentA).children('span').text('');
            currentA = currentA.next();
            $(currentA).children('span').text('');
            currentA = currentA.next();
            $(currentA).children('span').text('');
            currentA = currentA.next();
            $(currentA).children('span').text('');
        }
    });

    /* Opportunity List Sort */
    $('select#sort-opportunities').on('change', function (e) {
        let sortData = $(this).children(':selected');
        let ajax_url = $(this).attr('data-ajax-url')

        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                sorter: sortData.val()
            },

            // Whether this is a POST or GET request
            type: "GET",

            // The type of data we expect back
            dataType: "json",

            // CSRF
            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function (json) {
                let listUL = $('ul.detail-list');
                $.each(json.opportunities, function (index, value) {
                    listUL.children("li[data-id*=" + value + "]").attr('data-sort-order', index)
                })
                $(listUL.children()).sort(function (a, b) {
                    let elA = parseInt($(a).attr('data-sort-order'));
                    let elB = parseInt($(b).attr('data-sort-order'));
                    return (elA < elB) ? -1 : (elA > elB) ? 1 : 0;
                }).appendTo($(listUL));
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
            })
            // Code to run regardless of success or failure;
            .always(function (xhr, status) {
            });
    })

    /* Search behavior */
    $(function () {
        if (($('div.search-results-page').length)) {
            let urlParams = new URLSearchParams(window.location.search)
            if (urlParams.has('search-articles')) {
                let searchStr = urlParams.get('search-articles');
                $.searchArticles($(this), searchStr);
            }
        }
    })
})

