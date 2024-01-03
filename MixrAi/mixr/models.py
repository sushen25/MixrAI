from django.db import models

# Create your models here.

class Cocktail(models.Model):
    CATEGORY_CHOICES = [
        ('Ordinary Drink', 'Ordinary Drink'),
        ('Cocktail', 'Cocktail'),
        ('Shake', 'Shake'),
        ('Other / Unknown', 'Other / Unknown'),
        ('Cocoa', 'Cocoa'),
        ('Shot', 'Shot'),
        ('Coffee / Tea', 'Coffee / Tea'),
        ('Homemade Liqueur', 'Homemade Liqueur'),
        ('Punch / Party Drink', 'Punch / Party Drink'),
        ('Beer', 'Beer'),
        ('Soft Drink', 'Soft Drink'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    IBA = models.CharField(max_length=100, null=True, blank=True)
    alcoholic = models.BooleanField(default=True)
    glass = models.CharField(max_length=100)
    instructions = models.TextField()
    thumbnail_image = models.URLField()

    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient', through='CocktailIngredient')

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tags describing attributes of a Cocktail"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measurement = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.cocktail.name + "<-" + self.ingredient.name
