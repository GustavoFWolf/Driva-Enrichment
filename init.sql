/*Tabela de seed da API para test*/
CREATE TABLE api_enrichments_seed (
  id UUID PRIMARY KEY,
  id_workspace UUID,
  workspace_name TEXT,
  total_contacts INTEGER,
  contact_type TEXT,
  status TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

/*Bronze*/
CREATE TABLE bronze_enrichments (
  id UUID PRIMARY KEY,
  payload JSONB NOT NULL,
  dw_ingested_at TIMESTAMP NOT NULL,
  dw_updated_at TIMESTAMP NOT NULL
);

/*Gold*/
CREATE TABLE gold_enrichments (
  id_enriquecimento UUID PRIMARY KEY,
  id_workspace UUID,
  nome_workspace TEXT,
  total_contatos INTEGER,
  tipo_contato TEXT,
  status_processamento TEXT,
  data_criacao TIMESTAMP,
  data_atualizacao TIMESTAMP,
  duracao_processamento_minutos NUMERIC,
  tempo_por_contato_minutos NUMERIC,
  processamento_sucesso BOOLEAN,
  categoria_tamanho_job TEXT,
  necessita_reprocessamento BOOLEAN,
  data_atualizacao_dw TIMESTAMP
);

/*insere 5000 dados fake na tabela api_enrichments_seed*/

INSERT INTO api_enrichments_seed
SELECT
  gen_random_uuid(),
  gen_random_uuid(),
  'Workspace ' || i,
  (random() * 1500)::int + 1,
  CASE WHEN random() > 0.5 THEN 'COMPANY' ELSE 'PERSON' END,
  (ARRAY['COMPLETED','FAILED','PROCESSING','CANCELED'])[floor(random()*4)+1],
  now() - (random() * interval '5 days'),
  now()
FROM generate_series(1, 5000) i;
