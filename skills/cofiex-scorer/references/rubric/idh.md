# FASE 6 — Índice de Desenvolvimento Humano

## FASE 6 — Índice de Desenvolvimento Humano (apenas subnacional)
`Nota de Índice de Desenvolvimento Humano = 2 × ((1 − IDH_entidade) / (1 − IDH_menor_na_reunião))`

**Primeiro passo:** rodar `python -X utf8 scripts/objective_lookup.py --uf <UF> --reuniao <AAAA-MM-DD>
[--municipio "<nome>"]`. O script lê o IDH da planilha empacotada e aplica o piso padrão abaixo,
com a faixa. Se a composição da pauta for conhecida, passar `--piso-idh <IDH_menor>`.

### Piso da reunião (IDH_menor), calibrado nas notas oficiais da RN 1/2024
Os pisos abaixo foram tirados das notas oficiais das reuniões 180ª–185ª, invertendo a fórmula. Achado
principal: **municípios são comparados só com municípios, e estados só com estados.**

| Tipo de ente | IDH usado | Piso observado | Padrão |
|---|---|---|---|
| Município | IDHM 2010 | 0,639–0,646 (o mesmo valor para todos os municípios de cada reunião) | **0,643** |
| Estado | IDH estadual | 0,676–0,689 | **0,680** |

- O ente que tem o menor IDH entre os pleitos do mesmo tipo na pauta recebe 2,000.
- Para alguns estados, o IDH que a SEAID usa diverge do IDH 2021 da planilha em até ~0,03.
  Tratar a nota estadual como ±0,1 ponto.
- Entidades federais: não se aplica (nota 0). Estatais e consórcios: usar o ente mantenedor (FASE 2).

**Erro com o piso padrão** (mesmas reuniões usadas na calibração, então ligeiramente otimista):
erro médio de 0,01 ponto para municípios e 0,10 para estados, sem viés. Com os pisos antigos
(0,668 estadual; 0,572–0,620 municipal), o erro era de 0,12 e 0,14, ambos subestimando.

### Por que o viés de −0,29 do teste cego acontecia
Os pisos antigos eram **baixos demais**, sobretudo o municipal (0,572–0,620 contra 0,643 real).
Um piso menor aumenta o denominador e reduz a nota. A instrução anterior de "preferir o extremo
pessimista" (piso ainda mais baixo) agravava o erro e foi removida.

### Faixas de referência (com o piso padrão)
- **Estados:** IDH 0,676–0,690 → 1,9–2,0; IDH ~0,72 → ~1,75; IDH ~0,77 → ~1,4; IDH 0,80–0,83 → 1,1–1,25.
- **Municípios (IDHM 2010):** ≤ 0,643 → 2,0; 0,700 → ~1,68; 0,750 → ~1,40; 0,800 → ~1,12;
  0,850 → ~0,84.

### Quando mudar o piso
- **Pauta conhecida:** piso = menor IDH entre os pleitos do mesmo tipo na pauta (`--piso-idh`).
- **Pauta com muitos municípios de IDHM muito baixo** (< 0,62): o piso municipal pode cair.
  Mostrar o cenário com o piso menor como o extremo inferior da faixa, sem trocar o padrão.
- Sem evidência, manter o padrão. Não "puxar para o pessimista".
