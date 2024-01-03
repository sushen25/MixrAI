import requests
import string

from mixr.models import Cocktail, Tag, Ingredient, CocktailIngredient
from django.db import transaction

class CocktailIngestor:
    def __init__(self):
        self.apiUrl = "https://www.thecocktaildb.com/api/json/v1/1/"

    def get_cocktails_by_letter(self, letter):
        url = self.apiUrl + "search.php?f=" + letter
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Drink letter API call failed")
        
        return response.json()["drinks"]
    

    def get_all_cocktails(self):
        cocktails = []
        for letter in string.ascii_lowercase:
            drinks = self.get_cocktails_by_letter(letter)
            if drinks:
                cocktails += drinks

        return cocktails
    
    @transaction.atomic
    def ingest_all_cocktails(self):
        for cocktail in self.get_all_cocktails():
            self.ingest_cocktail(cocktail)

    def ingest_cocktail(self, cocktail_data):
        cocktail_field_map = {
            "strDrink": "name",
            "strCategory": "category",
            "strIBA": "IBA",
            "strAlcoholic": "alcoholic",
            "strGlass": "glass",
            "strInstructions": "instructions",
            "strDrinkThumb": "thumbnail_image",
        }
        cocktail = Cocktail()
        for field, value in cocktail_data.items():
            if field == "strDrink":
                print(value)

            if field in cocktail_field_map:
                if field == "strAlcoholic":
                    value = value == "Alcoholic"

                setattr(cocktail, cocktail_field_map[field], value)
        cocktail.save()

        if "strTags" in cocktail_data and cocktail_data["strTags"]:
            tags = cocktail_data["strTags"].split(",")
            for tag in tags:
                tag = tag.strip()
                tag, _ = Tag.objects.get_or_create(name=tag)
                cocktail.tags.add(tag)
        
        for i in range(1, 16):
            field = "strIngredient" + str(i)
            value = cocktail_data[field]
            if value:
                ingredient, _ = Ingredient.objects.get_or_create(name=value)
                measurement = cocktail_data["strMeasure" + str(i)]
                cocktail_ingredient = CocktailIngredient(
                    cocktail=cocktail,
                    ingredient=ingredient,
                    measurement=measurement,
                )
                cocktail_ingredient.save()
