
# Lista de algoritmos aceitos pela aplicação

# Algoritmos que geram descritores binários
BINARY_FEATURE_DETECTOR_ALG_LIST = ['ORB', 'BRISK', 'AKAZE']
# Algoritmos que geram descritores numéricos
NUMERICAL_FEATURE_DETECTOR_ALG_LIST = ['SIFT', 'SURF', 'KAZE']
# Métodos para comparação entree histogramas
HIST_COMP_METHODS = {
        'BHATTACHARYYA'     : 1, 
        'ALT-CHI-SQUARE'    : 2,
        'KULLBACK-LEIBLER'  : 3,
        'CHI-SQUARE'        : 4,
        'EUCLIDEAN'         : 5
    }

# Configuração a ser utilizada para a construção da VT e busca
GLOBAL_SETTINGS = {
    # Caminho para o dataset
    "dataset"                   : "images",
    # Algoritmo de extração de descritores
    "feature-detector-alg"      : "KAZE",
    # Grau da árvore(Quantos filhos cada nodo terá)
    "branch-factor"             : 14,
    # Quantidade de níveis que a árvore terá
    "levels"                    : 4, 
    # Níveis acima das folhas a serem considerados no cálculo do Score
    "levels-to-use"             : 2,
    # Cor da fonte de destaque na execução
    "font-color"                : "green"
}

DATABASE_SETTINGS = {
    # Nome do MySQL database que os dados serão armazenados
    "database"                  : "openvt",
    # Nome da tabela que os dados serão armazenados
    "table"                     : GLOBAL_SETTINGS["dataset"].split("/")[-1] + "_" + GLOBAL_SETTINGS["feature-detector-alg"],
    # Usuário para se conectar ao MySQL
    "user"                      : "giullianopaz",
    # Senha para se conectar ao MySQL
    "password"                  : "toor",
    # Host para se conectar ao MySQL
    "host"                      : "localhost"
}

SEARCH_SETTINGS = {
    # Quantidade de resultados mostrados ao final da busca
    "top-n-results"             : 12,
    # Metodo de comparação entre histogramas
    "hist-comp-method"          : HIST_COMP_METHODS["CHI-SQUARE"],
}
