# Application Flask minimale
Cette app sert de base pour les tests de sécurité automatisés (CodeQL, Dependabot) et fait partie des défis CTF.

## Démarrage
```bash
pip install -r requirements.txt
python app.py
```

## Description
Cette application est conçue pour être une cible pour les tests de pénétration et les défis de sécurité. Elle contient plusieurs vulnérabilités intentionnelles pour aider à apprendre et à pratiquer les techniques de sécurisation des applications web.

## Défis
Les défis CTF (Capture The Flag) intégrés dans cette application sont les suivants :

1. **Injection SQL** : Trouvez et exploitez une vulnérabilité d'injection SQL dans l'application.
2. **XSS (Cross-Site Scripting)** : Identifiez une faille XSS et exécutez un script malveillant.
3. **CSRF (Cross-Site Request Forgery)** : Réalisez une attaque CSRF réussie.
4. **Inclusion de fichiers** : Exploitez une vulnérabilité d'inclusion de fichiers pour lire des fichiers sensibles sur le serveur.

## Remarques
- Assurez-vous d'avoir un environnement virtuel Python configuré.
- Ne travaillez pas sur des systèmes en production.
- Respectez les règles d'engagement si vous participez à un CTF organisé.

## Acknowledgements
Cette application utilise des bibliothèques et des frameworks open-source. Merci à tous les contributeurs !

## License
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.