# Official data sources for CAPAG, debt and IDH(M) cross-checks

<!-- added per user instruction: free/official APIs only, no paid services -->

PHASE 1.6 requires a consultation date and source for every CAPAG, IDH(M) and debt-capacity
value. Use these free, official sources to obtain or cross-check them — never a paid data
vendor. If a value cannot be confirmed against one of these, raise `input_flag` rather than
trusting the proponent's figure.

| Need | Source | Access |
|---|---|---|
| CAPAG rating (states, DF, municipalities) | STN — Secretaria do Tesouro Nacional, *Boletim de Capacidade de Pagamento* | Datasets via [Tesouro Transparente CKAN](https://www.tesourotransparente.gov.br/ckan/dataset) (search "capacidade de pagamento" / "CAPAG") |
| Subnational debt / fiscal indicators (DC/RCL, debt trend, RGF/RREO figures) | STN, same portal | [Tesouro Transparente CKAN](https://www.tesourotransparente.gov.br/ckan/dataset) |
| IDH/IDHM | Atlas do Desenvolvimento Humano (PNUD/IPEA/FJP), mirrored in | [IPEA's `ipeadatar`](https://cran.r-project.org/web/packages/ipeadatar/index.html) (R) or [`ipeadatapy`](https://pypi.org/project/ipeadatapy/) (Python); cross-check municipal codes via [IBGE API](https://servicodados.ibge.gov.br/api/docs/) |
| Municipality/UF identifiers, population, other IBGE series | IBGE | [Serviço de Dados IBGE](https://servicodados.ibge.gov.br/api/docs/) · [metadados estatísticos (gov.br/conecta)](https://www.gov.br/conecta/catalogo/apis/metadados-estatisticos-do-ibge) |
| Water/sanitation/hydric-security indicators (rural/environment sector cross-check) | SNIRH | [SNIRH geonetwork catalog](https://metadados.snirh.gov.br/geonetwork/srv/por/catalog.search#/home) |
| Bulk/cleaned versions of the above (faster joins, historical series) | Base dos Dados | [basedosdados.org](https://basedosdados.org/) |

Notes:
- These cover CAPAG, debt and IDH(M). They do not replace the proponent's own declared values
  for the operation itself (ticket, counterpart, indicators) — those still come from the carta-
  consulta text.
- Record the consultation date and the exact dataset/endpoint used, per PHASE 1.6's metadata
  requirement.
- `ipeadatar`/`ipeadatapy` mirror IPEA's series (including IDHM); when in doubt, check the value
  against the IBGE API's municipal code to catch UF/code mismatches (the same cross-check PHASE
  1.6 already requires).
