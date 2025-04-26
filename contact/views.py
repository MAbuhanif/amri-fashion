from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Contact


class ContactFormCreateView(CreateView):
    """ View to handle contact form creation """
    model = Contact
    fields = ['email', 'name', 'subject', 'message']
    template_name = 'contact/contact_form.html'

    def get_initial(self):
        """ Pre-fill the email field if the user is authenticated """
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email
        return initial

    def get_success_url(self):
        """ Redirect to success page after form submission """
        return reverse('contact-success')

    def form_valid(self, form):
        """ Add success message and process the form """
        form.instance.author = self.request.user
        messages.success(self.request, "Message Sent!")
        return super().form_valid(form)


def ContactSuccess(request):
    """ Render the success page after form submission """
    return render(request, 'contact/contact_success.html')


class ContactListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """ View to display a list of contact messages for staff """
    model = Contact
    template_name = 'contact/contact_list.html'
    context_object_name = 'contacts'
    ordering = ['responded', 'pk']

    def test_func(self):
        """ Ensure only staff can access this view """
        return self.request.user.is_staff


class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ View to update contact messages and send responses """
    model = Contact
    fields = ["responded"]
    template_name_suffix = "_update_form"

    def _send_email(self):
        """ Send a response email to the contact """
        email = self.object.email
        subject = self.object.subject
        body = self.request.POST.get('email_body')
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

    def form_valid(self, form):
        """ Process the form and send the response email """
        form.instance.author = self.request.user
        messages.success(self.request, "Response sent via email")
        self._send_email()
        return super().form_valid(form)

    def test_func(self):
        """ Ensure only staff can access this view """
        return self.request.user.is_staff

    def get_success_url(self):
        """ Redirect to the same page after updating """
        return reverse('contact-update', kwargs={'pk': self.object.pk})


class ContactDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    """ View to delete contact messages """
    model = Contact
    success_url = reverse_lazy('contact-list')
    success_message = 'Message Deleted.'

    def test_func(self):
        """ Ensure only staff can delete messages """
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        """ Add success message and delete the message """
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
