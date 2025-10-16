# SQL Injection Challenge Solution

## Hint
Test the fields with quotes ' and try `username=' OR '1'='1` etc. Looking at the SQL query in the error response can help.

## Steps to Solve
1. **Craft the Payload**: Use the payload `username=' OR '1'='1' -- ` and any password.
2. **Analyze the Query**: The query becomes `SELECT username FROM users WHERE username = '' OR '1'='1' -- ' AND password='anything';`
3. **Exploit the Vulnerability**: This condition is always true, allowing you to bypass authentication.
4. **Access the Flag**: After logging in, navigate to `/flag` to read the flag.

## Conclusion
This SQL injection allows you to retrieve the first user and access sensitive information.