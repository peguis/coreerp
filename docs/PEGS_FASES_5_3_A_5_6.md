# Pegs — Fases 5.3 a 5.6

Documento de execução local da Matriz Pegs. A branch de referência é
`codex/pegs-roadmap`, commit inicial `d8c6a11` (23/09/2026). O objetivo é
preparar validações sem publicar, acessar produção, usar dados reais ou declarar
homologação sem retorno humano.

## Plano, dependências e critérios

| Fase | Entrega | Dependências/bloqueios | Critério de conclusão |
|---|---|---|---|
| 5.3 | Inventário de prontidão e instruções seguras para futuro ambiente demo | Publicação depende de provedor, domínio/DNS, TLS, credenciais e autorização | Separar o que existe do que falta; nenhuma alteração pública |
| 5.4 | Roteiro e formulário de homologação comercial | Resultado depende de vendedor/parceiro testar e enviar feedback | Cenários observáveis documentados; homologação permanece pendente |
| 5.5 | Auditoria UX/UI da Matriz, incluindo loading, e correções visuais de baixo risco se verificáveis | Revisão visual desktop/mobile depende de navegador utilizável | Evidências e backlog; nenhuma regra/API/permissão alterada |
| 5.6 | Revisão de segurança/operação, testes e correções de achados confirmados | Staging, backup real e revisão operacional dependem de ambiente/autorização | Testes locais reproduzíveis; pendências externas explicitadas |

## Fase 5.3 — preparação de ambiente público de demonstração

**Estado: preparação local documentada; nenhum ambiente público foi criado.**

### Confirmado no repositório

- Existe um modelo de deploy em `docker-compose.prod.yml`, Caddy em
  `deploy/Caddyfile.example` e variáveis sem credenciais reais em
  `deploy/.env.prod.example`. As variáveis `COREERP_PROD_*` são fornecidas pelo
  ambiente; não foi lido nem alterado `.env` local.
- CORS valida a lista de origens e rejeita `*`. O modelo requer a origem HTTPS
  real antes de publicação.
- `/healthz` executa `SELECT 1`; indica indisponibilidade do banco com HTTP 503,
  mas não substitui monitoramento de aplicação ou dependências externas.
- A migração `i9j0k1l2m3n4` foi exercitada em PostgreSQL descartável local na
  validação de 23/09/2026: upgrade, repetição, rollback e reaplicação; dados
  preexistentes de empresas/oportunidade permaneceram preservados. Isso não é
  validação em staging.
- Demonstrações são tenants próprios (`eh_demo`), com isolamento por empresa.
  Dados de apresentação são opcionais e só entram por seleção explícita.
- Arquivar uma demo marca o tenant como inativo e preserva os dados. Não há
  reset/limpeza automatizada; não excluir dados por improviso.
- Identidade da empresa aceita `logo_url`; o cadastro de demonstração não faz
  upload de logo. O upload existente é apenas de imagens de produtos.
- Há script de backup PostgreSQL custom com hash (`deploy/backup-postgres.sh`),
  mas não foi encontrado script automatizado de restauração, retenção ou cópia
  externa. A restauração precisa ser ensaiada em banco temporário antes de uso.
- Logs são gravados em `logs/coreerp.log` e stdout, sem rotação configurada no
  código. O rate limit de login guarda contadores em memória por processo; atrás
  de múltiplas instâncias é necessário limite compartilhado/edge confiável.
- HTTPS está previsto como arquitetura via proxy/Caddy, mas domínio, DNS,
  certificado e política de exposição continuam sem configuração real.

### Pronto localmente

- Modelo de variáveis e topologia de deploy documentados sem segredos.
- Política de CORS restrita e health check com dependência do banco identificados.
- Provisionamento e migração de Fase 5.2 validados em ambiente isolado local.
- Produção HYPE e qualquer infraestrutura pública permaneceram intocadas.

### Bloqueios para publicar posteriormente

1. Pedro precisa escolher provedor/região e domínio; configurar DNS e autorizar a
   política de acesso (público, allowlist ou acesso privado).
2. Fornecer/configurar segredos no secret manager do provedor, nunca no Git:
   URL/credencial PostgreSQL, chave JWT e origens CORS finais.
3. Confirmar o tenant demo, conta(s) temporária(s), duração/expiração e processo
   de encerramento. O sistema atual não reseta dados automaticamente.
4. Definir volumes persistentes para uploads/logs, retenção e destino externo de
   backups; implementar e ensaiar restauração isolada antes de depender dela.
5. Decidir limites de abuso/acesso público e rate limit compartilhado antes de
   expor mais de uma instância.
6. Autorizar explicitamente qualquer criação de recurso, staging público ou
   deploy. Nenhum desses itens foi executado nesta fase.

## Fase 5.4 — preparação da homologação comercial

**Estado: roteiro preparado; homologação real pendente.** Ver
`docs/PEGS_HOMOLOGACAO_COMERCIAL.md` para cenários, critérios e formulário de
feedback. Nenhum vendedor foi contatado ou convidado e nenhuma credencial foi
criada para uso público.

## Fase 5.5 — UX/UI da Matriz Pegs

**Estado: auditoria de código concluída; inspeção visual desktop/mobile pendente.**
As telas existentes incluem Dashboard, Empresas, Provisionamento, Detalhe,
Auditoria, Oportunidades, criação de demonstração e prévia. A base já tem
breakpoints responsivos, cartões mobile para oportunidades, foco global visível,
estados de loading/skeleton/erro/retry/vazio e semântica `role=status/alert`.
- Achado concreto: no wizard de criação, os passos 1 e 2 anunciavam “Criar
  demonstração” mesmo apenas avançando e não permitiam voltar para revisar os
  dados. Corrigido com rótulos de ação por passo e botão “Voltar etapa”.
- O ajuste alterou somente a interface de `MatrizCriarDemonstracao.jsx`; payload,
  API, permissões e regras de negócio foram preservados.
- Validação: ESLint direcionado, build frontend e 6 testes de identidade passaram;
  o build mantém aviso do bundle JavaScript >500 kB.
- A janela do navegador não foi liberada para automação, portanto não declaro
  conferência visual de desktop/mobile. Conferir a navegação corrigida em ambos
  quando o ambiente visual estiver disponível.

## Fase 5.6 — segurança e operação

**Estado: revisão de código/testes em andamento.** Registrar aqui apenas achados
reproduzidos, correções e comandos/ambientes efetivamente usados. Revisão de
staging, restauração real e homologação permanecem separadas de validação local.
