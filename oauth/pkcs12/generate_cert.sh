openssl req -x509 -newkey rsa:4096 -sha256 -days 3560 -nodes -keyout server.key -out server.crt -subj '/CN=localhost' -extensions san -config <( \
  echo '[req]'; \
  echo 'distinguished_name=req'; \
  echo '[san]'; \
  echo 'subjectAltName=DNS:localhost')
openssl pkcs12 -export -out certificate.pfx -inkey server.key -in server.crt
