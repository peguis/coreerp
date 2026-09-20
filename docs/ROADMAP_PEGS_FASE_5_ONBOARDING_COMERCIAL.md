# Pegs — Fase 5: onboarding e operação comercial

**Estado:** base operacional preparada em ambiente local/staging  
**Produção HYPE:** não publicada nem alterada

## Objetivo

Deixar a Pegs pronta para demonstrar e configurar novos negócios sem criar uma
aplicação separada para cada cliente. A criação de tenants continua sendo uma
ação controlada do `pegs_admin`; não existe cadastro público automático.

## Fluxo de implantação de um novo tenant

1. O `pegs_admin` provisiona a empresa com nome, CNPJ, e-mail, tipo de negócio,
   identidade inicial e administrador.
2. O backend cria o tenant, o administrador, os vínculos dos módulos ativos e
   o registro de auditoria em uma transação.
3. O administrador entra no tenant e acompanha o checklist em
   `/configuracoes`.
4. O administrador ou gerente configura identidade, módulos e permissões dos
   usuários.
5. A equipe cadastra serviços, durações, preços, profissionais e recursos.
6. A operação valida clientes, agenda, atendimentos, repasses e financeiro.
7. Antes da publicação, a equipe executa os testes e registra a aprovação do
   responsável pelo negócio.

## Checklist de onboarding

- [ ] Identidade: nome, logo, cores e tipo de negócio.
- [ ] Usuários: administrador, gerente e profissionais necessários.
- [ ] Módulos: ativar somente o que faz parte da operação.
- [ ] Permissões: confirmar que cada perfil vê e executa somente o permitido.
- [ ] Serviços: nome, categoria, duração, preço e recurso necessário.
- [ ] Profissionais: área de atuação, ativação e comissão padrão.
- [ ] Recursos: identificação individual, status ativo/manutenção/inativo.
- [ ] Clientes: cadastrar os primeiros clientes reais ou importar dados aprovados.
- [ ] Agenda: criar e alterar um agendamento, validar conflitos e snapshots.
- [ ] Atendimentos: concluir um fluxo operacional completo.
- [ ] Repasses e financeiro: validar valores, pendências e histórico.
- [ ] Acesso: testar login, logout e tentativa de acesso entre tenants.

O checklist exibido pela aplicação considera identidade, administrador, módulos,
serviço e profissional como itens obrigatórios. O primeiro agendamento é
acompanhado como item opcional de validação.

## Suporte inicial

### Antes da ativação

- Confirmar responsável, contatos e tipo de negócio.
- Confirmar módulos contratados ou previstos.
- Registrar identidade e regras comerciais fornecidas pelo cliente.
- Criar o tenant somente em ambiente autorizado.

### Durante a configuração

- Acompanhar o checklist de onboarding.
- Validar dados sem inserir informações fictícias na produção.
- Registrar decisões específicas como preço, duração, comissão e recurso.
- Reproduzir erros com o tenant e o identificador do registro afetado.

### Após a validação

- Registrar data, responsável e resultado dos testes.
- Confirmar backup e restauração conforme o runbook de deploy.
- Entregar credenciais por canal seguro, nunca em código ou logs.
- Manter histórico de alterações e reativação de módulos.

## Base para planos e cobrança futura

O núcleo já separa empresa, módulos e auditoria, mas planos, assinatura e
cobrança ainda não estão definidos nem devem ser inventados. Antes de criar
integrações comerciais, decidir:

- módulos por plano;
- preço e periodicidade;
- limites de usuários, agenda e armazenamento;
- período de teste e suspensão;
- política de suporte e implantação;
- provedor de cobrança e emissão fiscal.

## Critério de passagem para produção

Esta fase só pode ser encerrada após revisão visual desktop/mobile, execução dos
testes finais, conferência de backup/restauração, aprovação do usuário e decisão
explícita sobre o ambiente de publicação. Nenhum script deste documento publica
ou altera a base da HYPE automaticamente.
