# 🎬 Coleção de Filmes e Séries — Sistema de Gerenciamento e Avaliação

Este projeto consiste em uma aplicação em **Python** desenvolvida para execução no **Google Colab/VS Code**, criada como projeto prático para a disciplina de **Programação I** da UFRPE. O sistema permite que usuários gerenciem suas coleções de filmes e séries, registrem avaliações com comentários e analisem seus hábitos de consumo de mídias sem a necessidade de um banco de dados externo, utilizando persistência em arquivos **CSV**.

## 👥 Integrantes do Grupo e Responsabilidades 
| Nome Completo | Responsabilidade no Projeto |
| :--- | :--- |
| **José Bezerra Cabral Neto** | Desenvolvimento das rotinas de autenticação (Login/Cadastro) e controle de permissões. |
| **Marcos A. Lira Gomes** | Implementação das funções de cadastro de mídias, importação CSV e filtro por palavra-chave. |
| **Willian Hassan Costa Santos** | Criação do sistema de avaliação (0-10 com comentários), ranking, recomendações e exportação de relatórios. |

## 🚀 Funcionalidades do Sistema 
- **Autenticação e Controle de Acesso:** 
  - **Consulta Aberta**: Qualquer pessoa pode buscar e visualizar mídias e avaliações sem precisar fazer login. 
  - **Área do Usuário**: Para cadastrar novas mídias ou registrar avaliações, é obrigatório efetuar login no sistema.
- **Cadastro de Mídias (Filmes e Séries):** 
  - Registro individual informando título, categoria/gênero, tipo (Filme ou Série) e ano de lançamento.
- **Importação de Coleção Pessoal (CSV):**
  - Permite importar de forma automatizada um arquivo `.csv` contendo uma lista prévia de filmes e séries.
- **Avaliações com Comentários:**
  - Atribuição de notas em um intervalo fechado de **0.0 a 10.0** (onde `0` representa *Não recomendaria* e `10` representa *Super recomendaria / Perfeito*).
  - Espaço dedicado para inclusão de comentários e opiniões pessoais sobre a mídia.
- **Busca por Palavra-Chave:**
  - Pesquisa rápida de mídias por título, gênero ou tipo.
- **Ranking Geral:**
  - Listagem das mídias mais bem avaliadas pelos usuários organizadas por nota.
- **Recomendações Personalizadas:**
  - Algoritmo simples de recomendação baseado nos gêneros mais consumidos e bem avaliados pelo usuário logado.
- **Exportação de Relatórios:**
  - Geração de relatórios sumarizados em arquivo de texto (`.txt`) com estatísticas da coleção e histórico de avaliações.

## 🛠️ Tecnologias e Bibliotecas Utilizadas
- **Linguagem:** Python 3
- **Ambiente de Desenvolvimento:** Visual Studio Code (VS Code)
- **Ambiente de Execução Alternativo:** Google Colab
- **Persistência de Dados:** Arquivos `.csv` e `.txt` (sem uso de banco de dados relacional/SQL)
- **Bibliotecas Nativas do Python:**
  - `csv`: Para leitura e escrita estruturada dos dados da coleção e usuários. 
  - `os` / `sys`: Para manipulação e verificação de arquivos e caminhos no ambiente Colab.
  
## 📋 Instruções de Execução Passo a Passo (Google Colab) 
1. **Acessar o Notebook:** 
   - Abra o arquivo `.ipynb` do projeto diretamente no Google Colab.
2. **Preparar os Arquivos de Dados:** 
   - Certifique-se de carregar os arquivos `.csv` necessários na aba **Arquivos** (ícone de pasta no menu esquerdo do Colab) ou execute a célula inicial do código para que o programa crie automaticamente a estrutura de dados inicial.
3. **Executar a Aplicação:** 
   - Execute a célula principal do projeto para iniciar o menu interativo via terminal/console do Colab. 
4. **Navegação:** 
   - Utilize as opções numéricas do menu para navegar entre as rotinas de consulta, login, cadastro, avaliação e exportação de relatórios. 

## 📋 Instruções de Execução Passo a Passo (VS Code)
1. **Clonar o Repositório:** 
``bash
    git clone https://github.com/Willian-devprog/Colecao_de.Filmes.git 
    cd Colecao_de.Filmes

## 📂 Estrutura dos Arquivos de Dados (CSV) 
O projeto armazena as informações em arquivos texto com separador `;` para garantir a persistência dos dados entre execuções:
   - `usuarios.csv`: Armazena os dados dos usuários cadastrados (`id;nome;login;senha`). 
   - `midias.csv`: Contém o acervo de filmes e séries (`id;titulo;tipo;genero;ano`).
   - `avaliacoes.csv`: Registra o histórico de avaliações (`id_midia;id_usuario;nota;comentario`)
  
