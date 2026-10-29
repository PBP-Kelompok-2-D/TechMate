# models.py — Defines the database table where every laptop we fetch from the
# RapidAPI "LaptopDB" service is saved, so our app can reuse the data locally.

from django.db import models


class Laptop(models.Model):
    # The full name of the laptop, e.g. "ASUS ROG Strix G15".
    # unique=True means two rows can never have the same name — this is what
    # lets update_or_create() in views.py recognize a laptop it saved before
    # and UPDATE it instead of creating a duplicate row.
    name = models.CharField(max_length=255, unique=True)

    # RAM amount in gigabytes (16 means 16 GB of RAM).
    ram_gb = models.IntegerField()

    # Total storage capacity in gigabytes (512 means 512 GB SSD/HDD).
    storage_gb = models.IntegerField()

    # Dedicated graphics (GPU) memory in gigabytes. 0 = no dedicated GPU.
    vram_gb = models.IntegerField()

    # The processor inside the laptop, e.g. "Intel Core i5-12450H".
    cpu = models.CharField(max_length=255)

    # Price in USD. We use DecimalField (not IntegerField) because real prices
    # can contain cents, e.g. 1299.99.
    # max_digits=12 = up to 12 digits total, decimal_places=2 = 2 of them
    # after the decimal point.
    price = models.DecimalField(max_digits=12, decimal_places=2)

    # What this laptop is good for, e.g. "Gaming, Video Editing".
    # blank=True makes the field optional — it may be left empty.
    recommended_for = models.CharField(max_length=255, blank=True)

    def __str__(self):
        # What Django shows for this row in the admin panel and shell:
        # simply the laptop's name instead of "Laptop object (3)".
        return self.name
