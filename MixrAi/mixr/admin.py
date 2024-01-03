from django.contrib import admin


from .models import Cocktail, Tag, Ingredient, CocktailIngredient

@admin.register(Cocktail)
class cocktail_admin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class tag_admin(admin.ModelAdmin):
    pass

@admin.register(Ingredient)
class ingredient_admin(admin.ModelAdmin):
    pass

@admin.register(CocktailIngredient)
class cocktail_ingredient_admin(admin.ModelAdmin):
    pass