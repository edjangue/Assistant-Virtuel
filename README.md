
```markdown
# Assistant Virtuel pour la Recommandation et le Suivi des Produits Agro-alimentaires

## Description
Ce projet vise à développer un assistant virtuel basé sur le Machine Learning et l'IA pour recommander et suivre les produits agro-alimentaires. Le chatbot fournit :
- Des **recommandations personnalisées** de produits agro-alimentaires.
- Des informations sur la **traçabilité** des produits.
- Des **conseils nutritionnels personnalisés** pour aider les consommateurs à atteindre leurs objectifs de santé.

---

## Fonctionnalités principales
1. **Suivi de la Traçabilité des Produits :**
   - Permet aux utilisateurs de suivre l'origine, les ingrédients et d'autres informations sur les produits agro-alimentaires.

2. **Recommandation de Produits Agro-alimentaires :**
   - Offre des suggestions personnalisées de produits basées sur les préférences et les besoins des utilisateurs.

3. **Assistance et Conseils Nutritionnels :**
   - Propose des conseils nutritionnels adaptés en fonction de la santé et des préférences alimentaires des utilisateurs.

---

## Installation
1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/edjangue/Assistant-Virtuel.git
   cd Assistant-Virtuel
   ```

2. **Configurer l'environnement virtuel :**
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Linux/Mac
   env\Scripts\activate     # Sur Windows
   ```

3. **Installer les dépendances Python :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Exécuter l'application Flask :**
   ```bash
   python app.py
   ```

5. **Configurer le frontend (React) :**
   ```bash
   cd chatbot1
   npm install
   npm start
   ```

---

## Exécution
- L'application Flask démarre par défaut sur [http://127.0.0.1:5000](http://127.0.0.1:5000).
- Le frontend React démarre sur [http://localhost:3000](http://localhost:3000).
- Pour tester, accédez à l'interface React ou utilisez une API client comme Postman.

---

## Structure du projet
```
ASSIS/
├── chatbot1/               # Dossier pour le frontend (React)
├── env/                    # Environnement virtuel (ignoré dans .gitignore)
├── .gitignore              # Fichier pour ignorer certains dossiers/fichiers dans Git
├── app.py                  # Fichier principal Flask pour l'API
├── conseil.py              # Module pour générer des conseils nutritionnels
├── extract_product.py      # Module pour l'extraction des noms de produits
├── intent_classification.py # Module pour la classification des intentions utilisateur
├── preprocess.py           # Module pour le prétraitement des textes utilisateur
├── recommandation2.py      # Module pour les recommandations de produits
├── requirements.txt        # Liste des dépendances nécessaires au projet
└── traceability.py         # Module pour la traçabilité des produits
```

---

## Technologies utilisées
- **Backend :** Flask (Python)
- **Frontend :** React (JavaScript)
- **Machine Learning :** GPT-4All pour la génération de texte
- **NLP :** SpaCy, Transformers
- **API :** Open Food Facts
- **Autres :** Flask-Caching, Flask-CORS

---

## Configuration requise
- **Python 3.8+**
- **Node.js 14+**
- **npm 6+**
- **Systèmes d'exploitation compatibles :** Windows, macOS, Linux

---

## Utilisation
1. **Recommandations de produits :**
   - Les utilisateurs peuvent saisir leurs préférences et recevoir des suggestions adaptées.

2. **Traçabilité des produits :**
   - Recherchez un produit pour voir son origine, ses ingrédients et autres détails.

3. **Conseils nutritionnels :**
   - Fournissez des informations sur vos objectifs de santé et recevez des conseils personnalisés.

---

## Contributions
Les contributions sont les bienvenues ! Pour contribuer :
1. Clonez le projet.
2. Créez une branche pour vos modifications.
3. Faites une pull request.

---

## Crédits
Ce projet utilise des bibliothèques et API open-source telles que :
- **Open Food Facts** pour les données des produits agro-alimentaires.
- **GPT-4All** pour la génération de texte intelligente.

---
