from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Subscriber, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_create_notify(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        emails = []
        for category in categories:
            subs = Subscriber.objects.filter(subscription=category)
            for sub in subs:
                emails.append(sub.user.email)

        subject = f'Новая публикация в категории {instance.post_category}'

        text_content = (
            f'Название публикации: {instance.title}\n'
            f'Автор публикации: {instance.author_post}\n'
            f'Тип публикации: {instance.category_type}\n\n'
            f'Ссылка на публикацию.: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Название публикации: {instance.title}<br>'
            f'Автор публикации: {instance.author_post}<br>'
            f'Тип публикации: {instance.category_type}<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">Ссылка на публикацию</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    else:
        return

