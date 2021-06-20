"""JobAdvisor tasks."""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Template
from django.template.loader import get_template

from jobadvisor.celery import app


@app.task
def send_email(emails: list,
               template_name: str,
               context: dict,
               title: str = "JobAdvisor team") -> None:
    """
    Send email to.

    :param title: mail title
    :param emails: user mail addresses
    :param template_name: message template
    :param context: message context
    :return: None
    """
    template: Template = get_template(template_name)
    context["SITE_URL"] = settings.SITE_URL
    body = template.render(context=context)
    mail = EmailMultiAlternatives(subject=title,
                                  body=body,
                                  from_email=settings.EMAIL_HOST_USER,
                                  to=emails)
    mail.attach_alternative(body, "text/html")
    mail.send(fail_silently=True)
