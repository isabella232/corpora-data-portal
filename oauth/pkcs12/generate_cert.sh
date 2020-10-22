openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
openssl pkcs12 -export -out certificate.pfx -inkey server.key -in server.crt
