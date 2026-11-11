"""Protótipo didático da orientação sobre Tarifa Social de Energia Elétrica.
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
    print("Não é canal oficial nem confirma concessão de benefício.\n")
    a = ler_bit("A - família inscrita no CadÚnico")
    b = ler_bit("B - renda familiar por pessoa até meio salário mínimo")
    c = ler_bit("C - algum integrante recebe BPC")
    d = ler_bit("D - condições da unidade/cadastro conferidas")
    saidas = avaliar_simplificada(a, b, c, d)
    print("\nSaídas S1, S2, S3:", *saidas)
    print(orientar(saidas))

if __name__ == "__main__":
    main()
