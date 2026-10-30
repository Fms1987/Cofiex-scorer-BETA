# FASE 9 — Nota final

## FASE 9 — Nota Final
`Total = mín(10, Nota de Área Estratégica + bônus) + Índice de Desenvolvimento Humano +
Capacidade de Pagamento + Dívida` (subnacional, máx. 15). Federal = apenas Nota de Área
Estratégica.
Apresentar como **[Mínimo — Esperado — Máximo]**.

**Faixa empírica (padrão de apresentação).** A faixa pela rubrica (soma do pior e do melhor
caso de cada item) cobriu a nota oficial em só 65% dos 89 pleitos do teste cego, com largura
mediana de 3,0. A faixa calibrada pelos erros observados é mais honesta:
- **Nota Geral:** esperada ± 2,1 cobre ~80% dos casos (± 1,7 cobre ~70%; erro mediano 1,1).
- **Nota de Área Estratégica:** esperada ± 2,2 cobre ~80% (n=30, ainda fraco).
- Cortar nos limites da escala (0 a 15; 0 a 10).
Mostrar a faixa empírica de 80% como [Mínimo — Esperado — Máximo]. A faixa pela rubrica vai
para segundo plano, com uma frase dizendo o cenário que leva a cada extremo (ex.: "a nota cai
para X se a área principal for lida como C"). Os valores ± são atualizados por
`tools/run_regression.py` a cada rodada do banco de teste fixo (campo `faixa_empirica`).

**Teto prático = 15,0.** Manter o teto total em 15,0 por padrão. Os bônus são absorvidos
dentro do teto de 10 da Nota de Área Estratégica. Se evidência documental de acúmulo de bônus
implicar um valor acima de 15, marcar como **teto extensível** com probabilidade BAIXA,
pendente de confirmação explícita da COFIEX/SEAID — não pontuar acima de 15 por padrão.

**Padrão de âncora (testes cegos anonimizados, NR 1/2024):** a Nota de Área Estratégica é o
componente de maior variância (≈3,5–9,0); o Índice de Desenvolvimento Humano beneficia
entidades do Norte/Nordeste em até +2,0; a Capacidade de Pagamento discrimina A+ (2,0) contra
B+ (1,0); a Dívida varia com a Dívida Consolidada/Receita Corrente Líquida histórica. Exemplos
de total confirmado (perfis anonimizados): investimento de município-capital ≈ 10,6;
investimento + refinanciamento de município de fronteira ≈ 11,9; reestruturação/Dívida Pública
Interna/Externa fiscal estadual ≈ 6,7 — **todos aprovados** (o último confirma aprovação
independente da nota para a modalidade de reestruturação).

**Reestruturação de Dívida/Dívida Pública Interna ou Externa — aprovação independente da
nota.** A nota é irrelevante para o desfecho; o que determina a aprovação é: (1) vantagem
financeira documentada (anexos comparativos obrigatórios); (2) Capacidade de Pagamento
aprovada (A+/A/B+/B); (3) a dívida original já garantida pela União (sub-rogação da garantia).
Com os três presentes, a aprovação é ≈ 100% independentemente da Nota de Área Estratégica.

**Modificadores (projetos de investimento) — uso interno, nunca como número no relatório.**
Pela regra de redação (`output/docx-report.md`), estes fatores só orientam a leitura em texto
da seção Janela e Momento: acima da linha de corte recente, perto dela ou abaixo. Não mostrar
percentual de aprovação nem o multiplicador. O módulo de sublimite (saldo e linha de corte por
reunião) vai substituí-los.
- valor da operação > 0,15 × teto → ×0,7; valor da operação > 0,25 × teto → ×0,3
- Primeiro trimestre após virada de ciclo → probabilidade geral = máx(5%, base × 0,1)
- Banco Mundial no sublimite Geral → ×0,9 (padrão de porte do valor da operação)
- 2º reenvio visando o quarto trimestre → ×1,15 (teto 95%); 3º+ reenvio → ×0,6
- Valor da operação comprimido em mais de 50% entre reenvios → ×1,2
- Mesmo texto de carta-consulta reenviado → nota inalterada; a probabilidade depende
  inteiramente do saldo do teto + concorrentes.
- Bônus aplicado com peso esperado 0,5, salvo quando houver enquadramento documental anexado
  (então valor cheio).

**Ressalvas:** estimativas de ordem de grandeza (5 reuniões da NR 1/2024, n≈140 + análise de
iteração sobre 15 reuniões + validação formal com retenção de amostra n=52+22). A
incerteza dominante é o saldo do teto na data da reunião, não a nota — **confirmado
empiricamente**: na rodada de validação com retenção de amostra, o TOTAL médio
previsto foi estatisticamente indistinguível entre casos reais Aprovados e reais Não aprovados
(9,70 contra 9,50/15), e o filtro do Art. 28 isoladamente previu APROVADO quase universalmente
independente do desfecho real. Uma nota alta é um sinal necessário mas nunca suficiente —
sempre relatá-la junto com a leitura de viabilidade de sublimite, e nunca enquadrar o filtro do
Art. 28 aprovado ou um TOTAL forte como "provavelmente será aprovado" sem essa qualificação.
