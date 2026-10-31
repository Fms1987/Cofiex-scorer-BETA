# Entrega do relatório em .docx (passo final obrigatório)

Ao terminar todas as fases, gravar o relatório completo em `.docx` e entregá-lo ao usuário,
além da resposta no chat. O gerador é `scripts/build_report_docx.py`. Ele recalcula os
subtotais e a Nota Geral a partir dos itens, aplicando o teto da Nota de Área Estratégica, e
assim as tabelas do sumário executivo nunca contradizem os itens.

## Passos
1. Montar um JSON com o esquema abaixo, com os mesmos números da resposta no chat.
2. Rodar `python -X utf8 scripts/build_report_docx.py relatorio.json "Simulacao_COFIEX_<proposta>.docx"`
   (acrescentar `--carta-cliente "Comentarios_<proposta>.docx"` quando houver carta ao cliente).
   (`-X utf8` evita erro de codificação no Windows.)
   Precisa de `python-docx`; se faltar, instalar com `pip install python-docx`. Em ambiente
   sem Python, montar o mesmo documento com a skill de `.docx` disponível, seguindo a mesma
   estrutura.
3. Entregar o arquivo: anexá-lo na resposta ou informar o caminho. A saída deve ficar na
   pasta de trabalho do usuário, não em pasta temporária.

## Regras de redação (valem para o chat e para o .docx)
**Um número em destaque.** O relatório tem um só número principal: a **Nota Geral esperada**,
com a Nota de Área Estratégica esperada logo abaixo. Todo outro número fica em segundo plano e
vem com uma frase que diz quando ele importa:
- faixa: "a nota cai para X se a área principal for lida como C";
- teto de sublimite: "a nota só decide se houver disputa no sublimite Geral";
- dados objetivos: "valor oficial, não muda com a redação da carta".

**Sem previsões paralelas.** Nada de probabilidade de aprovação em percentual, multiplicador
ou taxa de desfecho em primeiro plano. A chance de aprovação aparece como leitura do sublimite,
em texto curto: acima da linha de corte recente, perto dela ou abaixo.

**Cada seção tem um papel só.** Um achado aparece uma vez, na seção dona dele; as outras
remetem a ele ("ver A.5").

| Seção | Papel único | O que não repete |
|---|---|---|
| Resumo para o líder de equipe | Nota esperada, sublimite recomendado, 3 lacunas, 3 ações | Não detalha justificativas |
| Pontuação pela rubrica (seções 4–6) | Por que cada item recebeu a nota | Não propõe correções |
| Revisão sênior e lente Banco Mundial (seção 8) | Qualidade do projeto do ponto de vista de um banco | Não volta a pontuar áreas |
| Plano de Correção (seção 9) | O que mudar, onde e quanto vale | Cita a lacuna por remissão, sem reexplicar |
| Janela e Momento (seção 10) | Onde e quando submeter | Não repete a nota, só a posição frente à linha de corte |

O gerador avisa quando dois parágrafos de seções diferentes são quase iguais (85% ou mais de
semelhança, com 80 caracteres ou mais). Corrigir antes de entregar: manter o texto na seção
dona e trocar o outro por uma remissão.

## Anexos do relatório
- **Carta de comentários ao cliente** (opcional, quando o usuário vai devolver a carta ao
  mutuário). Bloco `carta_cliente` do JSON e opção `--carta-cliente carta.docx`. É uma tabela
  "seção do formulário (Anexo I) → problema → redação sugerida". Não traz nota, sublimite nem
  leitura interna. A redação sugerida sai dos textos-modelo (`review/model-texts.md`) e da
  biblioteca de indicadores. Na versão para o cliente, ela substitui o Plano de Correção; no
  relatório interno o Plano de Correção continua, e a carta não é copiada para ele.

## Painel de carteira
Se o usuário acompanha vários pleitos, registrar cada simulação com
`python -X utf8 scripts/portfolio.py registrar --proposta … --proponente … --nota-geral … --nota-ae … --sublimite … --valor-usd …`
e gerar o painel com `portfolio.py mostrar --html Carteira_COFIEX.html`. O painel mostra, por
pleito:
- nota esperada;
- sublimite recomendado;
- limite da próxima reunião;
- linha de corte recente;
- posição: acima, perto ou abaixo.

O arquivo da carteira fica na pasta de trabalho do usuário.

## Estrutura obrigatória do documento
**Resumo para o líder de equipe** (primeira página, bloco `resumo_ttl`):
- veredito em uma linha;
- Nota Geral esperada em destaque e Nota de Área Estratégica esperada logo abaixo, as duas
  calculadas pelo gerador;
- uma frase de faixa em segundo plano;
- sublimite recomendado;
- as 3 lacunas que mais custam nota;
- as 3 ações de maior ganho, com o ganho rotulado.

Com `resumo_ttl.en`, o resumo sai também em inglês, para circular na equipe do banco.

**Sumário executivo**, com três tabelas separadas:
- **Tabela 1 — Pontuação por item: mínima, esperada e máxima.** Contém:
  - cada item de Dados Objetivos (Nota do Índice de Desenvolvimento Humano até 2,00;
    Capacidade de Pagamento até 2,00; Tendência da Dívida até 1,00) e o subtotal (até 5,00);
  - cada área estratégica e cada bônus, com o subtotal da Nota de Área Estratégica (teto 10,
    ou o teto do ente, com bônus incluído);
  - a **Nota Geral** total.

  Para ente federal não há linhas de Dados Objetivos: usar `"ente_federal": true`.
- **Tabela 2 — Objetivos estratégicos do PPA indicados no pleito e pontuação possível.** Uma
  linha por objetivo. Colunas: código, nome, situação, nível e pontos mín./esp./máx., e o
  fundamento em uma frase. A situação pode ser "Declarada", "Declarada sem sustentação" ou
  "Sugerida — não declarada". Incluir as áreas declaradas que devem sair com nota zero,
  porque mostram onde a carta perde pontos.
- **Tabela 3 — Sugestões a considerar (resumo).** De 5 a 10 linhas curtas: sugestão, item
  afetado, prioridade (P0–P3) e ganho estimado. Sem detalhamento: ele fica na seção Plano de
  Correção.

Depois do sumário, uma seção por item do FORMATO DE SAÍDA (1 a 10) em `secoes`, com os
mesmos títulos por extenso e sem siglas.

## Esquema do JSON
```json
{
  "data": "29/10/2026",
  "versao_skill": "selo de versão exigido pela skill",
  "cabecalho": {
    "proposta": "Nome da proposta",
    "proponente": "Ente",
    "campos": [["Credor", "…"], ["Valor da operação", "US$ …"], ["Contrapartida", "US$ …"],
               ["Sublimite-alvo", "…"], ["Tipo de ente", "Estado / Município / Federal / Estatal"]]
  },
  "sintese": "Duas ou três frases com a conclusão principal.",
  "ente_federal": false,
  "teto_area_estrategica": 10.0,
  "dados_objetivos": [
    {"item": "Nota do Índice de Desenvolvimento Humano (até 2,00)", "min": 1.2, "esp": 1.4, "max": 1.6},
    {"item": "Capacidade de Pagamento (até 2,00)", "min": 2.0, "esp": 2.0, "max": 2.0},
    {"item": "Tendência da Dívida (até 1,00)", "min": 0.5, "esp": 1.0, "max": 1.0}
  ],
  "area_estrategica": {
    "areas": [
      {"codigo": "111", "objetivo": "Cidades sustentáveis", "pleiteado_como": "Declarada",
       "nivel_min": "C", "nivel_esp": "B", "nivel_max": "A",
       "justificativa_curta": "Objetivo geral direto; ~60% dos recursos; impacto alto."}
    ],
    "bonus": [
      {"item": "Prioridade do PPA (Art. 15 §3º)", "situacao": "não pedido / pedido / negado",
       "min": 0, "esp": 0, "max": 1.0},
      {"item": "Integração regional (Art. 15 §4º)", "min": 0, "esp": 0, "max": 0}
    ]
  },
  "base_calibracao": "n=…, filtros…, ancoragem…",
  "faixa_empirica": {"min": 7.4, "max": 11.6},
  "resumo_ttl": {
    "veredito": "Uma linha.",
    "frase_faixa": "A Nota Geral cai para 8,9 se a área principal for lida como C.",
    "sublimite_recomendado": "Ambiental e Climático, se o componente de gestão sair da operação.",
    "lacunas": ["…", "…", "…"],
    "acoes": [{"acao": "…", "ganho": "+1,0 na Nota de Área Estratégica"}],
    "en": {"veredito": "…", "frase_faixa": "…", "sublimite_recomendado": "…",
           "lacunas": ["…"], "acoes": [{"acao": "…", "ganho": "+1.0 Strategic Area Score"}]}
  },
  "carta_cliente": {
    "introducao": "…",
    "itens": [{"secao_anexo": "III. Gestão", "problema": "…", "redacao_sugerida": "…"}],
    "fechamento": "…"
  },
  "sugestoes": [
    {"sugestao": "Tabela de custo por área, produto a produto", "item_afetado": "Área 202",
     "prioridade": "P1", "ganho_estimado": "+0,5 a +1,0"}
  ],
  "secoes": [
    {"titulo": "1. Cabeçalho", "blocos": [
      {"tipo": "p", "texto": "…"},
      {"tipo": "bullets", "itens": ["…", "…"]},
      {"tipo": "tabela", "titulo": "…", "cabecalho": ["…", "…"], "linhas": [["…", "…"]]},
      {"tipo": "nota", "texto": "…"}
    ]}
  ]
}
```
Regras de soma:
- Só entram no subtotal da Tabela 1 as áreas com `pleiteado_como` começando por "Declarada",
  inclusive "Declarada sem sustentação", que tende a zero. Linhas "Sugerida — não declarada"
  aparecem só na Tabela 2.
- Para um esperado entre dois níveis, informar `pontos_min`, `pontos_esp` ou `pontos_max`
  numéricos na área (ex.: `"pontos_esp": 1.5`). Esses valores prevalecem sobre o nível na
  soma, e o nível continua sendo exibido.

- `faixa_empirica` é a faixa de 80% da FASE 9 (Nota Geral esperada ± o valor calibrado). Ela
  aparece como nota abaixo da Tabela 1; as colunas Mínimo e Máximo da tabela são cenários da
  rubrica.

Níveis aceitos: `A` (5), `B` (3), `C` (2), `D` (1), `E` (0,5), `0` (sem nota). Os valores do
JSON usam ponto decimal; o documento sai com vírgula.
