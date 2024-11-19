#preprocess.py
import spacy
import unidecode
from spellchecker import SpellChecker

# Charger le modèle français SpaCy
nlp = spacy.load("fr_core_news_sm")
spell = SpellChecker(language='fr')

# Mots spécifiques à votre domaine que vous ne voulez pas corriger
# Liste de produits connus
KNOWN_PRODUCTS = [
    "coca-cola", "pepsi", "fanta", "sprite", "orangina", "red bull", "tropicana juice", "evian water",
    "milk", "yogurt", "cheese", "butter", "cream", "tomate", "orange",
    "chicken", "beef", "pork", "salmon", "tuna", "shrimp",
    "rice", "wheat", "oats", "cornflakes", "pasta", "pomme",
    "apples", "bananas", "oranges", "strawberries", "grapes", "lemons",
    "carrots", "potatoes", "broccoli", "spinach", "tomatoes", "bell peppers",
    "chips", "chocolate", "nuts", "granola bars",
    "ketchup", "mustard", "mayonnaise", "olive oil", "vinegar", "salt", "pepper",
    "lipton ice tea", "schweppes", "san pellegrino",
    "nutella", "oreos", "haribo gummy bears", "m&m's", "pringles",
    "activia yogurt", "président cheese", "lactel milk", "philadelphia cream cheese",
    "birds eye frozen vegetables", "häagen-dazs ice cream", "mccain french fries",
    "kellogg's corn flakes", "jus orange", "jus", "jus d'orange bio", "jus d'orange", "cheerios", "special k",
    "lays chips", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", "twix", "snickers", "mars", "bounty",
    "heinz ketchup", "hellmann's mayonnaise", "tabasco sauce", "frank's redhot sauce",
    "quaker oats", "nestlé nesquik", "cadbury dairy milk", "milka chocolate",
    "ben & jerry's ice cream", "magnum ice cream", "breyers ice cream",
    "pringles", "lays", "doritos", 
    "kellogg's corn flakes","cheerios", "special k"
]

def preprocess_text(text):
    text_normalized = unidecode.unidecode(text.lower())
    doc = nlp(text_normalized)
    
    tokens = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            token_lemma = token.lemma_
            if token_lemma in KNOWN_PRODUCTS:
                corrected_token = token_lemma  # Ne pas corriger les noms de produits
            else:
                corrected_token = spell.correction(token_lemma)
            if corrected_token:
                tokens.append(corrected_token)
    
    return tokens  # Retourner une liste de tokens normalisés et corrigés
