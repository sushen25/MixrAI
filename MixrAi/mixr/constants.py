
DATABASE_SCHEMA = """
Name of Django app: mixr

Cocktail Table Schema:
- id: Primary Key, Auto-increment
- name: CharField(max_length=200), help_text='Name of the cocktail'
- category: CharField(max_length=100) with choices (Ordinary Drink, Cocktail, etc.), help_text='Category of the cocktail'
- IBA: CharField(max_length=100), nullable and blank, help_text='International Bartenders Association category'
- alcoholic: BooleanField, default True, help_text='Is the cocktail alcoholic?'
- glass: CharField(max_length=100), help_text='Type of glass to serve the cocktail in'
- instructions: TextField, help_text='Instructions for making the cocktail'
- thumbnail_image: URLField, help_text='URL of the thumbnail image for the cocktail'
- tags: ManyToManyField with Tag, help_text='Tags describing the cocktail'
- ingredients: ManyToManyField with Ingredient through CocktailIngredient, help_text='Ingredients in the cocktail'

Tag Table Schema:
- id: Primary Key, Auto-increment
- name: CharField(max_length=100), unique, help_text='Tag name'

Ingredient Table Schema:
- id: Primary Key, Auto-increment
- name: CharField(max_length=100), unique, help_text='Ingredient name'

CocktailIngredient Table Schema:
- id: Primary Key, Auto-increment
- cocktail: ForeignKey to Cocktail, help_text='Cocktail containing the ingredient'
- ingredient: ForeignKey to Ingredient, help_text='Ingredient in the cocktail'
- measurement: CharField(max_length=100), nullable and blank, help_text='Measurement of the ingredient in the cocktail'
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "ask_database",
            "description": "Use this function to answer user questions about Cocktails. Input should be a fully formed SQL query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                                SQL query extracting info to answer the user's question about cocktails.
                                SQL should be written for a sqlite3 database using this Django model database schema:
                                {DATABASE_SCHEMA}
                                The query should be returned in PLAIN TEXT, not in JSON.
                                The query should not contain unnecessary whitespace and should be written on one line.
                                The query should be able to access the Django database accurately and return the correct results, including the use of '__' to span relationships.
                                The querys should use SQL joins when spanning Many to Many relationships.
                                """,
                    }
                },
                "required": ["query"],
            },
        }
    }
]

