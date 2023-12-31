from django.db import models
from rest_framework.exceptions import ValidationError

# Create your models here.


WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]


class OpeningHours(models.Model):
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        ordering = ("weekday", "from_hour")

    def clean(self):
        # Check if from_hour is less than to_hour
        if self.from_hour >= self.to_hour:
            raise ValidationError("from_hour must be less than to_hour")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_weekday_display()}: {self.from_hour} - {self.to_hour}"

    def __unicode__(self):
        return f"{self.get_weekday_display()}: {self.from_hour} - {self.to_hour}"


class Address(models.Model):
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.postal_code}, {self.country}"


class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, related_name="stores")
    opening_hours = models.ManyToManyField(OpeningHours, blank=True, related_name="stores")

    def __str__(self):
        return self.name
