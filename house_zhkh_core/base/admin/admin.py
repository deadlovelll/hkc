from django.contrib import admin
from house_zhkh.base.models.models import (
    Building,
    Flat,
    Counter,
    CounterHistory,
    Inhabitant,
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("id", "address")
    search_fields = ("address",)


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = ("id", "building", "flat_number", "flat_floor", "square")
    list_filter = ("building", "flat_floor")
    search_fields = ("flat_number",)


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ("id", "flat", "counter_type", "current_reading")
    list_filter = ("counter_type",)


@admin.register(CounterHistory)
class CounterHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "counter", "date", "reading")
    list_filter = ("date",)


@admin.register(Inhabitant)
class InhabitantAdmin(admin.ModelAdmin):
    list_display = ("id", "flat", "full_name", "age")
    search_fields = ("full_name",)
