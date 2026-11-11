# Citizen Assist AI - módulo de decisão lógica

Protótipo didático de triagem de duas rotas da Tarifa Social de Energia Elétrica. Não é canal oficial e não confirma concessão de benefício.

## Arquivos
- `GS_Citizen_Assist_AI_1CC_FEV.pdf`: documentação completa, simplificações, mapas, circuitos e fontes.
- `elegibilidade.py`: implementação interativa com validação 0/1.
- `testa_equivalencia.py`: compara as funções em todas as 16 entradas.
- `tabela_verdade.csv`: tabela completa.
- `imagens/circuito_original.png` e `imagens/circuito_simplificado.png`: referência para montar os circuitos no simulador.

## Executar
Com Python 3 instalado, nesta pasta:
```sh
python elegibilidade.py
```
Para validar todas as combinações:
```sh
python testa_equivalencia.py
```
O programa aceita apenas 0 ou 1, repete entradas inválidas e apresenta uma orientação textual. Não informe nome, CPF, endereço ou número de instalação.

## Referência dos circuitos
Monte A, B, C e D como entradas independentes e S1, S2 e S3 como saídas. Use as imagens na pasta `imagens/` como referência. Para todas as 16 combinações e saídas esperadas, veja o CSV e o relatório.
