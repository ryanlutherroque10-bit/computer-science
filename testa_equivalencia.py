import itertools
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
