openssl req -x509 -days 3650 -nodes -newkey rsa:4096 -keyout /tmp/server.key -out /tmp/server.crt -config - << __EOF__
[req]
distinguished_name = req_distinguished_name
prompt = no

[req_distinguished_name]
C = JP
ST = Aichi
L = Toyota-shi
O = 42
OU = 42tokyo
CN = hsano.42.fr

[v3_req]
keyUsage = TestInception
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = mydomain.example
DNS.2 = sub.mydomain.example
__EOF__

# 証明書の内容を確認
#openssl x509 -in /etc/nginx/server.crt -noout -text
#cp /etc/nginx/server.crt /var/www/html/
#chown user42 /var/www/html/server.crt
#chmod 777 /var/www/html/server.crt
