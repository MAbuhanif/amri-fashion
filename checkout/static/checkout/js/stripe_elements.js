const stripe = Stripe('{{ stripe_public_key }}');
    const elements = stripe.elements();
    const card = elements.create('card');
    card.mount('#card-element');

    const form = document.getElementById('payment-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const { paymentIntent, error } = await stripe.confirmCardPayment('{{ client_secret }}', {
            payment_method: {
                card: card,
                billing_details: {
                    name: form.querySelector('input[name="full_name"]').value,
                    email: form.querySelector('input[name="email"]').value,
                },
            },
        });

        if (error) {
            document.getElementById('card-errors').textContent = error.message;
        } else {
            form.submit();
        }
    });