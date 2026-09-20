# Pegs Core — auditoria real e matriz de execução

**Data:** 20/09/2026
**Branch segura:** `codex/pegs-roadmap`
**Commit auditado:** `9aeff80`
**Produção:** não alterada por esta execução

## Escopo e fontes

Esta auditoria compara o código, as migrações, os testes disponíveis e a
validação de staging com as páginas do Notion:

- [Pegs Core — Arquitetura modular e migração da HYPE](https://app.notion.com/p/3e0f7b35dac5810a8499c517a9984e68)
- [CoreERP — Execução Técnica e MVP](https://app.notion.com/p/3dcf7b35dac581e69770d0ab76ff63df)

O estado registrado no Notion foi tratado como hipótese de acompanhamento e
confirmado contra o código. A HYPE continua sendo apenas o primeiro tenant de
referência; novas mudanças devem ser feitas na base reutilizável da Pegs.

## Evidências encontradas

- O backend possui `Empresa`, `empresa_id` nas entidades operacionais, JWT,
  perfis, catálogo de módulos, associação empresa-módulo, auditoria,
  provisionamento protegido por `pegs_admin` e checklist de onboarding.
- Os routers de dashboard, agenda, serviços, profissionais, clientes,
  atendimentos, repasses, financeiro, produtos, estoque, vendas e recursos
  usam a proteção de módulo ativo; login, usuários, empresa e módulos são
  responsabilidades do núcleo.
- As migrações da arquitetura multiempresa e auditoria estão em
  `backend/migrations/versions`, com cadeia linear já validada em PostgreSQL
  temporário no staging.
- A interface carrega nome, logo, tipo de negócio e cores do tenant depois do
  login; a sidebar é filtrada por módulos ativos e o menu do proprietário já
  segue a ordem operacional definida.
- A validação anterior de staging registrou dois tenants isolados, 136 testes
  backend aprovados e 1 ignorado, build de produção do frontend aprovado e
  smoke test das telas principais.
- Nesta conferência, o build do frontend passou novamente e a suíte backend foi
  executada em um ambiente temporário isolado, com 136 testes aprovados e 1
  ignorado. O `.venv` original continua sendo um link quebrado do OneDrive,
  mas isso não impediu a validação automatizada desta rodada.

## Matriz real de execução

| Frente | Status real | Núcleo ou módulo | Dependências | Risco | Próxima ação |
|---|---|---|---|---|---|
| Auditoria e classificação | Concluída e revisada | Núcleo | Código, Notion, staging | Documentação histórica ainda possui percentuais antigos | Manter este arquivo como referência atual |
| Tenant e isolamento | Implementado e validado em staging | Núcleo | `empresa_id`, auth, repositórios e testes | E-mail continua globalmente único; alguns caminhos legados precisam permanecer compatíveis | Ampliar matriz cross-tenant para todos os módulos |
| Perfis e permissões | Implementado | Núcleo | `require_perfil`, vínculo profissional e regras por ação | Ativação de módulo e permissão individual precisam continuar sendo testadas separadamente | Criar matriz de autorização por rota e perfil |
| Módulos por empresa | Implementado | Núcleo | Catálogo, associação, `require_modulo` e UI | Bancos legados sem catálogo usam fallback de compatibilidade | Documentar e testar o bloqueio quando o catálogo estiver ativo |
| Identidade do tenant após login | Implementado parcialmente | Configuração Pegs | `/empresas/me`, shell, tokens | Tokens e classes ainda usam muitos nomes `hype` | Migrar tokens semânticos para `pegs` mantendo aliases de compatibilidade |
| Login da plataforma | Ainda acoplado à HYPE | Núcleo + identidade do tenant | Não há tenant conhecido antes do login | O núcleo da Pegs não deve apresentar a HYPE como marca padrão | Tornar o login neutro da Pegs e manter a marca da empresa no shell pós-login |
| Design System compartilhado | Parcialmente implementado | Núcleo visual | Componentes UI, CSS global, shell | `hype.css` concentra semântica e dificulta temas independentes | Criar tokens `pegs-*` e usar identidade do tenant como camada de aplicação |
| Dashboard | Implementado e validado | Módulo | Dados reais, período, módulos | Ainda há referências históricas ao dashboard piloto | Preservar endpoint e fazer a composição consumir só dados do tenant |
| Agenda e recursos | Implementado e validado | Módulo | Duração, preço, snapshots, recursos e permissões | Feedback de uso real ainda não existe | Aguardar uso real antes de adicionar lembretes ou agenda pública |
| Serviços e profissionais | Implementado | Módulo + configuração | Áreas configuráveis, comissão, status | Compatibilidade com BARBEARIA/TATTOO ainda aparece em utilitários | Generalizar novas áreas sem remover compatibilidade legada |
| Clientes, vendas, produtos e estoque | Funcionais e protegidos | Módulos opcionais | CRUDs, histórico, imagens e movimentos | CRM e regras comerciais avançadas ainda não fazem parte do MVP Pegs | Só priorizar após confirmar necessidade de tenants |
| Financeiro e repasses | Funcionais e protegidos | Módulos opcionais | Snapshots, pagamentos parciais, categorias | Integrações bancárias e estorno ainda pendentes | Manter fora do núcleo até existir demanda real |
| Tenant demonstrativo | Validado em staging | Operação comercial | Seed explícito e provisionamento | Nunca executar seed na HYPE ou em produção | Repetir somente em ambientes isolados |
| Onboarding comercial | Base implementada | Núcleo + operação | Provisionamento, checklist e auditoria | Ainda não há fluxo comercial completo de planos/assinaturas | Documentar o roteiro e testar um novo tenant sem dados HYPE |
| Fase 6 — operação real | Pendente | Produto e operação | Uso real da HYPE e feedback dos responsáveis | Implementar hipótese antes de observar uso gera retrabalho | Registrar feedback, priorizar fricções e converter somente padrões em melhorias reutilizáveis |
| Produção da Pegs | Não iniciada | Infraestrutura | Provedor, DNS, secrets, backup, monitoramento e CI/CD | O domínio antigo da HYPE apresentou redirecionamento indevido | Não publicar até recuperar infraestrutura sob controle do proprietário |

## Decisão de execução

As Fases 0 a 5 possuem implementação técnica e evidência de staging. A próxima
mudança de código será a primeira subetapa prática da base Pegs: separar a
linguagem visual do núcleo da identidade HYPE. Ela não altera APIs, banco,
permissões, snapshots ou regras da operação.

Depois dessa subetapa, a sequência segura é:

1. completar tokens semânticos e login neutro da Pegs;
2. ampliar testes cross-tenant e de módulo/perfil;
3. revisar o shell em desktop/mobile;
4. preparar observabilidade, backup e publicação da Pegs somente com provedor
   definido;
5. iniciar a Fase 6 com feedback real da HYPE, sem inventar funcionalidades.

## Critérios para considerar a auditoria encerrada

- Cada afirmação de conclusão possui evidência de código, teste, staging ou foi
  marcada explicitamente como pendente.
- A produção da HYPE não foi modificada.
- A próxima alteração está limitada ao núcleo reutilizável da Pegs.
- Nenhum dado fictício é introduzido no código de produção.

## Execução desta rodada

- A base visual neutra foi iniciada em `frontend/src/styles/variables.css` e no
  fallback do shell multiempresa.
- O login deixou de apresentar logo, slogan e texto fixos da HYPE quando a
  plataforma ainda não conhece o tenant; passou a usar a marca Pegs e mantém
  `autocomplete` e autofill escuro nos campos.
- A prévia local confirmou a marca Pegs, campos escuros, senha mascarada e a
  mensagem de recuperação de senha.
- `npm run build`, lint direcionado e `git diff --check` passaram.
- O lint completo foi corrigido e passou sem erros ou avisos.
- A suíte backend foi executada no ambiente temporário `pegs-core-test-20260920`:
  136 testes passaram e 1 foi ignorado. Permanecem somente avisos de
  depreciação de dependências.
- A criação do commit foi bloqueada por permissão ao arquivo
  `.git/index.lock`; as alterações permanecem no branch seguro
  `codex/pegs-roadmap` e não foram publicadas.
