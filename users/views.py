# coding=utf-8
from __future__ import unicode_literals

from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import (
    authenticate,
    REDIRECT_FIELD_NAME,
    login as auth_login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.forms import forms
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class SiteAuthenticationForm(AuthenticationForm):
    """
    Inherits a standard authentication, plus check assigned sites
    """

    def clean(self):

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Please enter a correct username and password. "
                      "Note that both fields are case-sensitive.")
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        return self.cleaned_data


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=SiteAuthenticationForm,
          current_app=None, extra_context=None):

    redirect_to = request.POST.get(
        redirect_field_name,
        request.GET.get(redirect_field_name, '')
    )

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)

        if form.is_valid():
            netloc = urlparse(redirect_to)[1]

            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
