#traceability.py
import requests
import logging

# Activer le logging détaillé
logging.basicConfig(level=logging.DEBUG)

def detect_user_intent_from_tokens(tokens):
    intent_mapping = {
        'ingredients': ['ingrédient', 'ingredients', 'ingrédients', 'ingredient'],
        'origine': ['origine', 'provenance', 'provient', 'traçabilité', 'proviennent'],
        'marque': ['marque'],
        'nutriments': ['nutriment', 'valeur nutritionnelle'],
        'additifs': ['additif', 'additifs'],
        'allergenes': ['allergène', 'allergènes', 'contient', 'ne contient pas'],
        'labels': ['label', 'labels', 'certification', 'certifications', 'bio', 'équitable', 'AOP', 'IGP'],
        'emballage': ['emballage', 'emballages', 'recyclable', 'non recyclable', 'plastique', 'verre', 'carton'],
        'date_peremption': ['date de péremption', 'expiration', 'date limite de consommation', 'DLC', 'DLUO'],
        'prix': ['prix', 'coût', 'tarif'],
        'quantite': ['quantité', 'poids', 'volume', 'taille', 'portion'],
        'conservation': ['conservation', 'conserver', 'température', 'conditions de stockage'],
        'preparation': ['préparation', 'mode d\'emploi', 'cuisson', 'recette'],
        'origine_geographique': ['pays', 'région', 'localité', 'fabriqué en', 'produit en'],
        'impact_environnemental': ['empreinte carbone', 'impact écologique', 'durabilité', 'écoresponsable'],
        'avis': ['avis', 'critiques', 'notes', 'évaluations'],
        'composition_detaillee': ['composition', 'ingrédients détaillés', 'liste des ingrédients'],
        'valeurs_nutritionnelles': ['calories', 'protéines', 'glucides', 'lipides', 'fibres', 'sucres','sucre', 'sel']
    }

    # Parcourez les tokens et vérifiez si l'un des mots-clés correspond
    for intent, keywords in intent_mapping.items():
        if any(keyword in tokens for keyword in keywords):
            return intent
            
    return 'general'  # Si aucune intention spécifique n'est trouvée


def get_product_traceability(product_name, user_intent):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&json=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        logging.debug(f"Réponse API OpenFoodFacts pour le produit {product_name} : {data}")

        # Vérifier si l'API retourne des produits
        if 'products' not in data or len(data['products']) == 0:
            # Aucune information trouvée
            return f"Nous n'avons pas trouvé d'informations sur la traçabilité pour le produit '{product_name}'."
        
        
        if 'products' in data and len(data['products']) > 0:
            product = data['products'][0]
            
            # Récupération des informations principales
            product_name = product.get('product_name', 'Inconnu')
            brand = product.get('brands', 'Inconnue')
            origin = product.get('origins', 'Inconnue')
            ingredients = product.get('ingredients_text', 'Inconnus')
            nutrients = product.get('nutriments', {})  # Nutriments du produit
            additives = product.get('additives_tags', [])
            allergens = product.get('allergens_tags', [])
            labels = product.get('labels_tags', [])
            packaging = product.get('packaging', 'Inconnu')
            expiration_date = product.get('expiration_date', 'Inconnue')
            price = product.get('price', 'Inconnu')
            quantity = product.get('quantity', 'Inconnue')
            conservation = product.get('conservation_conditions', 'Inconnues')
            preparation = product.get('preparation', 'Inconnue')
            geographic_origin = product.get('origins_tags', [])
            environmental_impact = product.get('environment_impact_level_tags', [])
            reviews = product.get('reviews_tags', [])
            detailed_composition = product.get('ingredients_analysis_tags', [])
            nutritional_values = product.get('nutriments', {})

            # Dictionnaire pour stocker les réponses selon l'intention
            responses = {}
            
            # Construire les réponses basées sur l'intention de l'utilisateur
            if user_intent == 'ingredients':
                responses['ingredients'] = f"Le produit '{product_name}' contient les ingrédients suivants : {ingredients}."
            elif user_intent == 'origine':
                responses['origine'] = f"Le produit '{product_name}' provient de {origin}."
            elif user_intent == 'marque':
                responses['marque'] = f"Le produit est fabriqué par la marque {brand}."
            elif user_intent == 'nutriments':
                # Exemple : extraire les valeurs nutritionnelles spécifiques
                energy = nutrients.get('energy_100g', 'Inconnu')
                fat = nutrients.get('fat_100g', 'Inconnu')
                sugar = nutrients.get('sugars_100g', 'Inconnu')
                responses['nutriments'] = (f"Le produit '{product_name}' contient {energy} kJ d'énergie, {fat}g de matières grasses, "
                                            f"et {sugar}g de sucres pour 100g.")
            elif user_intent == 'additifs':
                if additives:
                    responses['additifs'] = f"Le produit '{product_name}' contient les additifs suivants : {', '.join(additives)}."
                else:
                    responses['additifs'] = f"Le produit '{product_name}' ne contient aucun additif répertorié."
            elif user_intent == 'allergenes':
                if allergens:
                    responses['allergenes'] = f"Le produit '{product_name}' contient les allergènes suivants : {', '.join(allergens)}."
                else:
                    responses['allergenes'] = f"Le produit '{product_name}' ne contient aucun allergène répertorié."
            elif user_intent == 'labels':
                if labels:
                    responses['labels'] = f"Le produit '{product_name}' possède les labels suivants : {', '.join(labels)}."
                else:
                    responses['labels'] = f"Le produit '{product_name}' ne possède aucun label répertorié."
            elif user_intent == 'emballage':
                responses['emballage'] = f"Le produit '{product_name}' est emballé dans : {packaging}."
            elif user_intent == 'date_peremption':
                responses['date_peremption'] = f"Le produit '{product_name}' a une date de péremption de : {expiration_date}."
            elif user_intent == 'prix':
                responses['prix'] = f"Le prix du produit '{product_name}' est : {price}."
            elif user_intent == 'quantite':
                responses['quantite'] = f"Le produit '{product_name}' a une quantité de : {quantity}."
            elif user_intent == 'conservation':
                responses['conservation'] = f"Les conditions de conservation pour le produit '{product_name}' sont : {conservation}."
            elif user_intent == 'preparation':
                responses['preparation'] = f"Les instructions de préparation pour le produit '{product_name}' sont : {preparation}."
            elif user_intent == 'origine_geographique':
                if geographic_origin:
                    responses['origine_geographique'] = f"Le produit '{product_name}' provient de : {', '.join(geographic_origin)}."
                else:
                    responses['origine_geographique'] = f"Le produit '{product_name}' n'a pas d'origine géographique répertoriée."
            elif user_intent == 'impact_environnemental':
                if environmental_impact:
                    responses['impact_environnemental'] = f"L'impact environnemental du produit '{product_name}' est : {', '.join(environmental_impact)}."
                else:
                    responses['impact_environnemental'] = f"Le produit '{product_name}' n'a pas d'impact environnemental répertorié."
            elif user_intent == 'avis':
                if reviews:
                    responses['avis'] = f"Les avis des consommateurs pour le produit '{product_name}' sont : {', '.join(reviews)}."
                else:
                    responses['avis'] = f"Le produit '{product_name}' n'a pas d'avis de consommateurs répertoriés."
            elif user_intent == 'composition_detaillee':
                if detailed_composition:
                    responses['composition_detaillee'] = f"La composition détaillée du produit '{product_name}' est : {', '.join(detailed_composition)}."
                else:
                    responses['composition_detaillee'] = f"Le produit '{product_name}' n'a pas de composition détaillée répertoriée."
            elif user_intent == 'valeurs_nutritionnelles':
                calories = nutritional_values.get('energy-kcal_100g', 'Inconnu')
                proteins = nutritional_values.get('proteins_100g', 'Inconnu')
                carbs = nutritional_values.get('carbohydrates_100g', 'Inconnu')
                fats = nutritional_values.get('fat_100g', 'Inconnu')
                fibers = nutritional_values.get('fiber_100g', 'Inconnu')
                sugars = nutritional_values.get('sugars_100g', 'Inconnu')
                salt = nutritional_values.get('salt_100g', 'Inconnu')

                responses['valeurs_nutritionnelles'] = (f"Le produit '{product_name}' contient {calories} kcal, {proteins}g de protéines, "
                                                        f"{carbs}g de glucides, {fats}g de lipides, {fibers}g de fibres, {sugars}g de sucres, "
                                                        f"et {salt}g de sel pour 100g.")
 
 
            # Construction de la réponse finale
            if responses:
                return "\n".join(responses.values())
            else:
                # Fallback si aucune intention correspondante n'est trouvée
                return (f"Le produit '{product_name}' de la marque {brand} est originaire de {origin} et contient "
                        f"les ingrédients suivants : {ingredients}.")
    
    # Si aucune donnée n'est trouvée
    return f"Impossible d'accéder aux informations pour le produit '{product_name}'."
