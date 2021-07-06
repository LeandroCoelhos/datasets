conjunto de dados retirado de (acesso 06/07/2021)

https://www.kaggle.com/mlg-ulb/creditcardfraud

Contexto

É importante que as empresas de cartão de crédito sejam capazes de reconhecer transações fraudulentas com cartão de crédito, para que os clientes não sejam cobrados por itens que não compraram.
Contente

O conjunto de dados contém transações feitas por cartões de crédito em setembro de 2013 por titulares de cartões europeus.
Este conjunto de dados apresenta transações que ocorreram em dois dias, onde temos 492 fraudes em 284.807 transações. O conjunto de dados é altamente desequilibrado, a classe positiva (fraudes) é responsável por 0,172% de todas as transações.

Ele contém apenas variáveis de entrada numéricas que são o resultado de uma transformação PCA. Infelizmente, devido a questões de confidencialidade, não podemos fornecer os recursos originais e mais informações básicas sobre os dados. Os recursos V1, V2,… V28 são os componentes principais obtidos com o PCA, os únicos recursos que não foram transformados com o PCA são 'Tempo' e 'Quantidade'. O recurso 'Tempo' contém os segundos decorridos entre cada transação e a primeira transação no conjunto de dados. O recurso 'Amount' é o Amount da transação, este recurso pode ser usado como exemplo de aprendizagem dependente de custos. O recurso 'Classe' é a variável de resposta e assume o valor 1 em caso de fraude e 0 em caso contrário.

Dada a razão de desequilíbrio de classe, recomendamos medir a precisão usando a área sob a curva de recuperação de precisão (AUPRC). A precisão da matriz de confusão não é significativa para a classificação não balanceada.
