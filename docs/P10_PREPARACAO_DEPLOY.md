# P10 — preparação do deploy do piloto

Esta etapa prepara uma execução PROD isolada; ela não publica o sistema nem
altera o banco usado pelo ambiente DEV.

## Arquitetura mínima

- Frontend: build Vite imutável servido por Nginx.
- Backend: FastAPI/Uvicorn sem `--reload`, com dois workers e sem bind mount.
- Banco: PostgreSQL com volume nomeado separado e migração explícita em serviço
  one-shot (`alembic upgrade head`).
- Proxy/TLS: Caddy na frente do Nginx, somente depois de domínio, DNS e
  política de TLS aprovados. O `deploy/Caddyfile.example` é apenas um modelo.
- Uploads e logs: volumes separados do banco, incluídos no plano de backup.

O `docker-compose.prod.yml` exige variáveis `COREERP_PROD_*`, não fornece
credenciais padrão e publica apenas `127.0.0.1:18080` para validação local.
Em produção, a porta deve ficar atrás do proxy HTTPS e o banco não deve ser
publicado no host.

## Segredos e CORS

Use um secret manager ou o ambiente do host. O arquivo
`deploy/.env.prod.example` contém somente placeholders. A URL PostgreSQL deve
usar senha URL-encoded. `COREERP_PROD_CORS_ORIGINS` deve listar apenas as
origins HTTPS reais do frontend.

## Migração e inicialização

O serviço `migrate` roda `alembic upgrade head` antes do backend. Não use
`stamp` para ocultar divergências e não rode `down -v` em um banco normal.
Uma migração deve ser revisada e testada antes de ser aplicada a uma base
real.

## Backup e restauração

O script `deploy/backup-postgres.sh` usa credenciais fornecidas externamente
por `PGHOST`, `PGPORT`, `PGUSER` e `PGDATABASE` (a senha pode ser fornecida
via mecanismo padrão do PostgreSQL, sem ser gravada no repositório). Ele gera
um dump custom e seu SHA-256. Configure retenção, armazenamento externo e
teste periódico de restauração.

Restaure primeiro em uma instância temporária e isolada, valide a aplicação e
somente então planeje qualquer recuperação. Nunca restaure diretamente sobre
o banco normal do piloto durante esta preparação.

## Rate limit de login

O backend limita falhas de `POST /usuarios/login` por IP, por processo, com
janela e limite configuráveis. O padrão é 10 falhas por 60 segundos; o bloqueio
retorna `429` e `Retry-After`. Login bem-sucedido limpa as falhas daquele IP.

É uma barreira proporcional para um piloto único, não uma solução distribuída:
com múltiplos workers cada processo mantém seu próprio contador. Antes de
escalar horizontalmente, mover o limite para o proxy/edge ou usar um store
compartilhado (por exemplo, Redis) é uma decisão obrigatória. O backend PROD
aceita `X-Forwarded-For` somente porque fica atrás de proxies controlados na
arquitetura proposta; não exponha sua porta diretamente.

## Escolha de infraestrutura ainda pendente

Para um único piloto, as opções são:

1. VPS pequeno + Docker Compose + Caddy: menor custo e controle direto, com
   mais responsabilidade operacional.
2. PaaS para frontend/backend + PostgreSQL gerenciado: menos operação, porém
   custo recorrente e dependência do provedor.
3. Serviço gerenciado de contêineres + PostgreSQL gerenciado: mais escala,
   mas desproporcional antes de validar demanda.

Antes do deploy público, Pedro precisa definir provedor/região, domínio/DNS,
retenção de backups, política de restauração, e onde os segredos serão
armazenados. Nenhuma dessas decisões ou recursos pagos foi criada nesta etapa.
