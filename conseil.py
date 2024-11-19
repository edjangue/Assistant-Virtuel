#conseil.py

def generate_nutrition_advice(user_preferences, user_id):
    """
    Génère un conseil nutritionnel de base en fonction des préférences de l'utilisateur.
    
    :param user_preferences: Dictionnaire contenant les préférences de l'utilisateur, 
                             y compris les préférences alimentaires, allergies, et objectifs de santé.
    :param user_id: ID de l'utilisateur pour un suivi spécifique.
    :return: Conseil nutritionnel de base en texte.
    """
    dietary_preferences = user_preferences.get('dietary_preferences', [])
    allergies = user_preferences.get('allergies', [])
    health_goals = user_preferences.get('health_goals', [])
    

    # Introduire l'identifiant de l'utilisateur si disponible
    greeting = f"Bonjour utilisateur {user_id} !" if user_id else "Bonjour !"
    advice = greeting + "\nVoici des conseils personnalisés :\n"
    
    if dietary_preferences:
        advice += f"- Privilégiez une alimentation adaptée à vos préférences : {', '.join(dietary_preferences)}.\n"
    if allergies:
        advice += f"- Évitez les ingrédients suivants en raison d'allergies : {', '.join(allergies)}.\n"
    if health_goals:
        advice += f"- Pour vos objectifs de santé, voici quelques conseils : {', '.join(health_goals)}.\n"
        
    return advice