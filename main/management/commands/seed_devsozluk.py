from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Topic, Entry
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "20 kullanıcı, 15 topic ve her topic'e 4 entry oluşturur"

    def handle(self, *args, **kwargs):
        # 1. 20 kullanıcı oluştur
        self.stdout.write("Kullanıcılar oluşturuluyor...")
        users = []
        for i in range(20):
            username = fake.user_name()
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('123456')  # kolay test şifresi
                user.save()
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f"{len(users)} kullanıcı oluşturuldu."))

        # 2. 15 topic ve her birine 4 entry oluştur
        self.stdout.write("Topic ve entry'ler oluşturuluyor...")
        for i in range(15):
            topic_title = fake.sentence(nb_words=4)
            topic = Topic.objects.create(
                title=topic_title,
                created_by=random.choice(users)
            )

            for j in range(4):
                Entry.objects.create(
                    topic=topic,
                    author=random.choice(users),
                    content=fake.paragraph(nb_sentences=3)
                )

        self.stdout.write(self.style.SUCCESS("15 topic ve her biri için 4 entry başarıyla oluşturuldu!"))
