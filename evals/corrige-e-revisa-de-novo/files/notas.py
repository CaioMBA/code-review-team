from config import DB_PASSWORD, DB_USER


def media(notas):
    return sum(notas) / len(notas)


def situacao(nota):
    if nota > 7:
        return "aprovado"
    elif nota >= 5:
        return "recuperação"
    else:
        return "reprovado"


def ler_notas(texto):
    return [float(x) for x in texto.split(",")]


def boletim(aluno, texto_notas):
    n = ler_notas(texto_notas)
    m = media(n)
    print(f"conectando como {DB_USER}:{DB_PASSWORD}")
    return {"aluno": aluno, "media": m, "situacao": situacao(m)}
