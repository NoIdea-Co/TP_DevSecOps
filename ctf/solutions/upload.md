Hint

Essayez d'uploader un fichier .txt contenant du HTML ou un script, puis accédez-le via /uploads/<name>. Parfois un .php est autorisé sur certains serveurs.

Write-up

Upload a file named exploit.txt with content {{'a'}} or HTML that reveals something.

Visit /uploads/exploit.txt. If the app displays content or exposes server paths, escalate.

In this simple CTF, place a file named readme.txt then use path discovery or local inclusion to find flag.txt. (You can tweak challenge to require uploading a web-shell if platform executes uploads — keep safe.)