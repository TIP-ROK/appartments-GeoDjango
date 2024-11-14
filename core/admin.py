from django.contrib import admin
from django.utils.safestring import mark_safe
from leaflet.admin import LeafletGeoAdmin

from core.models import Company, TelephoneNumber, Flat, FlatPhoto


class TelephoneNumberInline(admin.TabularInline):
    model = TelephoneNumber
    extra = 1


@admin.register(Company)
class CompanyAdmin(LeafletGeoAdmin):
    list_display = ('name', 'address', 'website_link', 'created_at', 'updated_at')
    search_fields = ('name', 'address')
    inlines = [TelephoneNumberInline]
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'address', 'website_link', 'polygon',)
        }),
        ('Social Media Links', {
            'fields': ('facebook_link', 'twitter_link', 'tik_tok_link', 'instagram_link')
        }),
        ('Display on client side', {
           'fields': ('is_active',)
        }),
    )


@admin.register(TelephoneNumber)
class TelephoneNumberAdmin(admin.ModelAdmin):
    list_display = ('company', 'number')
    search_fields = ('number',)
    ordering = ('company',)



class FlatPhotoTabular(admin.TabularInline):
    model = FlatPhoto
    extra = 1
    readonly_fields = ('show_photo',)

    def show_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=100>")

    show_photo.short_description = 'Image'


@admin.register(Flat)
class FlatAdmin(LeafletGeoAdmin):
    list_display = (
        'complex_name',
        'builder_company',
        'address',
        'build_year',
        'price',
        'created_at',
        'updated_at',
    )
    readonly_fields = ('id', )
    search_fields = ('complex_name', 'address')
    inlines = [FlatPhotoTabular]
    ordering = ('-created_at',)
    list_display_links = (
        'complex_name',
        'builder_company',
        'address',
        'build_year',
        'price',
        'created_at',
        'updated_at',
    )
    fieldsets = (
        (None, {
            'fields': ('id', 'complex_name', 'builder_company', 'address', 'build_year', 'price', 'description',  'polygon',)
        }),
        ('Display on client side', {
           'fields': ('is_active', )
        }),
    )
