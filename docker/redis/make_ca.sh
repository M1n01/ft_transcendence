openssl genrsa 4096 > ca.key
openssl rsa -text -noout -in ca.key
openssl rsa -in ca.key -pubout -out ca-public.key

ssh-keygen -f id_rsa.pub -e -m pem
openssl req -new -key ca.key -subj "/CN=rootca" > ca.csr
openssl x509 -text -noout -in ca.crt
openssl req -x509 -new -nodes -key ca.key -subj "/CN=rootca" -sha256 -days 10000 -out ca.crt


openssl genrsa 4096 > server.key
openssl rsa -text -noout -in server.key
openssl rsa -in server.key -pubout -out server-public.key
openssl req -new -key server.key -subj "/CN=servername" > server.csr
openssl req -text -noout -in server.csr

#openssl req -new -key server.key  -out server.csr -config - << __EOF__
#[ req ]
#default_bits = 2048
#prompt = no
#default_md = sha256
#req_extensions = req_ext
#distinguished_name = dn
#
#[ dn ]
#CN = servername
#
#[ req_ext ]
#subjectAltName = @alt_names
#
#[ alt_names ]
#DNS.1 = othername1
#DNS.2 = othername2
#
#[ v3_ext ]
#authorityKeyIdentifier=keyid,issuer:always
#basicConstraints=CA:FALSE
#keyUsage=keyEncipherment,dataEncipherment
#extendedKeyUsage=serverAuth,clientAuth
#subjectAltName=@alt_names
#__EOF__

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 10000 -out server.crt
#openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 10000 \
  #-extensions v3_ext -extfile csr.conf \
  #-out server.crt
  #
openssl x509 -text -noout -in server.crt


cp server.key /etc/tls/server.key
cp server.crt /etc/tls/server.crt
cp ca.crt /etc/tls/ca/ca.crt
cp ca.key /etc/tls/ca/ca.key