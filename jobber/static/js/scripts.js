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
        console.log("delete");
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

    $('div.popup-form').on('click', 'button#contact-submit', function (e) {
        let isError = $.validate($(this));
        if (isError) {
            e.preventDefault();
        } else {
            console.log(e.defaultPrevented);
            /* TODO: submit form without reloading page */
        }
    })

    $('div.popup-form').on('click', '#contact-cancel', function () {
        let popupDiv = $(document).find('div.popup-form')
        popupDiv.css('display', 'none')
        let popupForm = $(popupDiv).parent();
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

