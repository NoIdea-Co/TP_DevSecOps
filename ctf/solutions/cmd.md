Hint

Tente host=127.0.0.1; cat flag.txt ou host=127.0.0.1 && cat flag.txt selon la shell.

Write-up

Soumettre ?host=127.0.0.1; cat flag.txt provoque l'exécution de cat flag.txt si la commande est interprétée par le shell.

La sortie contiendra la flag.

Mitigation : éviter shell=True, utiliser subprocess.run([...], shell=False) et valider le host (whitelist).

# Command Injection Challenge Solution

## Overview
This challenge tests your ability to exploit command injection vulnerabilities in a web application.

## Steps to Solve
1. **Identify Input Fields**: Look for input fields that may execute system commands.
2. **Inject Commands**: Try injecting commands using various payloads, such as `; ls` or `&& dir`.
3. **Analyze Responses**: Check the application responses to see if your commands are executed.

## Example Payload
- Input: `; ls` or `&& dir`
- Expected Output: A list of files in the server's directory.

## Conclusion
Once you successfully execute commands, you can gather information about the server and potentially access sensitive files.