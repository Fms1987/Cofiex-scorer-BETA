# FASE 5 — rubrica da Nota de Área Estratégica, objetivos do PPA e tratamento de bônus

## FASE 5 — Pontuação das Áreas Estratégicas (Nota de Área Estratégica)

### Passo 0 (obrigatório, antes de classificar qualquer nível) — orçamento por área
A fatia do orçamento é a variável que mais separa os níveis, e estimá-la "de olho" foi a maior
fonte de erro da Nota de Área Estratégica. Calcular sempre:
1. Listar cada produto (ou componente, se a carta não detalhar produtos) com seu valor e as
   áreas do PPA a que a carta o vincula. Usar o quadro de usos e fontes da carta; se houver
   divergência entre texto e anexo, usar o anexo e marcar a inconsistência (ela custa nível).
2. Gravar num JSON e rodar `python -X utf8 scripts/budget_by_area.py <produtos.json>`.
   - Produto com uma área vai inteiro para ela.
   - Produto com várias áreas e sem custo atribuído pela carta é repartido em partes iguais,
     como faz a Nota Técnica. Usar `alocacao` só quando a própria carta atribuir o custo.
3. Colar a tabela do script no detalhamento por área. O **teto pelo orçamento** limita o nível:
   A só acima de 50%, B acima de 30%, C a partir de 15%, D a partir de 4%; abaixo disso, E.
   Teto não é nível. O nível final vem da lente A.6 (objetivo direto, indicador de resultado
   com ano-meta, impacto, inovação) e pode ficar abaixo do teto, nunca acima.
4. Os alertas do script entram no plano de correção: área declarada sem produto próprio
   (tende a zero), produto sem área, repartição linear que derruba a área principal.
5. **Áreas secundárias começam em 0.** Para cada área que não é a principal e tem menos de 15%
   do orçamento, aplicar a regra da seção 4 de `calibration/ae-criteria-by-level-and-ppa-area.md`:
   E só com um vínculo próprio fora da seção de áreas estratégicas (dois nos objetivos que
   quase sempre ficam em 0), teste da soma de cerca de 0,4 ponto por área secundária declarada
   e, na dúvida entre 0 e E, 0. Dar E a áreas que receberam 0 foi o maior erro da Nota de Área
   Estratégica na validação cega.
### Objetivos do PPA 2024–2027 (35)
Eixo 1 — Social: 101 Pobreza · 102 Saúde/SUS · 103 Primeira infância/educação · 104 Ensino
médio/técnico · 105 Economia criativa · 106 Direitos humanos · 107 Mulheres · 108 Indígenas/
quilombolas · 109 Antirracismo · 110 Previdência social · 111 Cidades sustentáveis ·
112 Segurança · 113 Esporte.
Eixo 2 — Econômico: 201 Meio ambiente · 202 Desastres/clima · 203 Agricultura familiar ·
204 Descarbonização · 205 Competitividade · 206 Ciência, Tecnologia e Inovação ·
207 Trabalho · 208 Energia limpa · 209 Digital · 210 Logística · 211 Comércio · 212 Água ·
213 Turismo · 214 Equidade regional · 215 Mineração.
Eixo 3 — Democracia: 301 Transparência · 302 Capacidade estatal · 303 Governo digital ·
304 Defesa · 305 Cooperação internacional · 306 Fiscal · 307 Justiça.
*Prioridades do Art. 15 §3º (elegíveis a bônus): 101, 102, 103, 111, 201, 210, 212.*

### Rubrica — Anexo II + lista de verificação operacional
| Nota | Pontos | Descrição | Lista de verificação (todos SIM) |
|---|---|---|---|
| A | 5 | Direto + SMART + estrutural + maioria dos recursos + inovador | Vínculo direto com o PPA · SMART com linha de base · >50% do orçamento · cronograma viável · inovação |
| B | 3 | Direto + SMART + alto impacto + recursos significativos | Vínculo direto com o PPA · SMART com linha de base · >30% do orçamento · cronograma viável |
| C | 2 | Relevante + SMART + impacto moderado | Relevância para o PPA · indicadores (não totalmente SMART) · algum orçamento |
| D | 1 | Específico + indicadores + baixo impacto | Menção ao PPA · indicadores básicos · orçamento mínimo |
| E | 0,5 | Baixa relevância | relação tangencial com o PPA · sem indicadores/metas |

**SMART (por indicador):** 1. Específico (um único resultado definido) · 2. Mensurável
(fórmula + unidade) · 3. Alcançável (realista frente à linha de base/prazo) · 4. Relevante
(mede o objetivo) · 5. Com prazo definido (ano de linha de base + ano-meta).

**Fatores que movem a Nota de Área Estratégica (anonimizados):**
- Indicadores padronizados/prontos de referência internacional (ISO 37120/22/23; CID-10; IDEB;
  iRAP; DEC/FEC; SNIS) satisfazem o SMART por construção → o preditor mais forte de Nota de
  Área Estratégica ≥ 8,0.
- Um **indicador-âncora de referência nacional** presente em uma carta-consulta multissetorial
  adiciona sistematicamente cerca de +0,5 à estimativa da Nota de Área Estratégica (âncora:
  carta-consulta multissetorial, mix de 7 objetivos estratégicos com 3B + 4C/D, com um
  indicador-âncora nacional → Nota de Área Estratégica ~8,0).
- "Indicadores a serem definidos durante a preparação" / linha de base = 0 por construção →
  nível D–E (típico de repasses genuinamente postergados; NÃO se aplica a fundos com
  indicadores totalmente especificados).
- Linhas de base físicas com metas ano a ano → nível B–A.
- Indicadores apenas de produto ("X sistemas implantados") sem medição de resultado →
  nível C–D.
- Exaustividade técnica ≠ conformidade SMART (uma carta-consulta altamente detalhada com
  indicadores no nível de produto ainda é Nota de Área Estratégica de nível médio).
- O bônus de +1 "100% integral ao PPA" é raro na prática — só cartas-consulta focadas em um
  único setor se qualificam; híbridos multicomponentes não.

`Subtotal = mín(10, Σ) | +prioridade do PPA (faixa, ver bônus) | +Zona de Fronteira (faixa, ver bônus)`
Piso: Nota de Área Estratégica + bônus < 3,0 → eliminatório (apenas subnacional).

### Tratamento de bônus (Art. 15 §3º / §4º) — modelado como uma faixa
Os bônus são incertos até confirmados pela COFIEX/SEAID. Modelar cada um como uma distribuição
discreta **[0 — 0,5 — 2,0]** com peso esperado **0,5** na estimativa probabilística. Aplicar
o **valor cheio apenas quando houver enquadramento documental anexado** (ofício/Portaria que
evidencie o enquadramento, ex.: Lei 6.634/1979 para zona de fronteira). Sem o documento,
carregar o bônus apenas no cenário otimista, não na estimativa-base. Os dois bônus permanecem
limitados juntos dentro do teto de 10 da Nota de Área Estratégica.

**Bônus de Zona de Fronteira — critérios de "presunção forte"** (incluir na estimativa-base,
não no cenário otimista, apenas quando TODOS se verificarem): (1) uma conurbação
transfronteiriça nomeada com cidades específicas do país vizinho; (2) um indicador dedicado e
quantificado de fluxo transfronteiriço; (3) referência explícita à Lei 6.634/1979. Âncora:
município de fronteira que atende aos três critérios → +1,0 (Nota de Área Estratégica ~8,5
contra ~7,5 sem o bônus).
