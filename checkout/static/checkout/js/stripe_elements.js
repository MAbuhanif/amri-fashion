// This script handles the Stripe Elements integration for payment processing.

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

// Define styling for the card element
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// Create and mount the card element
var card = elements.create('card', { style: style });
card.mount('#card-element');

// Handle real-time validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submission
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    // Disable the card element and submit button to prevent multiple submissions
    card.update({ 'disabled': true });
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';
    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    email: $.trim(form.email.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.city.value),
                        state: $.trim(form.state.value),
                        country: $.trim(form.country.value),
                        postal_code: $.trim(form.postcode.value)
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.city.value),
                    state: $.trim(form.state.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value)
                }
            }
        }).then(function (result) {
            if (result.error) {
                // Display error message
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>
                `;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);

                // Re-enable the card element and submit button
                card.update({ 'disabled': false });
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    // Submit the form if payment is successful
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // Reload the page, the error will be in Django messages
        location.reload();
    });
});
