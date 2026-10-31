# FASE 6 — Índice de Desenvolvimento Humano

## FASE 6 — Índice de Desenvolvimento Humano (apenas subnacional)
`Nota de Índice de Desenvolvimento Humano = 2 × ((1 − IDH_entidade) / (1 − IDH_menor_na_reunião))`

**Primeiro passo:** rodar `python -X utf8 scripts/objective_lookup.py --uf <UF> --reuniao <AAAA-MM-DD>
[--municipio "<nome>"]`. O script lê o IDH das tabelas do Atlas do Desenvolvimento Humano em `reference-data/` (todos os municípios, IDHM 2010; todos os estados, IDHM 2024) e aplica o piso padrão abaixo,
com a faixa. Se a composição da pauta for conhecida, passar `--piso-idh <IDH_menor>`.

### Piso da reunião (IDH_menor), calibrado nas notas oficiais da RN 1/2024
Os pisos abaixo foram tirados das notas oficiais das reuniões 180ª–185ª, invertendo a fórmula. Achado
principal: **municípios são comparados só com municípios, e estados só com estados.**

| Tipo de ente | IDH usado | Piso observado | Padrão |
|---|---|---|---|
| Município | IDHM 2010 | 0,639–0,646 (o mesmo valor para todos os municípios de cada reunião) | **0,643** |
| Estado | IDHM 2024 (Atlas; atualizado com a PNAD) | 0,705–0,762 (média 0,739) | **0,739** |

- O ente que tem o menor IDH entre os pleitos do mesmo tipo na pauta recebe 2,000.
- Estados: o IDHM 2024 reproduz as notas oficiais bem melhor que o de 2021 (desvio do piso 0,013 contra 0,029). O piso ainda varia
  entre reuniões; tratar a nota estadual como ±0,2 ponto. O índice municipal só muda com o Censo; o estadual, com a PNAD.
- Estabilidade do piso 0,739 (conferida nas 23 combinações de reunião e estado da Res. Normativa 1/2024, 180ª a 185ª): o piso
  implícito médio por reunião é 0,745 (180ª), 0,737 (182ª), 0,739 (184ª) e 0,741 (185ª), sem tendência no tempo nem relação com o
  IDH do estado. Com 0,739, o viés é −0,006 e o erro médio 0,071 ponto (20 notas abaixo do teto). A variação vem de poucos
  estados: o Amapá fica em 0,705–0,708 nas duas reuniões em que aparece (erro de 0,2 ponto) e, sem ele, o erro médio cai para 0,056.
  Notas no teto de 2,000 (Maranhão, Piauí) só dão um limite superior para o piso. Manter 0,739; não há ganho em ajustar por reunião.
- A tabela municipal cobre todos os municípios existentes em 2010; os criados depois (por exemplo, Mojuí dos Campos, Pescaria
  Brava, Balneário Rincão, Pinto Bandeira e Paraíso das Águas) ficam sem índice e exigem busca no Atlas.
- Entidades federais: não se aplica (nota 0).
- **Bancos, agências de fomento e estatais de um estado ou município: o índice vale.** Todas as notas oficiais dessas entidades têm
  índice positivo, calculado com o do estado-sede (do município-sede, se o dono for um município). No Distrito Federal usa-se o
  IDHM 2010 de Brasília com o piso municipal (reproduz a nota oficial de uma estatal do Distrito Federal: 0,975).
  Com o estado-sede, as notas oficiais de dois bancos e de uma estatal estadual fecham em 0,05 ponto. Rodar `objective_lookup.py --entidade banco|empresa`.
  Consórcios: usar o ente que os integra.

**Erro com o piso padrão** (mesmas reuniões usadas na calibração, então ligeiramente otimista):
erro médio de 0,01 ponto para municípios (32 notas, os 10 municípios que faltavam na planilha antiga agora entram) e 0,07 para
estados (30 notas, viés −0,02; com o IDH 2021 e piso 0,680 era 0,10). Com os pisos antigos
(0,668 estadual; 0,572–0,620 municipal), o erro era de 0,12 e 0,14, ambos subestimando.

### Por que o viés de −0,29 do teste cego acontecia
Os pisos antigos eram **baixos demais**, sobretudo o municipal (0,572–0,620 contra 0,643 real).
Um piso menor aumenta o denominador e reduz a nota. A instrução anterior de "preferir o extremo
pessimista" (piso ainda mais baixo) agravava o erro e foi removida.

### Faixas de referência (com o piso padrão)
- **Estados (IDHM 2024):** IDH ≤ 0,74 → 2,0; ~0,76 → ~1,84; ~0,80 → ~1,53; ~0,84 → ~1,23.
- **Municípios (IDHM 2010):** ≤ 0,643 → 2,0; 0,700 → ~1,68; 0,750 → ~1,40; 0,800 → ~1,12;
  0,850 → ~0,84.

### Quando mudar o piso
- **Pauta conhecida:** piso = menor IDH entre os pleitos do mesmo tipo na pauta (`--piso-idh`).
- **Pauta com muitos municípios de IDHM muito baixo** (< 0,62): o piso municipal pode cair.
  Mostrar o cenário com o piso menor como o extremo inferior da faixa, sem trocar o padrão.
- Sem evidência, manter o padrão. Não "puxar para o pessimista".
