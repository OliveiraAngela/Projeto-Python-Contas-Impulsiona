import csv
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

FILE_PATH = "contas.csv"

def criar_conta_dict(tipo, descricao, valor, data_vencimento, data_recebimento, categoria, status, prioridade, comentarios):
    return {
        "tipo": tipo,
        "descricao": descricao,
        "valor": valor,
        "data_vencimento": data_vencimento,
        "data_recebimento": data_recebimento,
        "categoria": categoria,
        "status": status,
        "prioridade": prioridade,
        "comentarios": comentarios,
    }

def salvar_conta(conta):
    with open(FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=conta.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(conta)

def listar_contas():
    contas = []
    try:
        with open(FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                contas.append(row)
    except FileNotFoundError:
        pass
    return contas

def atualizar_conta(descricao, novos_dados):
    contas = listar_contas()
    conta_atualizada = False

    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=contas[0].keys() if contas else novos_dados.keys())
        writer.writeheader()
        for conta in contas:
            if conta["descricao"] == descricao:
                conta.update(novos_dados)
                conta_atualizada = True
            writer.writerow(conta)

    return conta_atualizada

def deletar_conta(descricao):
    contas = listar_contas()
    contas_filtradas = [conta for conta in contas if conta["descricao"] != descricao]

    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=contas[0].keys() if contas else [])
        if contas:
            writer.writeheader()
            writer.writerows(contas_filtradas)

    return len(contas) != len(contas_filtradas)

def gerar_relatorio_mensal():
    contas = listar_contas()
    relatorio = defaultdict(lambda: defaultdict(float))

    for conta in contas:
        mes_ano = "/".join(conta["data_vencimento"].split("/")[-2:])
        relatorio[mes_ano]["total_" + conta["tipo"]] += float(conta["valor"])

    return dict(relatorio)

def gerar_relatorio_pdf(caminho_pdf="relatorio_contas.pdf"):
    relatorio = gerar_relatorio_mensal()
    if not relatorio:
        print("Nenhuma conta para gerar relatório.")
        return None

    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    largura, altura = A4
    margem = 50
    y = altura - margem

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margem, y, "Relatório Contas")
    y -= 30

    for mes, dados in relatorio.items():
        if y < margem:
            c.showPage()
            y = altura - margem

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margem, y, f"Mês: {mes}")
        y -= 20

        for tipo, valor in dados.items():
            c.setFont("Helvetica", 12)
            c.drawString(margem, y, f"{tipo.capitalize()}: R$ {valor:.2f}")
            y -= 15

    c.save()
    print(f"Relatório salvo em {caminho_pdf}")
    return caminho_pdf

def buscar_contas(criterios):
    contas = listar_contas()
    resultados = []

    for conta in contas:
        corresponde = all(
            conta.get(campo, "").lower() == valor.lower()
            for campo, valor in criterios.items()
            if valor
        )
        if corresponde:
            resultados.append(conta)

    return resultados

def resumo_por_categoria():
    contas = listar_contas()
    resumo = defaultdict(lambda: {"total_debito": 0.0, "total_credito": 0.0})

    for conta in contas:
        categoria = conta["categoria"]
        valor = float(conta["valor"])
        if conta["tipo"] == "débito":
            resumo[categoria]["total_debito"] += valor
        elif conta["tipo"] == "crédito":
            resumo[categoria]["total_credito"] += valor

    return dict(resumo)


def menu():
    while True:
        print("\n=== Gerenciador de Contas ===")
        print("1. Criar Conta")
        print("2. Listar Contas")
        print("3. Atualizar Conta")
        print("4. Deletar Conta")
        print("5. Gerar Relatório em PDF")
        print("6. Buscar Contas ")
        print("7. Resumo por Categoria")
        print("8. Sair")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            tipo = input("Tipo (débito/crédito): ").strip()
            descricao = input("Descrição: ").strip()
            valor = float(input("Valor: ").strip())
            data_vencimento = input("Data de Vencimento (DD/MM/AAAA): ").strip()
            data_recebimento = input("Data de Recebimento (opcional): ").strip()
            categoria = input("Categoria (moradia, alimentação, lazer, outros): ").strip()
            status = input("Status (pago/pendente): ").strip()
            prioridade = input("Prioridade: ").strip()
            comentarios = input("Comentários (opcional): ").strip()
            conta = criar_conta_dict(tipo, descricao, valor, data_vencimento, data_recebimento, categoria, status, prioridade, comentarios)
            salvar_conta(conta)
            print("Conta criada com sucesso!")

        elif escolha == "2":
            contas = listar_contas()
            if not contas:
                print("Nenhuma conta cadastrada.")
            else:
                for conta in contas:
                    print(conta)

        elif escolha == "3":
            contas = listar_contas()
            if not contas:
                print("Nenhuma conta cadastrada.")
            else:
                print("\n=== Contas atuais ===")
                for conta in contas:
                    print(conta)
            descricao = input("Descrição da conta a atualizar: ").strip()
            novos_dados = {}
            novos_dados["tipo"] = input("Novo Tipo: ").strip()
            novos_dados["descricao"] = input("Nova Descrição: ").strip()
            novos_dados["valor"] = input("Novo Valor: ").strip()
            atualizar_conta(descricao, {k: v for k, v in novos_dados.items() if v})
            print("Conta atualizada!")

        elif escolha == "4":
            contas = listar_contas()
            if not contas:
                print("Nenhuma conta cadastrada.")
            else:
                print("\n=== Contas atuais ===")
                for conta in contas:
                    print(conta)
            descricao = input("Descrição da conta a deletar: ").strip()
            if deletar_conta(descricao):
                print("Conta deletada!")
            else:
                print("Conta não encontrada.")

        elif escolha == "5":
            gerar_relatorio_pdf()

        elif escolha == "6":
            print("\n=== Busca de Contas ===")
            tipo = input("Tipo (débito/crédito ou deixe em branco): ").strip()
            categoria = input("Categoria (ou deixe em branco): ").strip()
            status = input("Status (pago/pendente ou deixe em branco): ").strip()
            resultados = buscar_contas({
                "tipo": tipo,
                "categoria": categoria,
                "status": status,
            })
            if resultados:
                for conta in resultados:
                    print(conta)
            else:
                print("Nenhuma conta encontrada.")

        elif escolha == "7":
            print("\n=== Resumo Financeiro por Categoria ===")
            resumo = resumo_por_categoria()
            if not resumo:
                print("Nenhuma conta registrada.")
            else:
                for categoria, valores in resumo.items():
                    print(f"Categoria: {categoria}")
                    print(f"  Total Débito: R$ {valores['total_debito']:.2f}")
                    print(f"  Total Crédito: R$ {valores['total_credito']:.2f}")

        elif escolha == "8":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()