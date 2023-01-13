from .models import UserProfile
from leads.models import Category


def receiver_func(sender, instance, created, **kwargs):
    # create UserProfile when new user signup
    if created and instance.is_organisor:
        UserProfile.objects.create(user=instance)
        categories = ["Recent", "Contacted", "Converted", "Unconverted"]
        Category.objects.bulk_create([
            Category(name=name, organisation=instance.userprofile) for name in categories
        ])
