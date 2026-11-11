# Citizen Assist AI — módulo de decisão lógica

Protótipo didático de orientação sobre a Tarifa Social de Energia Elétrica. Não é canal oficial e não confirma a concessão de benefício.

## Arquivos
- `GS_Citizen_Assist_AI_1CC_FEV.pdf`: relatório técnico do projeto.
- `elegibilidade.py`: implementação interativa com validação das entradas 0/1.
- `testa_equivalencia.py`: valida as 16 combinações da tabela-verdade.
- `tabela_verdade.csv`: tabela completa.
- `circuito_original.png` e `circuito_simplificado.png`: diagramas de referência.
- `mapa_S1.png`, `mapa_S2.png` e `mapa_S3.png`: mapas de Karnaugh.
- `saida_testes.txt`: saída registrada da validação.
- `build_artifacts.py`: script de geração dos artefatos locais.

## Executar
Com Python 3 instalado, nesta pasta:
```sh
python elegibilidade.py
```
Para validar todas as combinações:
```sh
python testa_equivalencia.py
```
O programa aceita apenas 0 ou 1, repete entradas inválidas e apresenta orientações textuais. Não informe nome, CPF, endereço ou número de instalação.

Os diagramas mostram as entradas A, B, C e D e as saídas S1, S2 e S3. Consulte a tabela CSV para as saídas esperadas nas 16 combinações.
