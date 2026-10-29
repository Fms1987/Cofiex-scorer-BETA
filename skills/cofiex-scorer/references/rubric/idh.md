# FASE 6 — Índice de Desenvolvimento Humano

## FASE 6 — Índice de Desenvolvimento Humano (apenas subnacional)
`Nota de Índice de Desenvolvimento Humano = 2 × ((1 − IDH_entidade) / (1 − IDH_menor_na_reunião))`

**CRÍTICO:** a nota é RELATIVA à composição da reunião — não pode ser calculada sem saber quem
mais está pautado. Apresentar sempre como uma faixa de cenário. A âncora de piso fixo de
conveniência abaixo é um PADRÃO apenas para reuniões com predomínio estadual; ela nunca
substitui a fórmula relativa quando a composição da pauta é conhecida, e nunca sobrepõe os
pisos municipais.

### Âncora padrão para reunião estadual
Para reuniões com predomínio estadual e composição desconhecida, usar o piso **0,668** como
base, com:
- Pessimista 0,650 · Base 0,668 · Otimista 0,686 (limite superior 0,700 para pautas dominadas
  por estados de alto Índice de Desenvolvimento Humano do Sul/Sudeste ou litoral do Nordeste).
Sobrepor apenas com evidência da composição real da pauta (marcado como tal).

### Cenários calibrados (corpus 180ª–187ª reunião)
| Cenário | IDH_menor | Usar quando |
|---|---|---|
| Pessimista | 0,646–0,650 | Reunião tem estado do Norte/Nordeste com Índice de Desenvolvimento Humano muito baixo |
| Moderado (padrão estadual) | 0,668 | Padrão para reuniões com predomínio estadual |
| Otimista | 0,686–0,700 | Nenhum estado abaixo do piso de alto Índice de Desenvolvimento Humano |
| Municipal | 0,572–0,620 | Reunião inclui municípios de Índice de Desenvolvimento Humano Municipal baixo (pisos preservados) |

**Faixas empíricas — estados:** Índice de Desenvolvimento Humano baixo (0,639–0,689) → 1,7–2,0;
médio (0,660–0,665) → 1,3–1,9; alto (0,740–0,826) → 0,5–1,2. Âncora: estado do Nordeste com
Índice de Desenvolvimento Humano ≈ 0,689 que é praticamente o piso da reunião (IDH_menor ≈
0,686) → ≈ 1,98.

**Faixas empíricas — municípios (Índice de Desenvolvimento Humano Municipal) — pisos
preservados, NÃO sujeitos à âncora estadual de 0,668:**
- ≤ 0,600 (muito baixo) → 1,8–2,0 (quase máximo se for o menor da reunião)
- 0,650–0,699 (baixo) → 1,5–1,8
- 0,700–0,710 (médio-baixo) → 1,4–1,7 (piso ~0,619–0,646); até ~1,98 se for o menor
- 0,750–0,770 (médio) → 1,2–1,4 (piso ~0,580–0,620)
- 0,760–0,799 (médio-alto) → 0,9–1,4
- ≥ 0,800 (alto) → 0,4–0,9
Âncoras (anonimizadas): município com Índice de Desenvolvimento Humano Municipal 0,759, piso
da reunião ≈ 0,619 → **1,335**; município com Índice de Desenvolvimento Humano Municipal
0,700, piso semelhante → **1,695**.

**Estimativa prática:** quando a composição da reunião é desconhecida, usar a âncora estadual
de 0,668 para pautas estaduais; para pautas municipais ou mistas usar piso 0,620–0,650; ajustar
para cima (→1,9+) se a entidade for demonstravelmente o menor Índice de Desenvolvimento Humano
da pauta, para baixo (→0,5–1,2) se houver entidades de Índice de Desenvolvimento Humano menor
presentes.

Entidades federais: Índice de Desenvolvimento Humano = não se aplica (nota 0).

**Viés sistemático de subestimação (achado da validação por teste cego, n=15, 2026-10).** A Nota
de Índice de Desenvolvimento Humano cega saiu, em média, 0,29 ponto (escala 0–2) abaixo da nota
oficial — o único componente objetivo com viés direcional consistente (CAPAG e Dívida saíram
quase sem viés no mesmo teste). Como a fórmula é relativa ao IDH_menor da reunião real (não
conhecido às cegas), a hipótese mais provável é que os pisos-âncora acima (0,668 estadual;
0,572–0,620 municipal) estão, em média, ligeiramente **altos demais** — mais perto do IDH da
própria entidade do que o IDH_menor real costuma ser, o que comprime a nota calculada para baixo.
**Ajuste recomendado:** na ausência de evidência da composição real da pauta, preferir o extremo
**pessimista** de cada faixa de cenário (não o moderado) como ponto de partida — ex.: usar
0,650–0,660 em vez de 0,668 para pautas estaduais, e o piso inferior das faixas municipais. n=15
é pequeno; tratar como ajuste preliminar e revisar com mais casos de validação.
