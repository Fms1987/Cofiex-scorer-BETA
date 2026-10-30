# Direcionamento de sublimite (seção 10, Janela e Momento)

Este módulo substitui a antiga "probabilidade de aprovação". A aprovação depende sobretudo de
dois fatores:
- o sublimite escolhido;
- o saldo dele na reunião.

A nota decide apenas dentro de um sublimite disputado: a mesma nota pode aprovar num sublimite
e não aprovar em outro. Mudar de sublimite pode valer mais que ganhar 1 ponto de nota.

Dados:
- `references/strategy/sublimit-table.md`: tabela por reunião e sublimite;
- `reference-data/sublimit_status.json`: limites da próxima reunião e linha de corte recente.

Os dois são gerados por `tools/build_sublimit_table.py` a partir da base consolidada e devem
ser atualizados a cada reunião. Antes de usar, conferir a data de geração no JSON. Se houver
reunião mais recente que a base, dizer isso e pedir ao usuário a ata ou o resultado (FASE 1.6:
o insumo regulado não é presumido).

## Retrato da base (165ª–189ª)
| Sublimite | Pleitos | Aprovados (inclui parciais) | Uso típico do limite na reunião |
|---|---|---|---|
| Subnacional – Geral | 325 | 39% | 96% a 175%: saturado em quase toda reunião |
| Subnacional – Ambiental e Climático | 22 | 68% | 20% a 98%: muitas vezes sobra saldo |
| Subnacional – PPP | 15 | 73% | 19% a 100%: sobra saldo na maior parte das reuniões |
| Subnacional – Fiscal | 13 | 54% | 21% a 100% |
| Subnacional – Reestruturação de Dívidas | 15 | 87% | sem limite próprio |
| Subnacional – Operações em R$ | 8 | 88% | 96% a 98% |

**No sublimite Geral, a linha de corte subiu muito.**
- Sob a RN 1/2024, até a 184ª reunião, a menor nota aprovada ficou entre 6,6 e 9,7.
- Nas reuniões de 2026 subiu para 10,3–11,9. Na 185ª nenhum pleito do Geral foi aprovado, nem
  com Nota Geral 11,9.
- O limite por reunião caiu de cerca de US$ 700 milhões (2025) para US$ 175–270 milhões (2026).

## Passo 1 — Elegibilidade por sublimite
Para cada sublimite, responder "sim", "não" ou "sim, se…". Os critérios abaixo vêm da
experiência da base e das perguntas do Grupo Técnico. **A resolução de sublimites vigente
prevalece**: conferir o texto em vigor na FASE 0 (checagem regulatória) antes de afirmar
elegibilidade.

| Sublimite | Condição de elegibilidade observada | "Sim, se…" típico |
|---|---|---|
| Geral | Projeto de investimento subnacional sem enquadramento específico | — |
| Ambiental e Climático | Recursos integralmente ambientais ou climáticos (deliberação da 170ª reunião); componentes de outra natureza tiram o pleito do sublimite | separar o componente não climático numa operação própria, ou reescrever cada produto com o resultado ambiental ou climático mensurável |
| PPP | Garantia sobre contraprestação de parceria público-privada, com pagamento vinculado a indicadores de nível de serviço, não a entrega de obra (Pergunta 28 do Grupo Técnico, Art. 25 IV) | contrato ou minuta com indicadores de desempenho e mecanismo de pagamento |
| Fiscal | Programa de gestão ou ajuste fiscal do ente | objeto centrado em receita, gasto, dívida ou gestão fiscal, sem obras |
| PEF/RRF, RRF | Ente com Plano de Equilíbrio Fiscal ou em Regime de Recuperação Fiscal; projeto previsto no plano | conferir a situação do ente e se o projeto consta do plano (motivo de não aprovação já registrado) |
| Reestruturação de Dívidas | Troca de dívida com vantagem financeira demonstrada | ver `rubric/final-score.md`: vantagem documentada, Capacidade de Pagamento aprovada, dívida original garantida pela União |
| Operações em R$ | Operação contratada em reais | credor e moeda da operação |
| Federal | Ente federal (administração direta ou estatal) | — |

## Passo 2 — Saldo e linha de corte
Para cada sublimite elegível, ler no JSON:
- o limite divulgado para a próxima reunião;
- a linha de corte recente: a maior entre a menor nota aprovada e a maior nota não aprovada da
  última reunião com notas.

Classificar o pleito pela **Nota Geral esperada** (a mesma do resumo):
- **Cabe no saldo?** Se o valor da operação passa do limite divulgado, o pleito não cabe,
  qualquer que seja a nota. Condição necessária. Limite zero ou "a definir" também vale como
  não cabe.
- **Posição frente à linha de corte.** O erro mediano da Nota Geral no banco de teste é cerca
  de 1 ponto (FASE 9), por isso a régua usa 1 ponto de margem:
  - **acima:** nota esperada pelo menos 1 ponto acima da linha;
  - **perto:** a menos de 1 ponto, para cima ou para baixo;
  - **abaixo:** pelo menos 1 ponto abaixo.
- Sublimite sem nota recente ou sem limite próprio: dizer "sem linha de corte publicada" e
  julgar pelo saldo e pelos critérios do Passo 1.
- Reestruturação de Dívidas: a nota não decide; aplicar os três critérios de `final-score.md`.

## Passo 3 — Recomendação (texto curto, sem percentual)
Escrever de 3 a 5 linhas:
1. **Melhor sublimite e melhor reunião.** O sublimite elegível onde o pleito cabe no saldo e
   fica acima ou perto da linha; a reunião é a próxima com saldo divulgado. Se nenhum servir,
   dizer qual condição falta.
2. **Mudança de desenho para ficar elegível no sublimite menos disputado.** Exemplos:
   - separar um componente climático numa operação própria para o Ambiental e Climático;
   - reduzir o valor ou faseá-lo em duas operações para caber no saldo;
   - estruturar como parceria público-privada com pagamento por desempenho.
   Cada mudança cita o que o ente perde (prazo, escopo, nova carta).
3. **Se ficar no Geral.** Dizer quanto de Nota Geral falta para a linha recente e se o Plano de
   Correção alcança isso. Se não alcança, dizer que a nota sozinha não resolve.

Frases-modelo:
- "No Geral, a linha recente está em torno de 10,3 e a Nota Geral esperada é 8,9: abaixo da
  linha. O Plano de Correção soma até +1,0; não basta."
- "O componente de drenagem e o de áreas verdes somam 62% do valor e têm resultado climático
  mensurável. Separados numa operação de cerca de US$ 50 milhões, ficariam elegíveis no
  Ambiental e Climático, que costuma ter saldo. Limite divulgado para a 191ª: zero; mirar a
  primeira reunião de 2027 e confirmar o limite."

## O que não fazer
- Não mostrar probabilidade em percentual nem multiplicador.
- Não repetir a nota em detalhe: só a posição frente à linha (regra de redação,
  `output/docx-report.md`).
- Não presumir limite de reunião futura que ainda não foi divulgado: dizer "limite não
  divulgado".
- Não citar pleitos concorrentes pelo nome. A tabela é agregada de propósito.
