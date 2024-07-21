echo db:5432:${POSTGRES_DJANGO_DB_NAME}:${POSTGRES_DJANGO_USER}:${POSTGRES_DJANGO_PASSWORD} > /workspace/backend/.my_pgpass
chmod 600 /workspace/backend/.my_pgpass

echo "[ft_trans]" > ~/.pg_service.conf 
echo "host=db" >> ~/.pg_service.conf 
echo "user=${POSTGRES_DJANGO_USER}" >> ~/.pg_service.conf 
echo "dbname=${POSTGRES_DJANGO_DB_NAME}" >> ~/.pg_service.conf 
echo "port=5432" >> ~/.pg_service.conf 
