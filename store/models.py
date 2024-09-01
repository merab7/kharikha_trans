from django.db import models
from PIL import Image
import io
from django.core.files.base import ContentFile

#category for the products
class Category(models.Model):
    name = models.CharField(max_length=200, blank=False, null=True)
    name_en = models.CharField(max_length=200, blank=False, null=True)
    image = models.ImageField(upload_to='categories/', blank=False, null=True)

    def save(self, *args, **kwargs):
        # Call the original save method to handle file saving
        super().save(*args, **kwargs)

        # Open and resize the image
        if self.image:
            img = Image.open(self.image)

            # Resize image
            max_size = (300, 300)  # Define your maximum size here
            img.thumbnail(max_size, Image.LANCZOS)  # Updated from ANTIALIAS to LANCZOS

            # Save the image back to the same file
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85)  # Adjust quality as needed
            output.seek(0)
            self.image.save(self.image.name, ContentFile(output.read()), save=False)

        # Call the original save method to finalize saving
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

      



class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=True)
    name_en = models.CharField(max_length=100, blank=False, null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    cn = models.CharField(max_length=100, blank=False, null=True)
    cn_en = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=250, blank=False, null=True)
    description_en = models.CharField(max_length=250, blank=False, null=True)
    image = models.ImageField(upload_to='products/')
    model_image_1 = models.ImageField(upload_to='products/', blank=False, null=True)
    model_image_2 = models.ImageField(upload_to='products/', blank=False, null=True)
    sale = models.IntegerField(default=0)
    new_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def save(self, *args, **kwargs):
        # Calculate the new price based on sale percentage
        self.new_price = self.price - (self.price * self.sale) / 100

        # Call the original save method to handle file saving
        super().save(*args, **kwargs)

        # Process images
        for image_field in [self.image, self.model_image_1, self.model_image_2]:
            if image_field:
                img = Image.open(image_field)
                max_size = (800, 800)  # Define your maximum size here
                img.thumbnail(max_size, Image.LANCZOS)  # Updated from ANTIALIAS to LANCZOS
                
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85)
                output.seek(0)
                image_field.save(image_field.name, ContentFile(output.read()), save=False)

        # Call the original save method to finalize saving
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class ProductSize(models.Model):
    CHOICES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, choices=CHOICES)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('product', 'size') 

    
    def __str__(self) -> str:
         return (f'{self.product}, {self.size}')            



    








