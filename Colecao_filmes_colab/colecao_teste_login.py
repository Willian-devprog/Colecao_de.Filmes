import csv
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ARQUIVO = Path("filmes.json")
BANCO = Path("banco.db")

conexao = sqlite3.connect(BANCO)
cursor = conexao.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
""")
conexao.commit()


def cadastrar_conta():
    nome = input("Nome: ").strip()
    senha = input("Senha: ").strip()
    if not nome or not senha:
        print("Nome e senha não podem ficar vazios.")
        return
    try:
        cursor.execute("INSERT INTO contas (nome, senha) VALUES (?, ?)", (nome, senha))
        conexao.commit()
        print("Conta criada!")
    except sqlite3.IntegrityError:
        print("Esse nome já existe.")


def login_conta():
    nome = input("Nome: ").strip()
    senha = input("Senha: ").strip()
    cursor.execute("SELECT nome FROM contas WHERE nome = ? AND senha = ?", (nome, senha))
    conta = cursor.fetchone()
    if conta:
        print(f"Bem-vindo, {conta[0]}!")
        return conta[0]
    print("Dados incorretos.")
    return None


def listar_contas():
    cursor.execute("SELECT id, nome FROM contas")
    contas = cursor.fetchall()
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for id_conta, nome in contas:
        print(f"{id_conta} - {nome}")


def deletar_conta(usuario_atual):
    nome = input("Nome da conta para deletar: ").strip()
    cursor.execute("DELETE FROM contas WHERE nome = ?", (nome,))
    conexao.commit()
    if cursor.rowcount:
        print("Deletado.")
        if usuario_atual == nome:
            return None
    else:
        print("Conta não encontrada.")
    return usuario_atual


def carregar(): #Lê os filmes salvos. Se não houver arquivo (ou ele estiver quebrado), começa vazio.
    if not ARQUIVO.exists():
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Arquivo corrompido. Iniciando com lista vazia.")
        return []


def salvar(filmes): #Grava a lista inteira no arquivo JSON.
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(filmes, f, ensure_ascii=False, indent=2)




def validar_ano(texto): #Converte o ano para inteiro e confere se é um valor razoável.
    try:
        ano = int(texto)
    except ValueError:
        raise ValueError("O ano deve ser um número inteiro.")

    ano_maximo = datetime.now().year + 5  # permite filmes ainda não lançados
    if not 1888 <= ano <= ano_maximo:  # 1888 = primeiro filme da história
        raise ValueError(f"O ano deve estar entre 1888 e {ano_maximo}.")
    return ano


def validar_nota(texto): #Converte a nota para decimal entre 0.0 e 10.0. Aceita '7,5' e '7.5'.
    try:
        nota = float(texto.replace(",", "."))
    except ValueError:
        raise ValueError("A nota deve ser um número (ex: 8 ou 7.5).")

    if not 0.0 <= nota <= 10.0:
        raise ValueError("A nota deve estar entre 0.0 e 10.0.")
    return round(nota, 1)


def criar_filme(titulo, categoria, ano, nota, comentario=""): #Valida todos os campos e devolve o dicionário do filme.
    titulo = titulo.strip()
    categoria = categoria.strip()
    ano = str(ano).strip()
    nota = str(nota).strip()

    if not titulo or not categoria or not ano or not nota:
        raise ValueError("Título, categoria, ano e nota são obrigatórios.")

    return {
        "titulo": titulo,
        "categoria": categoria,
        "ano": validar_ano(ano),
        "nota": validar_nota(nota),
        "comentario": comentario.strip(),
    }


def filme_existe(filmes, titulo): #Verifica se já existe um filme com esse título (ignora maiúsculas/minúsculas).
    return any(f["titulo"].lower() == titulo.strip().lower() for f in filmes)


def exibir(lista): #Mostra uma lista de filmes na tela (usada na listagem e na busca).
    for i, f in enumerate(lista, 1):
        # .get() evita erro com filmes antigos que não tinham comentário
        comentario = f.get("comentario", "")
        print(f"{i}. [{f['categoria']}] {f['titulo']} ({f['ano']}) - Nota: {f['nota']:.1f}")
        if comentario:
            print(f"   Comentário: {comentario}")




def adicionar(filmes): #Opção 1: cadastra um filme, com nota e comentário.
    print("\n--- Adicionar novo filme ---")
    titulo = input("Título do filme: ").strip()

    if titulo and filme_existe(filmes, titulo):
        print(f"Atenção: o filme '{titulo}' já consta na sua coleção!")
        return

    categoria = input("Categoria (ex: Ação, Comédia, Terror): ")
    ano = input("Ano de lançamento: ")
    nota = input("Nota (0.0 a 10.0): ")
    comentario = input("Comentário (opcional): ")

    try:
        filme = criar_filme(titulo, categoria, ano, nota, comentario)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return

    filmes.append(filme)
    salvar(filmes)
    print(f"Filme '{filme['titulo']}' adicionado com sucesso!")


def listar(filmes): #Opção 2: mostra todos os filmes.
    if not filmes:
        print("\nSua coleção de filmes está vazia.")
        return

    print(f"\n--- Sua Coleção ({len(filmes)} filmes) ---")
    exibir(filmes)


def ordenar(filmes): #Opção 3: ordena a coleção por título, ano ou nota.
    if not filmes:
        print("\nNenhum filme cadastrado para ordenar.")
        return

    print("\n--- Critérios de Ordenação ---")
    print("1. Por Título (A-Z)")
    print("2. Por Ano (mais antigo ao mais recente)")
    print("3. Por Nota (maior para menor)")
    criterio = input("Escolha o critério (1-3): ").strip()

    if criterio == "1":
        filmes.sort(key=lambda f: f["titulo"].lower())
    elif criterio == "2":
        filmes.sort(key=lambda f: f["ano"])
    elif criterio == "3":
        filmes.sort(key=lambda f: f["nota"], reverse=True)
    else:
        print("Opção de ordenação inválida.")
        return

    salvar(filmes)
    print("Filmes ordenados com sucesso!")


def buscar(filmes): #Opção 4: procura a palavra no título ou na categoria.
    if not filmes:
        print("\nNenhum filme cadastrado para buscar.")
        return

    palavra = input("\nDigite a palavra-chave: ").strip().lower()
    if not palavra:
        print("Digite pelo menos uma letra para buscar.")
        return

    encontrados = [
        f for f in filmes
        if palavra in f["titulo"].lower() or palavra in f["categoria"].lower()
    ]

    if not encontrados:
        print(f"Nenhum filme encontrado para '{palavra}'.")
        return

    print(f"\n--- {len(encontrados)} resultado(s) para '{palavra}' ---")
    exibir(encontrados)


def importar_csv(filmes):
    print("\n--- Importar CSV ---")
    print("Colunas esperadas: titulo, categoria, ano, nota, comentario (opcional)")
    caminho = Path(input("Caminho do arquivo .csv: ").strip().strip('"'))

    if not caminho.is_file():
        print("Erro: arquivo não encontrado.")
        return

    importados = 0
    duplicados = 0
    erros = []  # guarda mensagens como "Linha 4: A nota deve ser..."

    with open(caminho, "r", encoding="utf-8-sig", newline="") as f:
        # descobre o separador olhando só o cabeçalho: ";" (Excel BR) ou ","
        cabecalho = f.readline()
        separador = ";" if cabecalho.count(";") > cabecalho.count(",") else ","
        f.seek(0)  # volta ao início para o leitor processar o arquivo inteiro

        leitor = csv.DictReader(f, delimiter=separador)

        # normaliza os nomes das colunas (minúsculas, sem espaços)
        if leitor.fieldnames:
            leitor.fieldnames = [c.strip().lower() for c in leitor.fieldnames]

        obrigatorias = {"titulo", "categoria", "ano", "nota"}
        if not leitor.fieldnames or not obrigatorias.issubset(leitor.fieldnames):
            print("Erro: o cabeçalho deve conter as colunas: titulo, categoria, ano, nota.")
            return

        # a linha 1 é o cabeçalho, então os dados começam na linha 2
        for numero_linha, linha in enumerate(leitor, start=2):
            titulo = (linha.get("titulo") or "").strip()

            if titulo and filme_existe(filmes, titulo):
                duplicados += 1
                continue

            try:
                filme = criar_filme(
                    titulo,
                    linha.get("categoria") or "",
                    linha.get("ano") or "",
                    linha.get("nota") or "",
                    linha.get("comentario") or "",
                )
            except ValueError as erro:
                erros.append(f"Linha {numero_linha}: {erro}")
                continue

            filmes.append(filme)
            importados += 1

    if importados:
        salvar(filmes)  # salva uma vez só, no final

    print("\n--- Resultado da importação ---")
    print(f"Importados: {importados}")
    print(f"Ignorados por já existirem: {duplicados}")
    print(f"Com erro: {len(erros)}")
    for mensagem in erros:
        print(f"  - {mensagem}")


#AQUI EMBAIXO ESTÁ O MENU PRINCIPAL

def gerenciar_filmes(usuario):
    filmes = carregar()

    while True:
        print("\n GERENCIADOR DE COLEÇÃO DE FILMES ")
        print("1. Adicionar novo filme")
        print("2. Ver lista de filmes")
        print("3. Ordenar filmes")
        print("4. Buscar por palavra-chave")
        print("5. Importar de CSV")
        print("6. Trocar de conta / Sair do gerenciador")

        opcao = input("\nEscolha uma opção (1-6): ").strip()

        if opcao == "1":
            adicionar(filmes)
        elif opcao == "2":
            listar(filmes)
        elif se_opcao := (opcao == "3"):
            ordenar(filmes)
        elif opcao == "4":
            buscar(filmes)
        elif opcao == "5":
            importar_csv(filmes)
        elif opcao == "6":
            print("Saindo da coleção...")
            break
        else:
            print("Opção inválida. Escolha de 1 a 6.")

      
def menu_acesso():
    usuario = None
    while True:
        print(f"\n[Logado: {usuario or 'ninguém'}]")
        print("1-Cadastrar | 2-Login | 3-Listar contas | 4-Deletar conta | 5-Acessar filmes | 0-Sair")
        op = input("Opção: ").strip()

        if op == "1":
            cadastrar_conta()
        elif op == "2":
            usuario = login_conta()
        elif op == "3":
            listar_contas()
        elif op == "4":
            usuario = deletar_conta(usuario)
        elif op == "5":
            if usuario:
                gerenciar_filmes(usuario)
            else:
                print("Faça login primeiro para acessar os filmes.")
        elif op == "0":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        menu_acesso()
    finally:
        conexao.close()