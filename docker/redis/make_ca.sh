openssl req -x509 -days 3650 -nodes -newkey rsa:4096 -keyout /etc/tls/redis.key -out /etc/tls/redis.crt -config - << __EOF__
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
#openssl x509 -in /etc/tls/redis.crt -noout -text

# CA証明書と秘密鍵の生成
#openssl genrsa -out /tmp/ca-key.pem 4096
#openssl req -x509 -new -nodes -key /tmp/ca-key.pem -sha256 -days 3650 -out /tmp/ca-cert.pem


openssl genrsa -out /etc/tls/ca-key.pem 4096
openssl req -x509 -new -nodes -key /etc/tls/ca-key.pem -sha256 -days 3650 -out /etc/tls/ca-cert.pem   -config - << __EOF__
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



# サーバー用の証明書と秘密鍵の生成
openssl genrsa -out /etc/tls/server-key.pem 4096
openssl req -new -key /etc/tls/server-key.pem -out /etc/tls/server.csr   -config - << __EOF__
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

openssl x509 -req -in /etc/tls/server.csr -CA /etc/tls/ca-cert.pem -CAkey /etc/tls/ca-key.pem -CAcreateserial -out /etc/tls/server-cert.pem -days 3650 -sha256


# サーバー用の証明書と秘密鍵の生成
#openssl genrsa -out /etc/tls/server-key.pem 4096
#openssl req -new -key /etc/tls/server-key.pem -out /etc/tls/server.csr  -config - << __EOF__
#[req]
#distinguished_name = req_distinguished_name
#prompt = no
#
#[req_distinguished_name]
#C = JP
#ST = Aichi
#L = Toyota-shi
#O = 42
#OU = 42tokyo
#CN = hsano.42.fr
#
#[v3_req]
#keyUsage = TestInception
#extendedKeyUsage = serverAuth
#subjectAltName = @alt_names
#
#[alt_names]
#DNS.1 = mydomain.example
#DNS.2 = sub.mydomain.example
#__EOF__
#
#
#
#openssl x509 -req -in /etc/tls/server.csr -CA /etc/tls/redis.crt -CAkey /etc/tls/redis.key -CAcreateserial -out /etc/tls/server-cert.pem -days 3650 -sha256
#
#
#
#
