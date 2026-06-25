from django.core.management.base import BaseCommand

from fruit_app.models import Category


class Command(BaseCommand):
    help = 'Seed default product categories into the Category model (idempotent)'

    def handle(self, *args, **options):
        categories = [
            'Citrus Fruits',
            'Tropical Fruits',
            'Berries',
            'Pome Fruits',
            'Melons',
            'Grapes',
        ]

        created_count = 0
        for name in categories:
            obj, created = Category.objects.get_or_create(category_name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {name}"))

        self.stdout.write(self.style.SUCCESS(f"Seeding complete. {created_count} new categories created."))
