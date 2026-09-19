# Pegs — Fases 4 e 5: empresa-demo e operação comercial

**Branch de desenvolvimento:** `codex/pegs-roadmap`  
**Produção HYPE:** não alterada e não publicada

## Objetivo

Preparar uma segunda empresa independente para demonstração e deixar o produto
com uma base segura de onboarding. A empresa-demo deve usar os mesmos módulos da
Pegs, mas ter identidade, usuários, serviços, profissionais, recursos, clientes
e agenda próprios.

## O que foi implementado

### Fase 4 — empresa-demo isolada

- `backend/app/seeds/create_demo.py` cria uma empresa-demo somente quando
  executado explicitamente.
- Os dados são lidos de variáveis `COREERP_DEMO_*`; não há seed automático na
  inicialização da API e nenhum dado-demo é inserido na HYPE.
- A criação é transacional: conflito de CNPJ/e-mail não altera registros e
  falha de commit faz rollback.
- A nova empresa recebe módulos próprios e pode receber, por configuração,
  serviço, profissional, recurso, cliente e agendamento de validação.
- O agendamento grava duração e preço aplicados na criação, seguindo o mesmo
  snapshot usado pela HYPE.

### Fase 5 — onboarding operacional

- `GET /empresas/me/onboarding` retorna um checklist por empresa.
- A configuração inicial acompanha identidade, administrador, módulos, serviço,
  profissional e primeiro agendamento opcional.
- A tela Configurações exibe o percentual e o estado de cada item.
- A criação de empresa/administrador continua fora do fluxo público; o bootstrap
  permanece explícito por ambiente e sem exposição de senha.
- O perfil `pegs_admin` foi separado do administrador da empresa. Ele pode ser
  criado somente pelo bootstrap explícito e usa `POST /empresas/provisionar` para
  criar um novo tenant com administrador e módulos em uma transação.
- A checagem de conflito do seed foi corrigida para considerar somente o e-mail
  efetivamente existente; a presença de administradores em outros tenants não
  bloqueia a criação de uma empresa-demo nova.

## Como validar uma empresa-demo local/staging

Defina as variáveis `COREERP_DEMO_*` para a empresa de teste, sem reutilizar
credenciais ou identificadores da HYPE. Os campos opcionais de serviço,
profissional, recurso, cliente e agendamento permitem validar o fluxo completo.
Depois execute o seed somente no banco local/staging e confirme:

1. login do administrador-demo;
2. identidade visual e módulos próprios;
3. criação/edição de serviço, profissional e recurso;
4. criação e alteração de agendamento;
5. ausência dos clientes, usuários, serviços, recursos e agendamentos da HYPE;
6. bloqueio de acesso cruzado entre os dois tenants;
7. checklist de onboarding em `/configuracoes`.

## Evidência de staging — 19/09/2026

Foi criado um PostgreSQL temporário e isolado em `127.0.0.1:55437`, fora da
produção e sem reutilizar o `.env` da HYPE. A cadeia Alembic foi aplicada online
até `a3b4c5d6e7f8`.

- HYPE de staging criada como tenant de referência.
- `Studio Demo Staging` criada como segundo tenant persistido.
- HYPE: nenhum serviço, profissional, recurso, cliente ou agendamento-demo.
- Demo: 1 serviço, 1 profissional, 1 recurso, 1 cliente e 1 agendamento.
- Demo: 12 vínculos de módulos ativos e onboarding em 100%.
- HYPE: onboarding em 60% por não possuir dados operacionais de demonstração.
- Login, `/empresas/me`, onboarding e `/modulos/` responderam corretamente nos
  dois tenants.
- Segunda execução do seed retornou conflito sem duplicar empresa ou dados.
- Provisionamento adicional registrou 12 módulos e auditoria
  `PROVISIONAR_EMPRESA` na mesma transação.

O cluster temporário foi usado apenas para validação controlada e não representa
ambiente público.

O script não deve ser executado contra o banco de produção. A publicação da
Pegs continua condicionada à revisão final e à confirmação explícita do usuário.

## Pendências antes da conclusão do roadmap

- finalizar a revisão visual de todas as páginas no design system oficial,
  incluindo evidência desktop/mobile;
- revisar a criação comercial de tenants e planos/assinaturas;
- executar build, lint direcionado, testes e revisão final da HYPE;
- apresentar o diff/commit final ao usuário e aguardar confirmação antes de
  qualquer deploy.
