#! /bin/bash
pg_restore -i -h localhost -p 5432 -U postgres -d postgres -v "poblado_tablas_desarrollo.backup"
