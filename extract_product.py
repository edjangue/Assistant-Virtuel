#extract_product.py
import spacy
import logging
import requests

# Charger le modèle français
nlp = spacy.load('fr_core_news_sm')
logging.basicConfig(level=logging.DEBUG)

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

def extract_product_name(user_message):
    doc = nlp(user_message)
    product_name = None

    # Extraire les entités de type 'PRODUCT'
    for ent in doc.ents:
        if ent.label_ == "PRODUCT":
            product_name = ent.text.lower()
            logging.debug(f"Produit trouvé par entité : {product_name}")
            return product_name

    # Recherche dans les tokens si aucune entité n'est trouvée
    message_tokens = [token.text.lower() for token in doc]
    for i in range(len(message_tokens)):
        for j in range(i + 1, len(message_tokens) + 1):
            candidate_product = ' '.join(message_tokens[i:j])
            if candidate_product in KNOWN_PRODUCTS:
                product_name = candidate_product
                logging.debug(f"Produit trouvé dans les tokens : {product_name}")
                return product_name

    # Si aucune correspondance n'est trouvée, rechercher dans l'API
    product_name = ' '.join(message_tokens)  # Utiliser le message complet de l'utilisateur
    api_url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&json=1"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        data = response.json()

        if 'products' in data and data['products']:
            product_name = data['products'][0].get('product_name', '').lower()
            logging.debug(f"Produit trouvé dans l'API : {product_name}")
            return product_name
        else:
            logging.debug("Aucun produit trouvé dans l'API.")
            return "Aucun produit trouvé. Veuillez réessayer."
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la requête API : {e}")
        return "Erreur lors de la recherche du produit. Veuillez réessayer."

    # Cette ligne est maintenant atteignable
    logging.debug("Aucun produit trouvé.")
    return "Aucun produit trouvé. Veuillez réessayer."