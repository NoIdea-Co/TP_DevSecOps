# File Upload Challenge Solution

## Hint
Essayez d'uploader un fichier .txt contenant du HTML ou un script, puis accédez-le via `/uploads/<name>`. Parfois un .php est autorisé sur certains serveurs.

## Steps to Solve
1. **Upload a Malicious File**: Upload a file named `exploit.txt` with content like `{{'a'}}` or HTML that reveals server information.
2. **Access the Uploaded File**: Visit `/uploads/exploit.txt`. If the app displays content or exposes server paths, escalate your attack.
3. **Discover the Flag**: In this simple CTF, place a file named `readme.txt` and use path discovery or local inclusion to find `flag.txt`. You can modify the challenge to require uploading a web shell if the platform executes uploads.

## Conclusion
This challenge demonstrates the risks associated with improper file upload handling.