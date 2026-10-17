def gerenciar_filmes():
    filmes = []  #aqui está a lista que vai sendo preenchida conforme os filmes vão sendo add

    while True:

        print(" GERENCIADOR DE COLEÇÃO DE FILMES ")
        print("1. Adicionar novo filme")
        print("2. Ver lista de filmes")
        print("3. Ordenar filmes")


        opcao = input("\nEscolha uma opção (1-3): ").strip() #vai pedir para vc escolher uma opção para determinada ação

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
                print("\n📭 Nenhum filme cadastrado para ordenar.")
                continue

            print("Critérios de Ordenação ")
            print("1. Por Título (A-Z)")
            print("2. Por Ano (Mais antigo ao mais recente)")
            print("3. Por Nota (Maior para menor)")

            criterio = input("Escolha o critério (1-3): ").strip()

            if criterio == "1":
                filmes.sort(key=lambda x: x["titulo"].lower())
                print(" Filmes ordenados por Título com sucesso!")
            elif criterio == "2":
                filmes.sort(key=lambda x: x["ano"])
                print(" Filmes ordenados por Ano com sucesso!")
            elif criterio == "3":
                filmes.sort(key=lambda x: x["nota"], reverse=True)
                print(" Filmes ordenados por Nota com sucesso!")
            else:
                print(" Opção de ordenação inválida.")



if __name__ == "__main__":
    gerenciar_filmes()