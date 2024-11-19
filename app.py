#app1.py
from flask import Flask, request, jsonify
from preprocess import preprocess_text
from intent_classification import classify_intent
from traceability import get_product_traceability, detect_user_intent_from_tokens
from extract_product import extract_product_name
from conseil import generate_nutrition_advice
from recommandation2 import get_product_recommendations
import logging
from flask_caching import Cache
from flask_cors import CORS
from gpt4all import GPT4All
from typing import Optional


class AIResponseGenerator:
    def __init__(self):
        # Initialiser le modèle GPT4All
        self.model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")
        # Requête de préchauffage
        _ = self.generate_ai_response("Warm-up test prompt", max_tokens=1)

        
    def generate_ai_response(self, 
                           prompt: str, 
                           max_tokens: int = 200,
                           temperature: float = 0.3) -> Optional[str]:
        """
        Génère une réponse IA basée sur le prompt fourni
        """
        try:
            
            # Collect all generated tokens into a string
            response_text = ""
            for token in self.model.generate(
                prompt,
                max_tokens=max_tokens,    # Augmenté pour des réponses plus complètes
                temp=temperature,       # Température modérée pour un bon équilibre créativité/cohérence
                top_k=20,          # Augmente la diversité des réponses
                top_p=0.8,          # la créativité     
                repeat_penalty=1.2  # Évite les répétitions
            ):
                response_text += token
            
            # Vérification pour détecter si la réponse est incomplète
            if len(response_text.strip()) < 10 or response_text.endswith("..."):
                return "Je n'ai pas pu générer une réponse complète. Veuillez réessayer ou vérifier les informations demandées."
        
            return response_text.strip()
        
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse IA: {str(e)}")
            return "Une erreur s'est produite lors de la génération de la réponse."
            

    def generate_response(self, 
                          context: str, 
                          user_message: str, 
                          response_length: str = 'priority') -> Optional[str]:
        """
        Génère une réponse IA en deux étapes, d'abord prioritaire puis complète.
        """
        try:
            # Première étape : réponse prioritaire
            max_tokens = 200 
            top_p = 0.8  # Augmenter pour retour rapide
            prompt = f"""Contexte: {context}
            Question utilisateur: {user_message}
            Réponse courte avec les informations essentielles:"""
        
            # Génération de la première réponse rapide avec les éléments prioritaires
            initial_response = self.generate_ai_response(prompt, max_tokens=max_tokens, temperature=0.3, top_p=top_p)
        
            # Si la réponse initiale est suffisante, on la retourne directement
            if response_length == 'priority':
                return initial_response.strip()

            # Seconde étape : Ajouter plus de détails
            prompt += "\nRéponse plus détaillée et explicative:"
            detailed_response = self.generate_ai_response(prompt, max_tokens=200, temperature=0.5, top_p=0.8)
        
            return f"{initial_response.strip()} {detailed_response.strip()}"
        
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse IA: {str(e)}")
            return "Une erreur s'est produite lors de la génération de la réponse."



    def enhance_traceability_response(self, product_name: str, trace_info: str) -> str:
        """
        Améliore la réponse de traçabilité avec l'IA
        """
        prompt = f"""En tant qu'assistant spécialisé dans la traçabilité alimentaire, voici la réponse détaillée pour:
        
        Produit: {product_name}
        Informations de traçabilité: {trace_info}
        
        Réponse:"""
        
        
        response = self.generate_ai_response(prompt)
        return response if response else trace_info

    def enhance_nutrition_advice(self, preferences: dict, base_advice: str) -> str:
        """
        Améliore les conseils nutritionnels avec l'IA
        """
        context = f"""En tant que nutritionniste virtuel, créez des conseils personnalisés basés sur:
        
        Préférences alimentaires: {preferences}
        Conseils de base: {base_advice}
        
        Incluez:
        1. Des suggestions de repas spécifiques
        2. Des alternatives alimentaires adaptées
        3. Des explications sur les bienfaits
        4. Des conseils pratiques quotidiens
        
        Réponse:"""
        
        response = self.generate_ai_response(context)
        return response if response else base_advice

    def enhance_recommendations(self, preferences: dict, recommendations: list) -> str:
        """
        Améliore les recommandations de produits avec l'IA
        """
        context = f"""En tant qu'expert en alimentation, voici les recommandations:
        
        Préférences utilisateur: {preferences}
        Produits recommandés: {recommendations}
        
        inclus:
        1. Une explication détaillée de chaque recommandation
        
        
        Réponse:"""
        
        response = self.generate_ai_response(context)
        return response if response else str(recommendations)

# Initialisation de Flask et du générateur IA
app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'SimpleCache'  # Utilise un cache en mémoire simple
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Durée de vie des entrées en cache : 300 secondes (5 minutes)
cache = Cache(app)

ai_generator = AIResponseGenerator()

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)

# État de la conversation pour chaque utilisateur
user_states = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_id = data.get('user_id')
    user_message = data.get('message', '').lower()
    user_intent_click = data.get('intent_click')

    if not user_id or (not user_message and not user_intent_click):
        return jsonify({"message": "Requête invalide"}), 400
    
    cache_key = f"{user_id}:{user_message}"  # Générer une clé unique pour chaque combinaison utilisateur-question

    # Vérifier si une réponse est déjà en cache
    cached_response = cache.get(cache_key)
    if cached_response:
        print("Réponse récupérée depuis le cache.")  # Debug : Indique si le cache a été utilisé
        return jsonify({"message": cached_response})
    

    if user_id not in user_states:
        user_states[user_id] = {
            'step': 0,
            'preferences': {},
            'conversation_context': []
        }

    user_state = user_states[user_id]
    step = user_state['step']

    # Ajouter le message au contexte
    if user_message:
        user_state['conversation_context'].append({"user": user_message})

    # Gestion des intentions par clic
    if user_intent_click:
        intent = user_intent_click.upper()
        if intent == "TRACEABILITY":
            user_state['step'] = 6
            response = "Quel produit souhaitez-vous avoir les informations ?"
            return jsonify({"message": response})
        elif intent == "RECOMMENDATION":
            user_state['step'] = 1  # Commencer directement par le type de produit
            response = "Dans quelle catégorie de produits cherchez-vous des recommandations ? (par exemple, snacks, boissons, produits laitiers)"
            return jsonify({"message": response})
        elif intent == "NUTRITION_ADVICE":
            user_state['step'] = 8 # Commencer directement par le type de produit
            response = "Avez-vous des préférences alimentaires spécifiques ? (par exemple, végétarien, sans gluten, sans lactose, etc.)"
            return jsonify({"message": response})
        else:
            response = f"Vous avez choisi : {intent}. Veuillez continuer."
            user_state['step'] = 0  # Réinitialiser l'étape pour les autres options
            return jsonify({"message": response})


    # Traitement selon le contexte pour la recommandation
    if step == 1:  # Attente du type de produit
        user_state['preferences']['product_category'] = user_message
        user_state['step'] += 1
        response = "Y a-t-il des ingrédients que vous souhaitez éviter ? (par exemple, sucre, gluten, lactose)"
        return jsonify({"message": response})

    elif step == 2:  # Attente des préférences alimentaires
        user_state['preferences']['avoid_ingredients'] = user_message.split(',')
        user_state['preferences']['avoid_ingredients'] = [ingredient.strip() for ingredient in user_state['preferences']['avoid_ingredients'] if ingredient.strip()]
        user_state['step'] += 1
        response = "Avez-vous une préférence pour le Nutri-Score ? (A, B, C, D, E)"
        return jsonify({"message": response})

    elif step == 3:  # Attente des allergies
        user_state['preferences']['min_nutriscore'] = user_message.upper()
        user_state['step'] += 1
        response = "Quel est votre seuil pour l'Eco-Score ? (A, B, C, D, E)"
        return jsonify({"message": response})
   
    
    elif step == 4:  # Recommandations
        user_state['preferences']['min_ecoscore'] = user_message.upper()
        user_preferences = user_state['preferences']
        # Générer une clé unique basée sur les préférences utilisateur
        cache_key = f"recommendations:{str(user_state['preferences'])}"

         # Vérifier si les recommandations sont en cache
        cached_recommendations = cache.get(cache_key)
        if cached_recommendations:
            print("Recommandations récupérées depuis le cache.")  # Debug
            return jsonify({"message": cached_recommendations})
        
        recommendations = get_product_recommendations(user_preferences)
        enhanced_recommendations = ai_generator.enhance_recommendations(
            user_preferences, 
            recommendations
        )
        user_states.pop(user_id)

        # Stocker les recommandations en cache
        cache.set(cache_key, enhanced_recommendations)


        return jsonify({"message": enhanced_recommendations})


    # Traitement selon le contexte pour la traçabilité
    if step == 6:  # Attente du nom du produit pour la traçabilité
        product_name = extract_product_name(user_message)
        if product_name:
            user_state['product_name'] = product_name  # Stocker le nom du produit
            user_state['step'] += 1
            response = "Que voulez-vous savoir sur ce produit ?"
        else:
            response = "Je n'ai pas compris le produit. Pouvez-vous répéter ?"
        return jsonify({"message": response})

    elif step == 7:  # Traçabilité
        user_intent = detect_user_intent_from_tokens(preprocess_text(user_message))
        trace_info = get_product_traceability(user_state['product_name'], user_intent)
        enhanced_response = ai_generator.enhance_traceability_response(
            user_state['product_name'], 
            trace_info
        )
        user_states.pop(user_id)
        return jsonify({"message": enhanced_response})
    
    if step == 8:  # Attente des préférences alimentaires
        user_state['preferences']['dietary_preferences'] = user_message.split(',')
        user_state['preferences']['dietary_preferences'] = [preference.strip() for preference in user_state['preferences']['dietary_preferences'] if preference.strip()]
        user_state['step'] += 1
        response = "Y a-t-il des ingrédients que vous souhaitez éviter en raison d'allergies ou d'intolérances ? (par exemple, noix, soja, gluten, etc.)"
        return jsonify({"message": response})
    elif step == 9:  # Attente des allergies
        dietary_restrictions = user_message.split(',')
        user_state['preferences']['allergies'] = [restriction.strip() for restriction in dietary_restrictions if restriction.strip()]
        user_state['step'] += 1
        response = "Avez-vous des objectifs de santé particuliers ? (par exemple, réduire le sucre, augmenter les fibres, etc.)"
        return jsonify({"message": response})


    elif step == 10:  # Conseils nutritionnels
        health_goals = user_message.split(',')
        user_state['preferences']['health_goals'] = [goal.strip() for goal in health_goals if goal.strip()]
        user_preferences = user_state['preferences']
        base_conseil = generate_nutrition_advice(user_preferences, user_id)
        enhanced_conseil = ai_generator.enhance_nutrition_advice(
            user_preferences, 
            base_conseil
        )
        user_states.pop(user_id)
        return jsonify({"message": enhanced_conseil})

    

    # Traitement par défaut
    tokens = preprocess_text(user_message)
    intent = classify_intent(user_message)
    user_intent = detect_user_intent_from_tokens(tokens)

    intent_mapping = {
        'LABEL_1': 'TRACEABILITY',
        'LABEL_2': 'RECOMMENDATION',
        'LABEL_3': 'NUTRITION_ADVICE'
    }
    intent = intent_mapping.get(intent, "UNKNOWN")

    # Générer la réponse appropriée selon l'intention
    if intent == 'TRACEABILITY':
        product_name = extract_product_name(user_message)
        trace_info = get_product_traceability(product_name, user_intent)
        response = ai_generator.enhance_traceability_response(product_name, trace_info)

    elif intent == "RECOMMENDATION":
        user_state['step'] = 1  # Commencer directement par le type de produit
        response = "Dans quelle catégorie de produits cherchez-vous des recommandations ? (par exemple, snacks, boissons, produits laitiers)"
        return jsonify({"message": response})

    elif intent == 'NUTRITION_ADVICE':
        user_state['step'] = 8 
        response = "Avez-vous des préférences alimentaires spécifiques ? (par exemple, végétarien, sans gluten, sans lactose, etc.)"
        return jsonify({"message": response})
    
    else:
         # Fixed: Properly providing both arguments to generate_quick_response
        default_message = "Je ne suis pas sûr de comprendre votre demande. Pourriez-vous la reformuler ?"
        response = ai_generator.generate_response("default", default_message)

    # Stocker la réponse en cache
    cache.set(cache_key, response)

    return jsonify({"message": response})

if __name__ == '__main__':
    app.run(debug=True)