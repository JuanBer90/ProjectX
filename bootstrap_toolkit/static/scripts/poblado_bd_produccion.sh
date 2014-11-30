#! /bin/bash
pg_restore -i -h localhost -p 5432 -U postgres -d produccion -v "poblado_tablas_produccion.backup"
