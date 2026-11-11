from pathlib import Path
import csv
import itertools
import textwrap

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak, KeepTogether,
                                Preformatted)

ROOT = Path(__file__).resolve().parent
IMG = ROOT / 'imagens'
TESTS = ROOT / 'testes'
DOCS = ROOT / 'docs'
for p in (IMG, TESTS, DOCS):
    p.mkdir(parents=True, exist_ok=True)

def original(a, b, c, d):
    s1 = bool(d and ((a and b) or c))
    s2 = not bool(d)
    s3 = bool(d and not ((a and b) or c))
    return int(s1), int(s2), int(s3)

def simplified(a, b, c, d):
    s1 = int(bool((c and d) or (a and b and d)))
    s2 = int(not bool(d))
    s3 = int(bool((not a and not c and d) or (not b and not c and d)))
    return s1, s2, s3

def rows():
    return [(a,b,c,d,*original(a,b,c,d),*simplified(a,b,c,d))
            for a,b,c,d in itertools.product((0,1), repeat=4)]

# Runnable prototype
(ROOT / 'elegibilidade.py').write_text('''"""Protótipo didático da orientação sobre Tarifa Social de Energia Elétrica.
Não determina elegibilidade oficial. Entradas booleanas: 0=não, 1=sim.
"""

def avaliar_original(a: int, b: int, c: int, d: int) -> tuple[int, int, int]:
    validar(a, b, c, d)
    s1 = int(bool(d and ((a and b) or c)))
    s2 = int(not bool(d))
    s3 = int(bool(d and not ((a and b) or c)))
    return s1, s2, s3

def avaliar_simplificada(a: int, b: int, c: int, d: int) -> tuple[int, int, int]:
    validar(a, b, c, d)
    s1 = int(bool((c and d) or (a and b and d)))
    s2 = int(not bool(d))
    s3 = int(bool((not a and not c and d) or (not b and not c and d)))
    return s1, s2, s3

def validar(*valores: int) -> None:
    if len(valores) != 4 or any(type(v) is not int or v not in (0, 1) for v in valores):
        raise ValueError("Informe exatamente quatro valores booleanos: 0 ou 1.")

def orientar(saidas: tuple[int, int, int]) -> str:
    s1, s2, s3 = saidas
    if saidas == (1, 0, 0):
        return ("O cenário informado coincide com uma das rotas modeladas. "
                "Consulte a distribuidora e confirme os requisitos oficiais.")
    if saidas == (0, 1, 0):
        return ("As condições da unidade familiar ainda não foram verificadas. "
                "Procure a distribuidora ou o CRAS para conferência.")
    if saidas == (0, 0, 1):
        return ("Esta combinação não corresponde às duas rotas incluídas no protótipo. "
                "Isso não é uma negativa: há outras regras e situações não modeladas.")
    raise ValueError("Estado lógico inconsistente: saídas não são exclusivas.")

def ler_bit(nome: str) -> int:
    while True:
        valor = input(f"{nome} (0=não, 1=sim): ").strip()
        if valor in ("0", "1"):
            return int(valor)
        print("Entrada inválida. Digite somente 0 ou 1.")

def main() -> None:
    print("Triagem didática da Tarifa Social de Energia Elétrica")
    print("Não é canal oficial nem confirma concessão de benefício.\\n")
    a = ler_bit("A - família inscrita no CadÚnico")
    b = ler_bit("B - renda familiar por pessoa até meio salário mínimo")
    c = ler_bit("C - algum integrante recebe BPC")
    d = ler_bit("D - condições da unidade/cadastro conferidas")
    saidas = avaliar_simplificada(a, b, c, d)
    print("\\nSaídas S1, S2, S3:", *saidas)
    print(orientar(saidas))

if __name__ == "__main__":
    main()
''', encoding='utf-8')

# Complete truth table CSV and test transcript
allrows = rows()
with (ROOT / 'tabela_verdade.csv').open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['A','B','C','D','S1_original','S2_original','S3_original','S1_simplificada','S2_simplificada','S3_simplificada'])
    w.writerows(allrows)
(ROOT / 'testa_equivalencia.py').write_text('''import itertools
from elegibilidade import avaliar_original, avaliar_simplificada, orientar

def main():
    print("A B C D | S1 S2 S3 | validação")
    for entradas in itertools.product((0, 1), repeat=4):
        original = avaliar_original(*entradas)
        simplificada = avaliar_simplificada(*entradas)
        assert original == simplificada, (entradas, original, simplificada)
        assert sum(simplificada) == 1, (entradas, simplificada)
        print(*entradas, "|", *simplificada, "| equivalente")
    print("OK: 16/16 combinações equivalentes; saídas exclusivas e completas.")

if __name__ == "__main__":
    main()
'''.replace('+',''), encoding='utf-8')
lines = ['A B C D | S1 S2 S3 | validação']
for r in allrows:
    a,b,c,d,s1,s2,s3,t1,t2,t3 = r
    assert (s1,s2,s3)==(t1,t2,t3) and s1+s2+s3==1
    lines.append(f'{a} {b} {c} {d} | {t1} {t2} {t3} | equivalente')
lines.append('OK: 16/16 combinações equivalentes; saídas exclusivas e completas.')
(TESTS / 'saida_testes.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')

(ROOT / 'README.md').write_text('''# Citizen Assist AI - módulo de decisão lógica

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
''', encoding='utf-8')

# Pillow based drawing keeps image generation independent of matplotlib.
FONT_PATH='C:/Windows/Fonts/arial.ttf'
FONT_BOLD_PATH='C:/Windows/Fonts/arialbd.ttf'
def font(size, bold=False):
    path=FONT_BOLD_PATH if bold else FONT_PATH
    try: return ImageFont.truetype(path,size)
    except OSError: return ImageFont.load_default()
def centered(draw, xy, text, fnt, fill):
    draw.text(xy, text, font=fnt, fill=fill, anchor='mm')

# Karnaugh maps
row_labels = ['00','01','11','10']
col_labels = ['00','01','11','10']
def idx(ab, cd): return int(ab[0]+ab[1]+cd[0]+cd[1], 2)
map_specs = [
    ('S1', {3,7,11,13,15}, [('CD',[(r,2) for r in range(4)]), ('ABD',[(2,1),(2,2)])],
     'S1 = CD + ABD'),
    ('S2', set(range(0,16,2)), [("D' (wrap)",[(r,c) for r in range(4) for c in (0,3)])],
     "S2 = D'"),
    ('S3', {1,5,9}, [("A'C'D",[(0,1),(1,1)]), ("B'C'D",[(0,1),(3,1)])],
     "S3 = A'C'D + B'C'D")]
for name, mins, groups, equation in map_specs:
    im=PILImage.new('RGB',(1100,790),'white'); dr=ImageDraw.Draw(im)
    centered(dr,(550,48),f'Mapa de Karnaugh - {name}',font(32,True),'#123454')
    x0,y0,cell=190,180,145
    centered(dr,(x0+2*cell,y0-88),'CD (ordem Gray)',font(20,True),'#17324d')
    centered(dr,(x0-98,y0+2*cell),'AB',font(20,True),'#17324d')
    for c,l in enumerate(col_labels): centered(dr,(x0+c*cell+cell//2,y0-40),l,font(19,True),'#314d67')
    for r,l in enumerate(row_labels): centered(dr,(x0-45,y0+r*cell+cell//2),l,font(19,True),'#314d67')
    for r,ab in enumerate(row_labels):
        for c,cd in enumerate(col_labels):
            m=idx(ab,cd); val=int(m in mins)
            x=x0+c*cell; y=y0+r*cell
            dr.rectangle((x,y,x+cell,y+cell),fill='#e8f1fb' if val else 'white',outline='#526578',width=2)
            centered(dr,(x+cell//2,y+cell//2-10),str(val),font(29,True),'#123454' if val else '#9aa6b2')
            if val: centered(dr,(x+cell//2,y+cell-30),f'm{m}',font(15),'#53677b')
    palette=['#ef6c00','#8e44ad','#16a085']
    for gi,(label,cells) in enumerate(groups):
        col=palette[gi%len(palette)]
        for r,c in cells:
            x=x0+c*cell; y=y0+r*cell
            dr.rounded_rectangle((x+7,y+7,x+cell-7,y+cell-7),radius=15,outline=col,width=6)
        dr.text((x0+4*cell+20,y0+20+gi*48),label,font=font(19,True),fill=col)
    centered(dr,(550,785),equation,font(23,True),'#142f4c')
    im.save(IMG/f'mapa_{name}.png')

# Circuit diagrams as clear simulator build guides
def draw_circuit(filename,title,simplified=False):
    im=PILImage.new('RGB',(1500,760),'white'); dr=ImageDraw.Draw(im)
    centered(dr,(750,55),title,font(31,True),'#123454')
    labels=(['S1 = CD + ABD  ->  D(AB + C)',"S2 = D'","S3 = A'C'D + B'C'D  ->  D NOT(AB + C)"] if simplified else
            ['S1 = D AND ( (A AND B) OR C )','S2 = NOT D','S3 = D AND NOT( (A AND B) OR C )'])
    for i,label in enumerate(labels):
        y=190+i*165
        dr.text((35,y-25),label,font=font(19,True),fill='#193752')
        if i==1:
            dr.text((620,y+46),'D',font=font(20,True),fill='#17324d')
            dr.line((650,y+60,790,y+60),fill='#314d67',width=4)
            dr.rounded_rectangle((790,y+25,940,y+95),radius=8,fill='#f1f5f9',outline='#24425f',width=3)
            centered(dr,(865,y+60),'NOT',font(21,True),'#17324d')
            dr.line((940,y+60,1120,y+60),fill='#314d67',width=4); dr.text((1130,y+42),"S2 = D'",font=font(20,True),fill='#17324d')
        else:
            dr.text((80,y+42),'A',font=font(18,True),fill='#17324d'); dr.text((80,y+90),'B',font=font(18,True),fill='#17324d')
            dr.line((105,y+55,260,y+55),fill='#314d67',width=4); dr.line((105,y+103,260,y+103),fill='#314d67',width=4)
            def box(x,yy,w,label):
                dr.rounded_rectangle((x,yy-38,x+w,yy+38),radius=9,fill='#f1f5f9',outline='#24425f',width=3)
                centered(dr,(x+w/2,yy),label,font(20,True),'#17324d')
            box(260,y+80,150,'AND'); dr.line((410,y+80,480,y+80),fill='#314d67',width=4)
            dr.text((455,y+102),'C',font=font(18,True),fill='#17324d'); dr.line((480,y+80,480,y+103),fill='#314d67',width=4)
            dr.line((480,y+103,520,y+103),fill='#314d67',width=4); dr.line((480,y+80,520,y+55),fill='#314d67',width=4)
            box(520,y+80,150,'OR')
            if i==0:
                dr.line((670,y+80,760,y+80),fill='#314d67',width=4); dr.text((740,y+102),'D',font=font(18,True),fill='#17324d')
                dr.line((760,y+80,800,y+80),fill='#314d67',width=4); dr.line((760,y+80,760,y+105),fill='#314d67',width=4); dr.line((760,y+105,800,y+105),fill='#314d67',width=4)
                box(800,y+80,150,'AND'); dr.line((950,y+80,1080,y+80),fill='#314d67',width=4); dr.text((1090,y+60),'S1',font=font(20,True),fill='#17324d')
            else:
                dr.line((670,y+80,740,y+80),fill='#314d67',width=4); box(740,y+80,150,'NOT')
                dr.line((890,y+80,960,y+80),fill='#314d67',width=4); dr.text((930,y+102),'D',font=font(18,True),fill='#17324d')
                dr.line((960,y+80,960,y+105),fill='#314d67',width=4); dr.line((960,y+105,1000,y+105),fill='#314d67',width=4)
                box(1000,y+80,150,'AND'); dr.line((1150,y+80,1270,y+80),fill='#314d67',width=4); dr.text((1280,y+60),'S3',font=font(20,True),fill='#17324d')
    footer='Critério: AND, OR e NOT de até 2 entradas; sem compartilhamento entre saídas. Total: 8 portas nos dois circuitos.'
    centered(dr,(750,720),footer,font(17),'#455b70')
    im.save(IMG/filename)
draw_circuit('circuito_original.png','Circuito original - regras em forma fatorada',False)
draw_circuit('circuito_simplificado.png','Circuito simplificado - funções fatoradas',True)

# Technical PDF
pdf = ROOT / 'GS_Citizen_Assist_AI_1CC_FEV.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=17*mm,leftMargin=17*mm,topMargin=16*mm,bottomMargin=16*mm,title='Citizen Assist AI - módulo de decisão lógica',author='Equipe Citizen Assist AI')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Cover',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=23,leading=28,textColor=colors.HexColor('#123454'),alignment=TA_CENTER,spaceAfter=12))
styles.add(ParagraphStyle(name='SubCover',parent=styles['Normal'],fontSize=12,leading=18,alignment=TA_CENTER,textColor=colors.HexColor('#45617a')))
styles.add(ParagraphStyle(name='H1x',parent=styles['Heading1'],fontSize=16,leading=20,textColor=colors.HexColor('#123454'),spaceBefore=9,spaceAfter=7))
styles.add(ParagraphStyle(name='H2x',parent=styles['Heading2'],fontSize=12,leading=15,textColor=colors.HexColor('#1c5d83'),spaceBefore=7,spaceAfter=4))
styles.add(ParagraphStyle(name='Bodyx',parent=styles['BodyText'],fontSize=9.2,leading=13,spaceAfter=6))
styles.add(ParagraphStyle(name='Smallx',parent=styles['BodyText'],fontSize=7.5,leading=10))
styles.add(ParagraphStyle(name='Eq',parent=styles['Code'],fontName='Courier-Bold',fontSize=10,leading=14,leftIndent=8,spaceBefore=2,spaceAfter=5,textColor=colors.HexColor('#17324d')))
story=[]
P=lambda t,st='Bodyx': story.append(Paragraph(t,styles[st]))
story += [Spacer(1,28*mm), Paragraph('CITIZEN ASSIST AI',styles['Cover']), Paragraph('Módulo de decisão lógica: orientação sobre Tarifa Social de Energia Elétrica',styles['SubCover']), Spacer(1,18*mm)]
P('Relatório técnico de Computer Science', 'H1x'); P('Lógica booleana, formas canônicas, simplificação algébrica, mapas de Karnaugh, circuitos e protótipo em Python.','SubCover')
story += [Spacer(1,18*mm)]; P('Data do relatório: 11 de novembro de 2026.','SubCover'); P('Participantes: Ryan Luther Roque - RM 572993; João Guilherme Figueiredo - RM 572697.','SubCover'); story.append(PageBreak())

P('1. Problema e escopo','H1x')
P('O módulo recebe quatro respostas booleanas para fazer uma triagem didática de duas rotas frequentes relacionadas à Tarifa Social de Energia Elétrica (TSEE): inscrição no CadÚnico com renda familiar mensal por pessoa de até meio salário mínimo, ou recebimento de BPC por integrante da família. A resposta encaminha a pessoa para conferência, indica que uma rota modelada coincide com o caso informado ou esclarece que o caso está fora das rotas representadas.')
P('<b>Limite importante:</b> a regra é deliberadamente parcial. A legislação e as orientações oficiais contemplam outras situações, como famílias com integrante que necessita de equipamento elétrico de uso continuado, além de regras específicas para famílias indígenas e quilombolas. O protótipo não decide elegibilidade nem substitui a distribuidora, o CRAS ou os órgãos públicos. A TSEE prevê gratuidade da parcela de energia até 80 kWh mensais nas regras atuais; outros componentes da fatura podem permanecer. O modelo não calcula fatura.')
P('2. Variáveis e saídas','H1x')
data=[['Símbolo','Significado de 1','Significado de 0'],
['A','Família inscrita no CadÚnico','Não inscrita'],
['B','Renda familiar mensal por pessoa ≤ 1/2 salário mínimo','Renda acima desse limite'],
['C','Algum integrante da família recebe BPC','Nenhum integrante recebe BPC'],
['D','Unidade residencial e condições cadastrais conferidas','Ainda não conferidas ou não confirmadas']]
tbl_data=[[Paragraph(str(cell),styles['Smallx']) for cell in row] for row in data]
t=Table(tbl_data,colWidths=[16*mm,80*mm,80*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#123454')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7.5),('LEADING',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#aab8c6')),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f5f9')]),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)])); story.append(t); story.append(Spacer(1,6))
P('Para D=1, considere unidade residencial e confirme vínculo familiar/cadastral e endereço na área da distribuidora. D agrupa uma verificação operacional para manter o exercício em quatro entradas; em uso real, cada condição seria verificada separadamente. A tabela lógica não coleta nome, CPF, endereço ou número de instalação.')
P('As três saídas são one-hot (exatamente uma vale 1 para toda entrada):','Bodyx')
P('S1 = rota modelada coincide com as respostas informadas; orientar a confirmar os requisitos oficiais.','Bodyx')
P('S2 = D=0; encaminhar para conferência das condições da unidade/cadastro.','Bodyx')
P('S3 = D=1 e nenhuma das duas rotas simplificadas foi satisfeita; informar que isso não constitui negativa oficial.','Bodyx')
P('3. Regra e expressões canônicas','H1x')
P("Seja R = AB + C. A regra inicial é S1 = DR; S2 = D'; S3 = DR'. A notação + representa OR, justaposição representa AND e apóstrofo representa NOT. Índices dos mintermos seguem a ordem A,B,C,D (A é o bit mais significativo).")
P('Forma canônica por soma de mintermos:','H2x')
P('S1 = SUM m(3,7,11,13,15) &nbsp; | &nbsp; S2 = SUM m(0,2,4,6,8,10,12,14)<br/>S3 = SUM m(1,5,9)','Eq')
P('Equivalentes em produto de maxtermos:<br/>S1 = PRODUCT M(0,1,2,4,5,6,8,9,10,12,14)<br/>S2 = PRODUCT M(1,3,5,7,9,11,13,15)<br/>S3 = PRODUCT M(0,2,3,4,6,7,8,10,11,12,13,14,15).','Smallx')
P('4. Tabela-verdade completa','H1x')
P('As colunas O correspondem à regra inicial e as colunas E à expressão minimizada. A validação confirma a igualdade linha a linha.','Bodyx')
truth=[['A','B','C','D','S1 O','S2 O','S3 O','S1 E','S2 E','S3 E']]
for r in allrows:
    a,b,c,d,s1,s2,s3,t1,t2,t3=r
    truth.append([str(x) for x in (a,b,c,d,s1,s2,s3,t1,t2,t3)])
tt=Table(truth,colWidths=[12*mm]*10,repeatRows=1)
tt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#123454')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7.5),('ALIGN',(0,0),(-1,-1),'CENTER'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#afbbc6')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f1f5f8')]),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)])); story.append(tt)
P('O CSV separado tabela_verdade.csv inclui as mesmas linhas para consulta e validação automática.','Smallx')

P('5. Simplificação algébrica e De Morgan','H1x')
P('S1: DR = D(AB+C) = DAB+DC, pela distributiva.','Eq')
P("S2: D' já é mínima.",'Eq')
P("S3: DR' = D(AB+C)' = D(AB)'C' = D(A'+B')C' = A'C'D + B'C'D.",'Eq')
P("Na linha de S3, De Morgan transforma (X+Y)' em X'Y' e (AB)' em A'+B'; em seguida usamos distributiva. As regras principais usadas são distributiva, identidade de De Morgan e complemento. Forma fatorada equivalente de S3: D(AB+C)'.",'Bodyx')
P('6. Mapas de Karnaugh','H1x')
P('Linhas AB e colunas CD estão na ordem Gray 00, 01, 11, 10. Agrupamentos maiores possíveis são usados; bordas opostas são adjacentes. As imagens indicam mintermos e grupos.')
for nm,desc in [('S1','Grupo de quatro na coluna CD=11 produz CD; par m13,m15 produz ABD. Resultado: CD+ABD.'),('S2',"As oito células com D=0 formam um grupo com contorno entre as colunas CD=00 e CD=10 (adjacência circular), produzindo D'."),('S3',"Par m1,m5 produz A'C'D; par m1,m9 usa adjacência entre linhas AB=00 e AB=10, produzindo B'C'D.")]:
    P(nm+': '+desc,'H2x'); story.append(Image(str(IMG/f'mapa_{nm}.png'),width=150*mm,height=100*mm))
P("A soma de produtos obtida nos mapas coincide com as expressões algébricas simplificadas. Para desenhar os circuitos, as formas S1=D(AB+C) e S3=D(AB+C)' são fatoradas novamente sem alterar a função; a contagem de portas é feita sobre essas implementações equivalentes.")

P('7. Circuitos e comparação de portas','H1x')
P('Critério comparativo: portas AND, OR e NOT de até duas entradas; as saídas são implementadas em ramos separados e não há compartilhamento de subexpressões entre saídas. O desenho usa blocos rotulados para facilitar a montagem manual no logic.ly/demo ou no Logic Circuit.')
story.append(Image(str(IMG/'circuito_original.png'),width=177*mm,height=76*mm))
story.append(Spacer(1,4)); story.append(Image(str(IMG/'circuito_simplificado.png'),width=177*mm,height=76*mm))
ct=[['Saída','Original','Portas','Minimizada/fatorada','Portas'],['S1','D(AB+C)','3','D(AB+C), equivalente a CD+ABD','3'],['S2',"D'",'1',"D'",'1'],['S3',"D(AB+C)'",'4',"D(A'+B')C', fatorada como D(AB+C)'",'4'],['Total','','8','','8']]
ctt=Table(ct,colWidths=[18*mm,45*mm,17*mm,73*mm,17*mm],repeatRows=1)
ctt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#123454')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#aab8c6')),('FONTSIZE',(0,0),(-1,-1),7.5),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#f0f5f9')]),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold')])); story.append(ctt)
P('A simplificação reduz literais na soma de produtos, mas a fatoração da regra original já é eficiente no critério escolhido; portanto, a contagem total de portas fica igual. A equivalência deve ser priorizada sobre a expectativa de reduzir portas. Outras bases (NAND/NOR), fan-in ou compartilhamento entre saídas podem alterar a contagem.','Bodyx')

P('8. Programa, entradas inválidas e execução','H1x')
P('O arquivo elegibilidade.py implementa a expressão minimizada. Recebe A, B, C e D como 0/1, rejeita qualquer outro valor e solicita novamente em caso de entrada inválida. Em seguida imprime S1,S2,S3 e uma orientação em linguagem simples. A mensagem não declara concessão ou indeferimento.','Bodyx')
P('Execução, na pasta do projeto:','H2x')
story.append(Preformatted('python elegibilidade.py\npython testa_equivalencia.py',styles['Eq']))
P('Para reproduzir no simulador, crie quatro chaves A,B,C,D e três indicadores S1,S2,S3. As imagens separadas do circuito são guias visuais; mantenha A como bit mais significativo na conferência da tabela. Teste as 16 combinações de tabela_verdade.csv.')
P('9. Validação e resultados','H1x')
P('A validação percorre os 16 vetores binários de entrada. Para cada vetor, o código compara as funções original e simplificada e exige que exatamente uma saída esteja ativa. Resultado registrado: 16 de 16 combinações equivalentes, saídas exclusivas e completas. O transcript completo está em testes/saida_testes.txt.')
P('10. Limitações, privacidade e responsabilidade','H1x')
P('Este protótipo é educacional e não é canal oficial. Não confirma concessão de serviço, benefício ou direito, nem substitui a análise da distribuidora ou dos órgãos públicos. O escopo omite rotas e requisitos; por isso S3 significa apenas “fora das rotas modeladas”. S2 solicita conferência quando D=0. O programa não grava respostas. Evite inserir dados pessoais: somente bits 0/1 são necessários.')
story.append(PageBreak())
P('11. Guia rápido para montar e validar no simulador','H1x')
P('1. Crie quatro entradas binárias A, B, C e D; use as imagens circuito_original.png e circuito_simplificado.png como guias. Os blocos AND, OR e NOT representam portas lógicas de até duas entradas.','Bodyx')
P('2. Crie saídas S1, S2 e S3 e monte cada ramo separadamente. No circuito simplificado, a implementação fatorada é S1=D(AB+C), S2=D\' e S3=D(AB+C)\'.','Bodyx')
P('3. Aplique as 16 linhas de tabela_verdade.csv. Compare as três saídas da simulação às colunas S1 E, S2 E e S3 E. A cada linha, exatamente uma saída deve estar em 1.','Bodyx')
P('4. Fora do simulador, execute python testa_equivalencia.py para obter a comparação automática das expressões. O protótipo interativo recebe somente 0/1 e solicita novamente se a entrada for inválida.','Bodyx')
P('12. Conclusão','H1x')
P('O protótipo organiza duas rotas da TSEE em quatro variáveis booleanas. As formas canônicas, a álgebra, os mapas de Karnaugh e o programa produzem saídas equivalentes para todas as 16 combinações. O resultado é educativo e deve ser confirmado nos canais oficiais.','Bodyx')

def footer(canvas, doc):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(colors.HexColor('#d3dce5')); canvas.line(17*mm,12*mm,w-17*mm,12*mm)
    canvas.setFont('Helvetica',7.5); canvas.setFillColor(colors.HexColor('#52677b'))
    canvas.drawString(17*mm,8*mm,'Citizen Assist AI | Computer Science | 11 nov. 2026')
    canvas.drawRightString(w-17*mm,8*mm,f'{doc.page}')
    canvas.restoreState()
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(f'Criado: {pdf}')
