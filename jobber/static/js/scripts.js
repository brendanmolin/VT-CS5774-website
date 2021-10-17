jQuery.validate = function validate(thisEl) {
    let requiredInput = $(thisEl).parentsUntil("form").find('input.required');
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

    $(document).on("click", 'button.delete', function(e) {
        if(!confirm("Are you sure you want to delete this?  You cannot undo.")) {
            e.preventDefault();
        }
    })

    $(document).on("click", 'button[type*="submit"]:not(div.popup-form button)', function (e) {
        let isError = $.validate($(this));
        if (isError) {
            e.preventDefault();
        }
    })

    $('div.topic-box').on('blur', 'input.required', function () {
        if (($(this).val())) {
            /* update style */
            let reqParent = $(this).parent();
            reqParent.css('display', 'inline');
            reqParent.css('border-style', 'none');
        }
    })

    $('button.add-contact').on('click', function () {
        /* add new contact form */
        let contactBox = $(this).parent().parent().parent().parent().parent().parent().parent();
        if (!(contactBox.children('form[name*="new-contact-form"]').length)) {
            let addContactForm =
                '<form name="new-contact-form">' +
                '<div class="form-box popup-form">' +
                '<h3>New Contact Information:</h3>' +
                '<p><label for="contact-add-name">Name: </label>' +
                '<input type="text" name="contact-add-name" class="required" id="contact-add-name"></p>' +
                '<p><label for="contact-add-title">Title: </label>' +
                '<input type="text" name="contact-add-title" class="required" id="contact-add-title"></p>' +
                '<p><label for="contact-add-company">Company: </label>' +
                '<input type="text" name="contact-add-company" class="required" id="contact-add-company"></p>' +
                '<p><label for="contact-add-phone">Phone Number: </label>' +
                '<input type="tel" name="contact-add-phone" class="required" id="contact-add-phone"></p>' +
                '<p><label for="contact-add-email">Email: </label>' +
                '<input type="email" name="contact-add-email" class="required" id="contact-add-email"></p>' +
                '<button type="submit" id="contact-submit" class="button-small contact-list-submit-button">Save</button>' +
                '<button type="button" id="contact-cancel" class="button-small">Cancel</button>' +
                '</div><!-- contact-list-add -->' +
                '</form>';
            contactBox.append(addContactForm);
        }
    });

    $('div.topic-box').on('click', 'button#contact-submit', function (e) {
        let isError = $.validate($(this));
        if (isError) {
            e.preventDefault();
        } else {
            /* TODO: submit form without reloading page */
            e.preventDefault();
            $(this).parent().parent().remove();
        }
    })

    $('div.topic-box').on('click', 'button#contact-cancel', function () {
        $(this).parent().parent().remove();
    })

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

