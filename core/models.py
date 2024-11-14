from django.contrib.gis.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    polygon = models.GeometryField()
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Company(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    website_link = models.URLField(max_length=255)
    facebook_link = models.URLField(max_length=255, blank=True, null=True)
    twitter_link = models.URLField(max_length=255, blank=True, null=True)
    tik_tok_link = models.URLField(max_length=255, blank=True, null=True, verbose_name='Tik Tok')
    instagram_link = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def add_telephone_number(self, number):
        """Function to add a telephone number to the person"""
        telephone_number = TelephoneNumber(company=self, number=number)
        telephone_number.save()

    def get_telephone_numbers(self):
        """Function to get all telephone numbers of the person"""
        return self.telephone_numbers.all()


class TelephoneNumber(models.Model):
    company = models.ForeignKey(Company, related_name='telephone_numbers', on_delete=models.CASCADE)
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number


class Flat(BaseModel):
    complex_name = models.CharField(max_length=255)
    builder_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    build_year = models.CharField(max_length=4)
    price = models.DecimalField(decimal_places=2, max_digits=20, help_text='Price in USD for metr square')
    description = models.TextField()

    def __str__(self):
        return f"{self.complex_name}"


class FlatPhoto(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to='flat_images')

    def __str__(self):
        return f"{self.flat}"
