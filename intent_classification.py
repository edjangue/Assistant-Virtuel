#intent_classification.py
# intent_classification.py

from preprocess import preprocess_text
from transformers import pipeline

# Chargement du modèle de classification multilingue
classifier = pipeline("text-classification", model="bert-base-multilingual-cased")

# Mappage des intentions et des mots-clés associés
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
    'valeurs_nutritionnelles': ['calories', 'protéines', 'glucides', 'lipides', 'fibres', 'sucres', 'sucre', 'sel']
}

# Regrouper tous les mots-clés pertinents pour la traçabilité dans une seule liste
traceability_keywords = set(
    intent_mapping['ingredients'] + 
    intent_mapping['origine'] + 
    intent_mapping['marque'] + 
    intent_mapping['nutriments'] + 
    intent_mapping['additifs'] + 
    intent_mapping['allergenes'] + 
    intent_mapping['labels'] + 
    intent_mapping['emballage'] + 
    intent_mapping['date_peremption'] + 
    intent_mapping['prix'] + 
    intent_mapping['quantite'] + 
    intent_mapping['conservation'] + 
    intent_mapping['preparation'] + 
    intent_mapping['origine_geographique'] + 
    intent_mapping['impact_environnemental'] + 
    intent_mapping['avis'] + 
    intent_mapping['composition_detaillee'] + 
    intent_mapping['valeurs_nutritionnelles']
)

def detect_user_intent_from_tokens(tokens):
    for token in tokens:
        # Si le token est un mot-clé pertinent pour la traçabilité
        if token in traceability_keywords:
            return 'traceability'  # Rediriger vers l'intention de traçabilité
            
    return 'general'  # Si aucune intention spécifique n'est trouvée

def classify_intent(user_message):
    preprocessed_message = ' '.join(preprocess_text(user_message))  # Assurez-vous que preprocess_text renvoie une chaîne.

    # Vérifications basées sur des phrases clés
    product_related_phrases = [
        'origine', 'prix', 'calories', 'durabilité', 
        'nutriment', 'recette', 'provenance', 
        'provient', 'traçabilité', 'ingrédient', 
        'composition', 'contient', 'détails du produit'
    ]
    
    recommendation_phrases = [
        'recommander', 'suggestion', 'recommandation',
        "qu'est-ce que je devrais essayer", 
        'produits similaires', 'alternatives'
    ]
    
    nutrition_phrases = [
        'nutrition', 'conseil', 'santé', 'calories', 'conseils',
        'diététique', 'conseils alimentaires', 
        'conseils nutritionnels', 'régime', 'équilibre alimentaire'
    ]

    # Détecter les intentions de traçabilité
    tokens = preprocessed_message.split()
    intent = detect_user_intent_from_tokens(tokens)

    # Si l'intention est de traçabilité, retourner l'intention appropriée
    if intent == 'traceability':
        return "LABEL_1"  # TRACEABILITY

    # Vérifications basées sur des phrases clés
    if any(phrase in preprocessed_message for phrase in product_related_phrases):
        return "LABEL_1"  # TRACEABILITY
    if any(phrase in preprocessed_message for phrase in recommendation_phrases):
        return "LABEL_2"  # RECOMMENDATION
    if any(phrase in preprocessed_message for phrase in nutrition_phrases):
        return "LABEL_3"  # NUTRITION_ADVICE

    # Utiliser BERT pour les autres cas
    try:
        result = classifier(preprocessed_message)
        intent = result[0]['label']
    except Exception as e:
        print(f"Erreur lors de la classification de l'intention : {e}")
        intent = "LABEL_UNKNOWN"

    return intent
