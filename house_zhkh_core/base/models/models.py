from django.db import models
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
    """Здание с адресом."""
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.address


class Flat(models.Model):
    """Квартира в здании."""
    building = models.ForeignKey (
        Building, on_delete=models.CASCADE, related_name="flats"
    )
    flat_number = models.PositiveIntegerField()
    flat_floor = models.PositiveIntegerField()
    square = models.PositiveIntegerField()

    def __str__(self):
        return f"Flat {self.flat_number}, {self.building.address}"


class FlatHcsBalance(models.Model):
    """Баланс ЖКХ для квартиры."""
    flat = models.ForeignKey (
        Flat, on_delete=models.CASCADE, related_name="balances"
    )
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"Balance for {self.flat}: {self.balance}"


class Counter(models.Model):
    """Счетчик для квартиры (газ, электричество, вода, тепло)."""
    
    class CounterType(models.IntegerChoices):
        GAS = 0, _("Gas Counter")
        ELECTRICITY = 1, _("Electricity Counter")
        WATER = 2, _("Water Counter")
        HEAT = 3, _("Heat Counter")

    flat = models.ForeignKey (
        Flat, on_delete=models.CASCADE, related_name="counters"
    )
    counter_type = models.IntegerField(choices=CounterType.choices)
    last_reading = models.FloatField()
    current_reading = models.FloatField()

    def __str__(self):
        return f"{self.get_counter_type_display()} for {self.flat}"


class CounterHistory(models.Model):
    """История показаний счетчиков."""
    counter = models.ForeignKey (
        Counter, on_delete=models.CASCADE, related_name="history"
    )
    date = models.DateField(auto_now_add=True)
    reading = models.FloatField()

    def __str__(self):
        return f"History for {self.counter} on {self.date}"


class Inhabitant(models.Model):
    """Жилец квартиры."""
    flat = models.ForeignKey (
        Flat, on_delete=models.CASCADE, related_name="inhabitants"
    )
    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.full_name} (Flat {self.flat.flat_number})"


class WaterMeter(models.Model):
    """Счетчик воды в квартире."""
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    reading = models.FloatField()
    month = models.DateField()

    def __str__(self):
        return f"WaterMeter {self.reading} for {self.flat} ({self.month})"


class Payment(models.Model):
    """Оплата ЖКХ за квартиру."""
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    month = models.DateField()
    water_fee = models.FloatField()
    common_area_fee = models.FloatField()
    total_fee = models.FloatField()

    def __str__(self):
        return f"Payment for {self.flat} ({self.month}): {self.total_fee}"
