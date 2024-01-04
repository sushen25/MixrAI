from django.db import models

# Create your models here.

class Cocktail(models.Model):
    """A Cocktail"""
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

    name = models.CharField(max_length=200, help_text="Name of the cocktail")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, help_text="Category of the cocktail")
    IBA = models.CharField(max_length=100, null=True, blank=True, help_text="International Bartenders Association category")
    alcoholic = models.BooleanField(default=True, help_text="Is the cocktail alcoholic?")
    glass = models.CharField(max_length=100, help_text="Type of glass to serve the cocktail in")
    instructions = models.TextField(help_text="Instructions for making the cocktail")
    thumbnail_image = models.URLField(help_text="URL of the thumbnail image for the cocktail")

    tags = models.ManyToManyField('Tag', help_text="Tags describing the cocktail")
    ingredients = models.ManyToManyField('Ingredient', through='CocktailIngredient', help_text="Ingredients in the cocktail")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tags describing attributes of a Cocktail"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """An ingredient"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CocktailIngredient(models.Model):
    """An ingredient in a cocktail"""
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measurement = models.CharField(max_length=100, null=True, blank=True, help_text="Measurement of the ingredient in the cocktail")

    def __str__(self):
        return self.cocktail.name + "<-" + self.ingredient.name
