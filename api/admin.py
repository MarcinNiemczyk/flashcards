from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from api.models import Box, Card, Deck


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_total_cards", "box_amount", "get_author")
    list_filter = ("name", "author")
    search_fields = ("name", "author__username")

    def get_total_cards(self, obj):
        return Box.objects.filter(deck=obj).aggregate(Count("card"))[
            "card__count"
        ]

    get_total_cards.short_description = "total cards"

    def get_author(self, obj):
        url = reverse("admin:auth_user_change", args=(obj.author.id,))
        return format_html("<a href='{}'>{}</a>", url, obj.author.username)

    get_author.admin_order_field = "author"
    get_author.short_description = "author"


class CardInline(admin.TabularInline):
    model = Card
    extra = 0


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    inlines = [
        CardInline,
    ]

    list_display = ("__str__", "get_cards", "get_deck_link")
    list_filter = ("deck",)
    search_fields = ("deck__name", "deck__author__username")
    readonly_fields = ("number_of", "deck")

    def get_cards(self, obj):
        return obj.card_set.count()

    get_cards.short_description = "cards"

    def get_deck_link(self, obj):
        url = reverse("admin:api_deck_change", args=(obj.deck.id,))
        return format_html("<a href='{}'>{}</a>", url, obj.deck.name)

    get_deck_link.admin_order_field = "deck"
    get_deck_link.short_description = "deck"


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("front", "back", "active", "get_box_link")
    list_filter = ("active",)
    search_fields = ("front", "back")

    def get_box_link(self, obj):
        url = reverse("admin:api_box_change", args=(obj.box.id,))
        return format_html("<a href='{}'>{}</a>", url, str(obj.box))

    get_box_link.admin_order_field = "box"
    get_box_link.short_description = "box"
