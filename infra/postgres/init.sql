-- uuid_generate_v4() para gerar IDs únicos
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Busca por similaridade de texto (útil para buscar produtos e clientes)
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Habilita busca full-text em português
CREATE EXTENSION IF NOT EXISTS "unaccent";