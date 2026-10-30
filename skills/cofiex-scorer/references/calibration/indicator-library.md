# Biblioteca de indicadores por setor, com o veredito da SEAID

Base: 255 indicadores com fórmula, unidade, linha de base e meta, lidos das tabelas de
indicadores das Notas Técnicas do regime anterior (reuniões 166ª–178ª), cruzados com a nota do
item 1.3 "coerência entre indicadores e resultados" (ou 1.2, quando o 1.3 não existia). Somados
às críticas escritas desse item em 96 Notas Técnicas. Padrões anonimizados: os nomes de lugares,
órgãos e programas foram trocados por descrições genéricas. Usar na tarefa R6 do plano de
correção, nos indicadores de objetivo de desenvolvimento do projeto da lente Banco Mundial e na
skill cofiex-pleito-builder. Não usar para pontuar a Área Estratégica por semelhança de texto.

## O que separa um quadro de indicadores aprovado de um criticado
| Atributo do indicador | Quadros FORTE (n=69) | Quadros ADEQUADO (n=80) | Quadros FRACO ou AUSENTE (n=106) |
|---|---|---|---|
| Indicador de resultado (razão, taxa, índice, tempo, redução) | 67% | 66% | 49% |
| Linha de base igual a zero | 25% | 38% | **60%** |
| Ano da linha de base e ano-meta escritos no indicador | **48%** | 26% | 12% |

Regras práticas que saem daí e das críticas escritas:
1. **Ano-meta e ano de linha de base no próprio indicador** ("Linha de base: 2023; Meta: ano 5").
   A falta de prazo é o subitem que mais derruba o item 1.3.
2. **Linha de base medida, não zero.** "Base zero para todos os indicadores" foi lida como "não
   reflete a realidade". Zero só se justifica para algo que de fato não existe hoje.
3. **Razão com numerador e denominador nomeados** e fonte do dado (Defesa Civil, SNIS, INEP,
   DATASUS, registro administrativo do órgão). Contagem simples de entregas é produto, não
   resultado.
4. **Um indicador por objetivo específico, mais um de impacto para o objetivo geral**,
   classificados em produto, resultado e impacto.
5. **Recorte territorial explícito:** dizer se o indicador mede a área de intervenção ou o
   território inteiro. Indicadores de cobertura de uma concessionária inteira foram criticados
   por não separar o efeito do projeto.
6. **Meta progressiva**, ano a ano, quando o prazo é longo. A falta foi anotada mesmo em quadros
   bons.

## Indicadores que tiveram veredito FORTE, por setor (modelos de fórmula)
**Desenvolvimento urbano, drenagem e meio ambiente urbano**
- Taxa de permeabilidade do solo na área do programa = áreas permeáveis / área do programa × 100.
- Índice de área verde pública = área de espaços verdes de uso público / habitantes do bairro (m²/hab).
- Taxa de requalificação do curso d'água = extensão requalificada / extensão total × 100.
- Edificações (ou pessoas) em risco muito alto de inundação = em risco após o projeto / total no
  trecho × 100.
- Pontos de alagamento na bacia = pontos após / pontos antes × 100 (fonte: Defesa Civil ou
  central de atendimento do município).
- Linhas de transporte coletivo afetadas por alagamento = linhas afetadas / linhas que cruzam a
  área × 100.
- Índice composto de bem-estar urbano (dimensões de mobilidade, ambiente, habitação, serviços e
  infraestrutura), com a metodologia em anexo.

**Mobilidade**
- Redução do tempo de viagem = (tempo médio atual − tempo médio futuro) / tempo médio atual.
- Velocidade média no eixo (km/h), antes e depois.
- Participação do transporte coletivo na matriz de viagens = viagens por coletivo / viagens totais.
- Peso do custo do transporte na renda, antes e depois.
- Acidentes com vítimas na área de intervenção, % de redução sobre o ano de base.
- Passeios acessíveis = extensão acessível / extensão existente × 100.

**Água e saneamento**
- Índice de perdas do setor de distribuição = vazão perdida / vazão distribuída × 100.
- Índice de atendimento de esgoto da sub-bacia = população ligada à rede / população da sub-bacia.
- Taxa de internação por doenças de veiculação hídrica por 10 mil habitantes.
- Pontos de monitoramento da qualidade da água em operação / meta de pontos.
- Redução do lodo enviado a aterro = volume gerado × (1 − % de redução).

**Segurança, justiça e sistema prisional**
- Taxa de homicídios por 100 mil habitantes nas cidades priorizadas (e entre jovens de 15–29 anos).
- Reincidência criminal dos participantes = participantes que voltaram a cometer crime /
  participantes.
- Diferença em pontos percentuais entre grupo de tratamento e grupo de controle (avaliação de
  impacto) para empregabilidade, uso precoce de álcool, apreensões.

**Transformação digital e gestão pública**
- Escolas com conexão acima de um patamar de velocidade / total de escolas.
- Serviços disponíveis em forma digital na plataforma do cidadão.
- Estabelecimentos de saúde com prontuário eletrônico interligado.
- Tempo médio para concessão de benefício previdenciário.
- Taxa de crescimento real da folha de pagamento de servidores ativos ao ano.

## Indicadores que tiveram veredito FRACO, e o motivo
| Setor | Indicador criticado (forma genérica) | Motivo na Nota Técnica | Troca sugerida |
|---|---|---|---|
| Social e rural | Famílias beneficiadas (soma, base zero), também por recorte de mulheres, jovens ou povos tradicionais | contagem de beneficiários é produto; base zero | % de famílias atendidas que aumentam a renda ou saem da pobreza, medido por estudo de avaliação com linha de base |
| Educação profissional | Número de matrículas; número de professores formados | contagem sem relação com o resultado | taxa de conclusão; taxa de abandono e reprovação no ensino médio (fonte INEP); jovens que não estudam nem trabalham (PNAD) |
| Saneamento | Novas ligações de água ou esgoto (somatório) | não separa área do projeto da área da concessionária | índice de atendimento na área de intervenção, com recorte declarado |
| Energia e polos industriais | Capacidade instalada, empregos, emissões evitadas, só com meta final de longo prazo | sem prazo intermediário; resultados do projeto misturados com os do polo inteiro | metas no prazo do projeto e resultado atribuível ao que é financiado |
| Inovação e conectividade | "Elaboração de agenda", "relatórios técnicos desenvolvidos", "projetos de amplo alcance" | execução, sem fórmula, difícil de mensurar | proporção de domicílios com acesso, preço ou qualidade medida na área-alvo |
| Qualquer setor | Indicador cuja linha de base será medida por equipamento ainda não instalado | linha de base inexistente na data da carta | usar proxy disponível hoje e informar a data da primeira medição |
| Qualquer setor | Um único indicador cobrindo só uma das entregas | "não existe indicador para o resultado esperado X" | um indicador por objetivo específico |

## Ligação com a Área Estratégica da RN 1/2024
Os mesmos atributos movem o nível da área no regime atual (ver `ae-criteria-by-level-and-ppa-area.md`):
indicador de resultado setorial com ano-meta sustenta D ou mais; indicador de execução ou
contagem segura a área em D/E; indicador sem temporalidade é lido como "não atende à metodologia
SMART". A biblioteca serve para propor a troca; o nível continua sendo estimado pela lente A.6.
