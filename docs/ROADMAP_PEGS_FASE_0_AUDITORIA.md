# Pegs — Fase 0: auditoria e classificação

**Data:** 19/09/2026  
**Branch:** `codex/pegs-roadmap`  
**Baseline:** `63515d9` (`feat: padronizar telas administrativas no visual HYPE`)  
**Produção:** nenhuma alteração realizada. O `main` e `origin/main` continuam no baseline acima.

## Objetivo da auditoria

Mapear o que já existe no CoreERP/HYPE, separar o que é núcleo da Pegs do que é módulo reutilizável ou configuração do tenant e identificar os riscos para a evolução multiempresa. Esta etapa é documental; não altera contratos, dados, comportamento da HYPE ou infraestrutura de produção.

## Fonte de produto e decisões já registradas

O inventário foi comparado com as páginas do Notion:

- [Pegs Core — Arquitetura modular e migração da HYPE](https://www.notion.so/3e0f7b35dac5810a8499c517a9984e68)
- [Pegs — História, visão e evolução da plataforma](https://www.notion.so/3e0f7b35dac58104a48ec00416d327a0)
- [CoreERP — Execução Técnica e MVP](https://www.notion.so/3dcf7b35dac581e69770d0ab76ff63df)
- [CoreERP / Pegs — Produto e Estratégia Comercial](https://www.notion.so/3ddf7b35dac581f58ca1f2ac3955e16f)

Decisões confirmadas:

- Pegs é o núcleo da plataforma.
- Empresa é o tenant, com dados, identidade, regras e módulos próprios.
- HYPE STUDIO é o primeiro tenant real e não deve virar um frontend separado.
- Ativação de módulo é diferente de permissão de usuário.
- Desativar um módulo, serviço ou recurso não pode apagar histórico.
- A identidade HYPE deve ser uma configuração white-label, não uma regra espalhada pelo código.
- A experiência do profissional deve permanecer simples e mobile-first; a do proprietário deve consolidar operação e finanças.

## Inventário atual

### Núcleo existente

Já existe uma base inicial de tenant:

- Tabela/modelo `empresas` com `id`, nome, CNPJ, e-mail, telefone e status ativo.
- `usuarios.empresa_id` e perfil (`admin`, `gerente`, `operador`, `consulta`, `profissional` e `usuario`).
- JWT carrega empresa e perfil; a dependência de autenticação verifica usuário e empresa ativos.
- A maioria dos repositórios e serviços recebe `empresa_id` e filtra as entidades por empresa.
- Há helper `get_empresa_id` para reduzir a passagem manual do tenant em alguns endpoints.
- Rotas de empresa, usuário, login e usuário atual já existem.

Limitações do núcleo atual:

- Não há tabela de módulos habilitados por empresa.
- Não há proteção backend baseada em módulo ativo.
- Não há configuração de identidade da empresa (logo, cores, tema, nome exibido e tipo de negócio) no modelo/API.
- O e-mail de usuário é `unique=True` globalmente; isso impede, por enquanto, o mesmo e-mail em empresas diferentes.
- A criação de empresa existente não cria, no mesmo fluxo, um administrador inicial nem aplica um onboarding.
- Não há trilha de auditoria centralizada para alterações administrativas.
- O token identifica o tenant por payload, mas a autorização efetiva depende da consulta do usuário por e-mail; o desenho futuro deve usar uma identidade/associação multiempresa explícita antes de flexibilizar unicidade.

### Módulos e telas reutilizáveis

O frontend possui rotas e telas para:

1. Login e autenticação.
2. Dashboard executivo e dashboard legado.
3. Agenda, visão diária, novo agendamento e atendimentos.
4. Clientes, cadastro e edição.
5. Serviços.
6. Profissionais e produção do profissional.
7. Recursos da agenda (cadeiras, macas e estações).
8. Repasses/comissões.
9. Financeiro e categorias financeiras.
10. Produtos.
11. Estoque, movimentos e entrada de movimento.
12. Vendas, nova venda e detalhes.
13. Configurações gerais e configuração da operação.

O backend possui routers correspondentes para empresas, usuários, clientes, serviços, profissionais, recursos, agendamentos, atendimentos, repasses, dashboard, financeiro, categorias financeiras, produtos, imagens de produto, estoque e vendas.

### Componentes compartilhados existentes

O shell atual já tem uma camada reaproveitável:

- `MainLayout`, `Sidebar` e `Topbar`.
- `PageHeader`, `SectionCard`, `FormCard` e componentes de botão.
- Inputs, selects, textareas, checkbox, date picker, tabelas, badges, estados vazios, loading, mensagens e diálogo de confirmação.
- Tokens e compatibilidade visual em `frontend/src/styles/variables.css`, `global.css` e `hype.css`.
- Tema visual HYPE aplicado pelo shell através da classe `hype-theme`.

O ponto de evolução é transformar a atual camada HYPE em tokens semânticos da Pegs + tema carregado da empresa, mantendo os componentes e regras de acessibilidade.

### Regras de negócio já comprovadas na HYPE

- Usuários de uma empresa não devem consultar ou alterar dados de outra empresa.
- Profissional fica vinculado a um único cadastro profissional dentro da empresa.
- Profissional agenda e registra atendimento para si; gerente/admin podem operar para os profissionais permitidos.
- A agenda filtra a visão do profissional por área de atuação.
- Serviços possuem preço, duração, categoria, recurso necessário e modo de seleção automático/manual.
- Recursos possuem status ativo, inativo ou manutenção e não devem receber novos agendamentos quando indisponíveis.
- Agendamento grava snapshot de preço e duração; alterações futuras do serviço não alteram o histórico.
- Recursos/serviços usados não devem ser removidos definitivamente; registros não utilizados podem ser excluídos conforme as regras atuais.
- Só quem criou/reservou ou o gerente pode editar/cancelar o agendamento, de acordo com o fluxo já testado.
- Tattoo permite valor informado pelo profissional; o fluxo de barbearia mantém proteção diferente.
- Atendimento grava snapshot financeiro de percentual, valor do profissional e valor da casa.
- Repasses preservam histórico, aceitam pagamentos parciais e impedem excesso.
- Dashboard usa consultas reais por empresa e período, sem necessidade de dados mockados.

### Dados e relacionamentos atuais

Entidades principais identificadas:

| Entidade | Tenant | Histórico/observação |
|---|---:|---|
| Empresa | própria | ainda sem identidade, módulos e auditoria central |
| Usuário | sim | perfil e ativo; e-mail globalmente único |
| Profissional | sim | área BARBEARIA/TATTOO, percentual padrão, ativo |
| Cliente | sim | associado a atendimentos, agendamentos e vendas |
| Serviço | sim | preço, duração, categoria, recurso e ativo |
| RecursoAgenda | sim | nome, tipo, status e ativo |
| Agendamento | sim | datas, status, snapshots, recurso e cancelamento |
| Atendimento | sim | valores e comissão em snapshot |
| Repasse/RepasseItem | sim | valores pagos e vínculo aos atendimentos |
| LançamentoFinanceiro/Categoria | sim | entradas, despesas e status |
| Produto/Imagem/Movimento/Venda/ItemVenda | sim | módulos de produtos, estoque e vendas |

Todas as entidades operacionais verificadas possuem campo `empresa_id` e chaves estrangeiras para `empresas`, mas isso ainda precisa ser validado de forma uniforme nos serviços e nas futuras regras de módulo.

### Classificação de produto

| Item | Classificação | Ação no roadmap |
|---|---|---|
| Login, JWT, sessão, usuário atual | Núcleo Pegs | consolidar no núcleo multiempresa |
| Empresas, isolamento e perfis | Núcleo Pegs | fortalecer associação, auditoria e onboarding |
| Logo, nome exibido, cores, tema | Configuração por empresa | criar configuração white-label |
| Dashboard | Módulo reutilizável | manter dados reais e tema do tenant |
| Agenda e agendamentos | Módulo reutilizável | generalizar serviços, recursos e permissões |
| Clientes | Módulo reutilizável | manter histórico por tenant |
| Serviços | Módulo reutilizável + config do tenant | manter preço/duração/recurso configuráveis |
| Profissionais | Módulo reutilizável + config do tenant | tornar áreas extensíveis e permissões claras |
| Recursos físicos | Módulo reutilizável + config do tenant | preservar manutenção, status e histórico |
| Atendimentos | Módulo reutilizável | manter snapshots e fluxo mobile-first |
| Repasses/comissões | Módulo reutilizável + regra configurável | manter snapshots e visibilidade por perfil |
| Financeiro | Módulo reutilizável opcional | ativar por empresa, sem misturar com permissões |
| Produtos, estoque e vendas | Módulos opcionais | proteger backend e preservar históricos |
| Relatórios, notificações, lembretes, reserva pública | Módulos futuros | não implementar por hipótese nesta etapa |
| Regras `BARBEARIA`/`TATTOO` | Regra a generalizar | trocar condicionais fixas por áreas/configuração quando seguro |
| Nome/logo/assets HYPE e `hype-theme` | Configuração HYPE atual | migrar gradualmente para tema do tenant |

## Acoplamentos HYPE encontrados

Os principais acoplamentos localizados foram:

- Texto e subtítulo HYPE em telas de login, dashboard piloto e configuração da operação.
- Assets HYPE fixos no frontend (`hype-logo-official.png`, `hype-logo-sidebar.png`, hero do login).
- Tokens CSS nomeados `--hype-*` e classe global `hype-theme`.
- Área profissional limitada por constraint a `BARBEARIA` e `TATTOO`.
- Regras de valor do agendamento que reconhecem tattoo por categoria/nome.
- Seed/bootstrap com defaults HYPE usados como primeiro ambiente.
- Testes com dados de HYPE, barbearia e tattoo como cenário de validação.

Classificação: os assets, textos, cores e defaults devem virar configuração inicial da HYPE; as regras de recurso, duração, preço, snapshot e comissão são negócio reutilizável; as áreas e a regra de valor da tattoo precisam de uma decisão de modelagem antes de serem ampliadas.

## Dependências e riscos

### Riscos técnicos

1. Alterar `empresa_id` sem uma migração incremental pode quebrar dados existentes.
2. Remover a unicidade global de e-mail sem uma estratégia de login/tenant pode criar ambiguidade.
3. Esconder menus no frontend sem proteção backend permitiria acesso indevido por API.
4. Converter `hype.css` diretamente em tema global pode afetar o piloto; a migração deve ser por tokens e fallback.
5. A tabela de módulos precisa de catálogo estável e comportamento definido para histórico de módulos desativados.
6. O atual endpoint de criação de empresa é administrativo, mas não é ainda um fluxo comercial/onboarding completo.

### Riscos de produto

1. Ainda não há decisão final sobre quais módulos entram no plano inicial de R$ 100.
2. Produtos, estoque e vendas podem continuar opcionais para o segundo tenant.
3. O segundo tenant deve ser criado apenas em ambiente local/staging, nunca na base de produção da HYPE.
4. Identidade Pegs e white-label HYPE precisam coexistir sem transformar a interface em duas aplicações diferentes.

## Validação de baseline

- `npm run build` em `frontend`: **passou**.
- `npm run lint` completo em `frontend`: **não passou** por 30 erros e 5 avisos preexistentes em arquivos fora desta auditoria. O resultado foi registrado e não será corrigido nesta fase sem escopo específico.
- `python -m pytest -q` em `backend`: **não executou**, pois o interpretador disponível não possui `pytest` instalado. O arquivo raiz `requirements.txt` lista `pytest==9.1.1`; o `backend/requirements.txt` não lista essa dependência de teste.
- Git baseline: branch de trabalho criada a partir de `63515d9`; alterações não relacionadas existentes foram preservadas e não foram adicionadas ao trabalho.
- Produção: **não verificada nem alterada**, conforme regra deste roadmap.

## Lacunas de testes identificadas

Já existem testes relevantes para autenticação, usuários, clientes, serviços, profissionais, agenda, agendamento, atendimento, repasse, dashboard, vendas, estoque e rate limit. Há cenários explícitos de cross-tenant em atendimento, dashboard, profissionais, repasses e agenda.

Ainda faltam, como capacidade da Pegs:

- matriz completa de isolamento para todas as entidades, incluindo produtos, estoque, vendas, financeiro e imagens;
- teste de empresa com módulos ativos/inativos e bloqueio no backend;
- teste da separação entre módulo habilitado e permissão individual;
- teste de identidade/theme por empresa;
- fluxo de criação de empresa + administrador + configuração inicial;
- auditoria de alterações administrativas;
- segundo tenant independente com validação de menu, tema, agenda, clientes e dashboard;
- suíte visual desktop/mobile das telas principais;
- execução automatizada reproduzível do backend em ambiente de desenvolvimento/CI.

## Decisão técnica para a Fase 1

Implementar de forma incremental, sem modificar o comportamento da HYPE até haver cobertura:

1. Introduzir catálogo de módulos e associação `empresa_módulo` com ativação explícita e status.
2. Criar uma dependência única de backend para exigir módulo ativo, aplicada somente após mapear cada endpoint.
3. Separar a atualização da empresa atual da futura configuração de marca, adicionando campos/migração sem apagar valores existentes.
4. Manter `empresa_id` nas entidades atuais e adicionar testes de isolamento onde ainda faltam.
5. Preservar a unicidade global de e-mail nesta primeira migração; discutir associação multiempresa antes de mudar login.
6. Criar auditoria mínima para mudanças administrativas antes de expor a criação de segundo tenant.
7. Manter `hype-theme` como fallback compatível enquanto o frontend passa a consumir configuração da empresa.

## Status da Fase 0

**Concluída em documentação.** O inventário, a classificação, os acoplamentos, os riscos, o baseline de testes e a estratégia segura da Fase 1 estão registrados neste arquivo. Nenhuma regra da HYPE foi alterada e nenhuma publicação foi feita.

**Próxima etapa:** Fase 1 — núcleo multiempresa, começando pelo catálogo/ativação de módulos, configuração de identidade da empresa e cobertura de isolamento/permissões, com migrações reversíveis e testes antes de qualquer uso em produção.
