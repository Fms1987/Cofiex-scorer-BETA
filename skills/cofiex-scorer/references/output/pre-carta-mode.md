# Modo pré-carta (nota conceitual ou rascunho incompleto)

Usar quando o insumo ainda não é uma carta-consulta completa: nota conceitual, apresentação,
termo de referência, rascunho parcial do Anexo I ou uma ideia de projeto descrita pelo usuário.
O objetivo é dizer **o que impede pontuar** e o que escrever primeiro, não dar uma nota que
pareça definitiva.

## Quando entrar no modo (decidido na FASE 1, triagem)
Entrar se valer qualquer uma das condições:
- faltam 2 ou mais seções do Anexo I (I. Projeto, II. Áreas Estratégicas, III. Gestão,
  IV. Riscos, V. Financiamento, VI. Ações Preparatórias, VII. Contatos);
- não há valor por componente ou produto, o que impede o orçamento por área (FASE 5, passo 0);
- não há objetivos do PPA declarados nem objetivo geral e específicos;
- o usuário diz que é rascunho ou nota conceitual.

Avisar no início da resposta: "Modo pré-carta: o texto ainda não permite uma nota completa;
abaixo estão as lacunas que impedem pontuar e uma faixa provisória só do que já é pontuável."

## O que entregar (em vez das seções 4–9 completas)
1. **Mapa do Anexo I.** Uma linha por seção, com:
   - situação: presente, parcial ou ausente;
   - o que falta, em uma frase.
2. **O que já é pontuável.**
   - **Dados Objetivos** (Índice de Desenvolvimento Humano, Capacidade de Pagamento, Tendência
     da Dívida): dependem só do ente e da data da reunião. Calcular normalmente com
     `scripts/objective_lookup.py`.
   - **Nota de Área Estratégica:** só como faixa provisória, larga, por área que já tenha
     objetivo do PPA identificável, sempre rotulada "provisória".
   - Sem orçamento por produto, o teto de cada área fica desconhecido. Dizer isso em vez de
     presumir nível.
3. **Lacunas que impedem pontuar**, em ordem de impacto na nota:

| Lacuna | Item que ela trava | O que escrever | Texto-modelo ou referência |
|---|---|---|---|
| Custo por componente e produto | Nota de Área Estratégica (teto de nível por área) | Tabela produto → valor → área do PPA | planilha `budget_by_area.py --modelo` |
| Objetivos do PPA não escolhidos | Nota de Área Estratégica | Área principal + secundárias com produto e indicador próprios | `calibration/ae-criteria-by-level-and-ppa-area.md` |
| Indicadores sem linha de base, meta ou ano | Nível das áreas; item A.2 | Um indicador de resultado por objetivo específico | `calibration/indicator-library.md` |
| Gestão sem equipe nem matriz | Item A.4; perguntas do Grupo Técnico | Unidade de gestão, equipe, matriz de responsabilidades | `review/model-texts.md` §2 |
| Sustentação sem custo de manutenção | Item A.5 | Tabela plurianual de custo operacional | `review/model-texts.md` §1 |
| Credor e condições não justificados | Perguntas do Grupo Técnico | Por que externo, por que este credor, comparativo | `review/creditor-justification.md` |

4. **Sublimite e momento, já no rascunho.** Aplicar o Passo 1 de
   `strategy/sublimit-targeting.md` (elegibilidade). É no rascunho que se decide separar um
   componente climático, estruturar parceria público-privada ou ajustar o valor ao saldo.
   Depois de escrita a carta, mudar isso custa mais.
5. **Lente Banco Mundial, versão curta.** Na concepção, o mais útil é:
   - instrumento (seção 1);
   - Padrões Ambientais e Sociais que vão exigir estudos com antecedência (seção 3);
   - a subseção de empregos (seção 7), porque reconceber agora é barato.

## O que não fazer
- Não apresentar Nota Geral esperada como número de destaque. No modo pré-carta, o resumo para
  o líder de equipe traz:
  - em destaque, só os Dados Objetivos (valor oficial);
  - a faixa provisória da Nota de Área Estratégica, com a frase "depende das lacunas 1 a 3".
- Não simular as Perguntas do Grupo Técnico por inteiro. Listar só as que o rascunho já
  dispara.
- Não preencher a carta pelo proponente. A redação é tarefa da skill cofiex-pleito-builder.

## Integração com a skill cofiex-pleito-builder
O scorer diagnostica e o builder redige. Ao final, oferecer ao usuário:

> "Para redigir as seções que faltam, use a skill cofiex-pleito-builder com este diagnóstico."

Passar a tabela de lacunas (item 3) como insumo: cada linha vira uma tarefa de redação do
builder. Quando o rascunho voltar mais completo, rodar o scorer de novo no modo normal. A
comparação entre as duas rodadas mostra quanto cada lacuna fechada rendeu.
