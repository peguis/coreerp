# Pegs — roteiro de homologação comercial

Status: **preparado; homologação humana pendente**. Este roteiro não cria
credenciais, não convida participantes e não deve ser executado em produção.

## Preparação segura

- Use apenas ambiente local isolado ou staging previamente autorizado e
  identificado como teste.
- Um responsável configura uma conta temporária `vendedor_pegs` e uma conta
  `pegs_admin`; entregar acesso por canal seguro fora do repositório. Não incluir
  senhas, tokens, e-mails pessoais ou dados reais neste registro.
- Use nomes e contatos sintéticos reservados a testes (por exemplo, domínio
  `.invalid`). Não use empresa, cliente ou profissional real.
- Antes do teste, confirme que a Matriz aponta para o banco e API de teste e que
  o tenant HYPE/produção não está selecionado.
- Registre data, versão/commit, ambiente e participantes por papel. Não grave
  segredos nem dados pessoais no relatório.

## Roteiro do vendedor

1. Entrar com a conta temporária de vendedor e confirmar que a navegação oferece
   apenas as funções comerciais permitidas.
2. Tentar abrir a Matriz administrativa e uma área operacional de tenant; ambas
   devem negar ou redirecionar sem revelar dados.
3. Criar uma oportunidade sintética, preencher responsável, tipo de negócio,
   origem, próxima ação e data de retorno; salvar e reabrir.
4. Alterar status e registrar uma interação; confirmar que os campos retornam
   corretos e a auditoria registra a ação.
5. Criar uma demonstração vinculada à oportunidade. Escolher um template,
   revisar os módulos sugeridos e alterá-los antes de confirmar.
6. Manter dados de apresentação desligados no primeiro teste; confirmar que o
   tenant não nasce com clientes, serviços ou outros registros de exemplo.
   Repetir apenas em outra demo descartável com a opção explicitamente ligada e
   conferir que os dados ficam identificados como apresentação.
7. Abrir a prévia e o login do tenant demo. Confirmar nome, identidade e módulos
   selecionados; confirmar que a demo não mostra dados HYPE ou de outra empresa.
8. Atualizar a página/repetir a ação de criação com a mesma submissão apenas em
   ambiente descartável; não deve haver duplicação de demo por duplo envio.
9. Solicitar conversão e confirmar que o vendedor não consegue ativar sozinho a
   empresa real nem aprovar a própria solicitação.

## Roteiro do administrador Pegs

1. Entrar com `pegs_admin` e localizar a oportunidade e solicitação pendentes.
2. Conferir os dados definitivos da empresa e da conta administradora antes da
   aprovação; rejeitar valores incompletos ou inesperados.
3. Aprovar uma conversão somente no ambiente isolado de teste.
4. Confirmar que foi criado um tenant real separado, que a demo permaneceu
   marcada como demo, e que ambos continuam ligados à oportunidade e à auditoria.
5. Arquivar uma demo descartável e confirmar que ela fica inativa, o histórico
   permanece preservado e o login do tenant deixa de aceitar acesso.
6. Repetir abertura de oportunidade/demo de outro vendedor: dados privados devem
   continuar isolados, salvo a visão administrativa prevista para `pegs_admin`.

## Critérios observáveis de sucesso

- Login dos dois papéis funciona no ambiente de teste e a navegação respeita as
  permissões.
- Vendedor só consulta e altera as próprias oportunidades/demonstrações.
- O tenant demo nasce isolado e vazio por padrão; dados de apresentação exigem
  escolha explícita.
- Repetir uma submissão não cria tenants duplicados.
- A prévia informa que é demonstração; o login pertence ao tenant correto.
- Conversão exige solicitação, aprovação administrativa e confirmação explícita.
- A empresa real tem identidade/registro separado; a demo e os dados históricos
  não são promovidos nem apagados.
- Ações importantes aparecem na auditoria sem senhas, tokens ou conteúdo sensível.
- Erros e estados vazios deixam claro como prosseguir, sem ação decorativa.

## Perguntas de feedback

- Em que passo você precisou parar ou pedir ajuda?
- O que você esperava que acontecesse depois de cada ação?
- Os nomes “oportunidade”, “demonstração”, “prévia” e “conversão” ficaram claros?
- Você percebeu que a demo não é uma empresa ativa? A tela de aprovação deixou
  claro que a criação real é uma ação administrativa?
- Quais informações estavam faltando para apresentar o sistema com confiança?
- Qual problema impediria você de usar o fluxo novamente? Qual melhoria seria
  apenas conveniente?

## Registro de sessão

Preencher depois da participação real, sem inventar resultados:

| Campo | Registro |
|---|---|
| Data / commit | Pendente |
| Ambiente (local/staging) | Pendente |
| Papéis que participaram | Pendente |
| Cenários executados e evidência sem dados pessoais | Pendente |
| Resultado por critério (passou/falhou/não testado) | Pendente |
| Bloqueios, passo para reproduzir e impacto | Pendente |
| Feedback literal autorizado ou síntese aprovada | Pendente |
| Próxima decisão / responsável | Pendente |

Não declarar homologação concluída até um vendedor/parceiro executar os cenários
e fornecer feedback real. Bugs técnicos observados devem ser reproduzidos em
ambiente de teste e registrados separadamente de preferências ou pedidos de
produto.
