import json
from pathlib import Path

Arquivo = Path("filmes.json")

def carregar():
    if not Arquivo.exists():
        return []
    try:
        with open(Arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Iniciando com lista vazia.")
        return []

def salvar(filmes):
    with open(Arquivo, "w", encoding="utf-8") as f:
        json.dump(filmes, f, ensure_ascii=False, indent=2)

def gerenciar_filmes():
    filmes = carregar()  #lista que vai sendo preenchida conforme os filmes vão sendo add

    while True:

        print(" GERENCIADOR DE COLEÇÃO DE FILMES ")
        print("1. Adicionar novo filme")
        print("2. Ver lista de filmes")
        print("3. Ordenar filmes")
        print("4. Sair")

        opcao = input("\nEscolha uma opção (1-4): ").strip() #vai pedir para vc escolher uma opção para determinada ação

        if opcao == "1":
            print("Adicione seu Próximo Novo Filme")
            titulo = input("Título do filme: ").strip()


            filme_existe = any(f["titulo"].lower() == titulo.lower() for f in filmes) #Isso aqui serve para saber se o titulo do filme já está na lista
            if filme_existe:
                print(f" Atenção: O filme '{titulo}' já consta na sua coleção!")
                continue

            categoria = input("Categoria (ex: Ação, Comédia, Terror): ").strip()
            ano = input("Ano de lançamento: ").strip()
            nota = input("Estrelas (0 a 10): ").strip()

            if not titulo or not categoria or not ano or not nota: #Verifica se todas as perguntas foram respondidas para o filme entitulado
                print("Erro: Todos os campos precisam ser preenchidos! Tente novamente.")
                continue

            try:
                filme = {
                    "titulo": titulo,
                    "categoria": categoria,
                    "ano": int(ano),
                    "nota": int(nota)
                }
                filmes.append(filme)
                salvar(filmes)
                print(f"Seu Filminho '{titulo}' foi adicionado com sucesso!")
            except ValueError:
                print(" Erro: O ano deve ser um número inteiro e a nota um número válido!")


        elif opcao == "2":
            if not filmes: #Se não tiver filmes na lista vai mostrar esse texto
                print("\n Sua coleção de filmes está vazia.")
                continue

            print(f"\n--- Sua Coleção ({len(filmes)} filmes) ---") #Se tiver algum filme listado vai mostrar suas informações
            for i, f in enumerate(filmes, 1):
                print(f"{i}. [{f['categoria']}] {f['titulo']} ({f['ano']}) - Nota:  {f['nota']}")


        elif opcao == "3":
            if not filmes: #Se não tiver filmes na lista para ordenar, mostrar esse texto
                print("\n Nenhum filme cadastrado para ordenar.")
                continue

            print("Critérios de Ordenação ")
            print("1. Por Título (A-Z)")
            print("2. Por Ano (Mais antigo ao mais recente)")
            print("3. Por Nota (Maior para menor)")

            criterio = input("Escolha o critério (1-3): ").strip()

            if criterio == "1":
                filmes.sort(key=lambda x: x["titulo"].lower())
                salvar(filmes)
                print(" Filmes ordenados por Título com sucesso!")
            elif criterio == "2":
                filmes.sort(key=lambda x: x["ano"])
                salvar(filmes)
                print(" Filmes ordenados por Ano com sucesso!")
            elif criterio == "3":
                filmes.sort(key=lambda x: x["nota"], reverse=True)
                salvar(filmes)
                print(" Filmes ordenados por Nota com sucesso!")
            else:
                print(" Opção de ordenação inválida.")
        
        elif opcao == "4":
            print("Até a próxima!")
            break

        else:
            print(" Opção inválida. Escolha de 1 a 4.")



if __name__ == "__main__":
    gerenciar_filmes()