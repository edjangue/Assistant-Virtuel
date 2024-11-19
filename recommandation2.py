#recommandation.py

import requests
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ProductPreferences:
    category: Optional[str] = None
    avoid_ingredients: List[str] = None
    min_nutriscore: str = 'e'
    min_ecoscore: str = 'e'

    def __post_init__(self):
        if self.avoid_ingredients is None:
            self.avoid_ingredients = []
        self.avoid_ingredients = [ing.lower() for ing in self.avoid_ingredients]
        self.min_nutriscore = self.min_nutriscore.lower()
        self.min_ecoscore = self.min_ecoscore.lower()

class OpenFoodFactsAPI:
    BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"
    
    @staticmethod
    def get_search_params(page_size: int = 50) -> Dict:
        return {
            'search_simple': 1,
            'json': 1,
            'sort_by': 'popularity',
            'page_size': page_size,
            'action': 'process'
        }

    @staticmethod
    def fetch_products() -> Optional[Dict]:
        try:
            headers = {'Accept': 'application/json'}
            params = OpenFoodFactsAPI.get_search_params()
            
            response = requests.get(
                OpenFoodFactsAPI.BASE_URL,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            return None
        except ValueError as e:
            print(f"JSON Parsing Error: {str(e)}")
            return None

class ProductRecommender:
    @staticmethod
    def meets_criteria(product: Dict, preferences: ProductPreferences) -> bool:
        if not product.get('product_name'):
            return False

        # Vérification de la catégorie
        if preferences.category:
            categories = [cat.lower() for cat in product.get('categories_tags', [])]
            if preferences.category.lower() not in categories:
                return False

        # Vérification des ingrédients à éviter
        ingredients_text = product.get('ingredients_text', '').lower()
        if any(ingredient in ingredients_text for ingredient in preferences.avoid_ingredients):
            return False
        
        # Vérification du Nutriscore
        product_nutriscore = product.get('nutriscore_grade', 'e').lower()
        if product_nutriscore > preferences.min_nutriscore:
            return False

        # Vérification de l'Ecoscore
        product_ecoscore = product.get('ecoscore_grade', 'e').lower()
        if product_ecoscore > preferences.min_ecoscore:
            return False
            
        return True

    @staticmethod
    def get_recommendations(preferences: ProductPreferences, limit: int = 5) -> List[Dict]:
        data = OpenFoodFactsAPI.fetch_products()
        if not data or 'products' not in data:
            return []

        recommendations = []
        for product in data['products']:
            if ProductRecommender.meets_criteria(product, preferences):
                recommendations.append({
                    'name': product['product_name'],
                    'brand': product.get('brands', 'Unknown brand'),
                    'nutriscore': product.get('nutriscore_grade', 'unknown'),
                    'ecoscore': product.get('ecoscore_grade', 'unknown'),
                    'ingredients': product.get('ingredients_text', 'No ingredients listed')
                })

                if len(recommendations) >= limit:
                    break

        return recommendations

# Exemple d'utilisation
def get_product_recommendations(preferences_dict: Dict) -> List[Dict]:
    preferences = ProductPreferences(
        category=preferences_dict.get('category'),
        avoid_ingredients=preferences_dict.get('avoid_ingredients', []),
        min_nutriscore=preferences_dict.get('min_nutriscore', 'e'),
        min_ecoscore=preferences_dict.get('min_ecoscore', 'e')
    )
    
    return ProductRecommender.get_recommendations(preferences)
    