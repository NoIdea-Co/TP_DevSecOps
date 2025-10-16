# SQLi — Guide de résolution (scénario en 2 étapes via un seul formulaire)

## Principe
Le formulaire de connexion a deux vulnérabilités distinctes selon les champs fournis:
- Étape 1 (énumération): si vous remplissez uniquement le champ username, le serveur exécute une recherche vulnérable de type `LIKE '%<username>%'` (concaténée, non paramétrée).
- Étape 2 (bypass): si vous fournissez username ET password, alors le username est paramétré (sûr) mais le mot de passe est concaténé tel quel dans la requête.

## Étapes
1) Énumérer les utilisateurs existants
- Dans le champ "Nom d’utilisateur", entrez un motif ou une injection pour lister des comptes, par exemple:
	- `a%`
	- `' OR '1'='1' -- `
- Laissez le champ "Mot de passe" vide puis validez. La page affiche la liste des utilisateurs correspondants.

2) Bypasser le mot de passe pour un utilisateur trouvé
- Reprenez un username vu à l’étape 1 (par ex. `alice`).
- Dans "Mot de passe", injectez un payload qui rend la condition vraie, par exemple:
	- Avec la parenthèse dans la clause password, utilisez par exemple: `' OR '1'='1' )-- `
- Validez: la page de succès s’affiche et montre directement le flag.
 - Attention: si vous vous connectez en tant que `bob` via injection, vous obtenez une page de succès similaire mais sans flag, avec un indice suggérant de vérifier un autre utilisateur (ex: `alice`).

## Exemple de requêtes résultantes
- Énumération (username seul):
	- `SELECT username FROM users WHERE username LIKE '%<input_username>%';`
- Connexion (username paramétré, mot de passe injectable):
	- `SELECT username FROM users WHERE username = ? AND (password = '<input_password>');`

## Exemples concrets
- Pour énumérer:
	- username: `a%` (password vide)
	- username: `' OR '1'='1' -- ` (password vide)
- Pour bypasser:
	- username: `bob`, password: `' OR '1'='1' )-- ` → page de succès sans flag (indice)
	- username: `alice`, password: `' OR '1'='1' )-- ` → page de succès avec flag

## Résultat
En combinant l’énumération (username) puis le bypass (password), vous obtenez une connexion réussie et le flag est affiché immédiatement.