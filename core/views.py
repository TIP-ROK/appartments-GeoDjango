import json

from django.core.serializers import serialize
from django.db.models import Prefetch
from django.shortcuts import render

from core.models import Flat, FlatPhoto


def map_view(request):
    flats = Flat.objects.prefetch_related(
        Prefetch('images', queryset=FlatPhoto.objects.all())
    ).all()

    flats_json = serialize('geojson', flats, fields=(
        'complex_name',
        'builder_company',
        'address',
        'polygon',
        'build_year',
        'price',
        'description',
    ))

    flats_json = json.loads(flats_json)

    for feature in flats_json['features']:
        flat_id = feature['id']
        flat = next(flat for flat in flats if flat.id == int(flat_id))
        flat_photos = flat.images.all()
        if flat_photos:
            feature['properties']['photo'] = [photo.photo.url for photo in flat_photos]

    return render(request, 'map.html', {'flats_json': flats_json})
