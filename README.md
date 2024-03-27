# Data-Pipeline-on-Telegram
understand the main features of Telegram.

know the differences between groups and channels on Telegram.

understand the importance of Telegram as a data source.

# **Pipeline de Dados do Telegram I**

## Storytelling

![image](https://github.com/Vi4Na/Data-Pipeline-on-Telegram/assets/136501829/6c96c1e0-307e-4193-8805-a924fcf78e35)


### Contexto.

O projeto consiste em construir um pipeline completo de dados.
Para isso vamos dividi-lo em duas etapas: A infraestrutura por trás da arquitetura de dados e a analítica onde podemos, de fato, analizar os dados armazenados.
Arquitetura:
Sistema transacional: O *Telegram representa a fonte transacional de dados do projeto.

O primeiro passo será criar um BOT no telegram e adiciona-lo em um grupo novo onde será capaz de armazenar todos os dados fornecidos.
As mensagens capturadas serão acessadas via API e antes de avançar para etapa analítica é possível manipular e estruturar os dados utilizando apenas o Python nativo.

***Arquitetura***:

### Telegram.

 **Sistema transacional*: O **Telegram** representa a fonte transacional de dados do projeto.
  - O primeiro passo será criar um **BOT** no **telegram** e adiciona-lo em um grupo novo onde será capaz de armazenar todos os dados fornecidos.

2.1. Crie uma conta no **Telegram** caso não possua uma e faça o login na versão web da ferramenta através desse [link](https://web.telegram.org).
2.2. Crie um *bot*.
2.3. Crie um grupo e adicione o *bot*.
2.4. Torne o *bot* administrador do grupo.
2.5. Desabilite a opção de adicionar o *bot* a novos grupos.
2.6. Envie diversos tipos de mensagens no grupo (text, imagem, arquivos, video, áudio, etc.) e as consuma utilizand a API de *bots* do **Telegram**.

*Código no arquivo pipeline-telegram.py*

  - As mensagens capturadas serão acessadas via **API** e antes de avançar para etapa analítica é possível manipular e estruturar os dados utilizando apenas o **Python** nativo.

*Código no arquivo pipeline-wranglling.py*

  - As mensagens serão restringidas apenas ao formato **TEXT**, ou seja, o **BOT** entenderá como **"[ ]"** quaisquer outro tipo de dados como imagens, vídeos, mensagens de voz, arquivos.

***Sistema analítico***:
A etapa de ingestão é onde se armazena os dados transacionais em ambientes analíticos. O dado ingerido permanece no formato original **JSON**.

 *Para isso será utilizado*:

  - O **AWS S3** para armazenamento dos dados fornecidos. Para tanto, basta a criação de um *bucket*. Como padrão, vamos adicionar o sufixo `-raw` ao seu nome.
  - O **AWS Lambda** será o responsável por persistir ativamente as mensagens capturadas.

*Código no arquivo pipeline-lambda.py*

O AWS API Gateway que irá receber as mensagens captadas pelo bot enviadas via webHook iniciando a função Lambda executada acima.
Por fim, é necessário configurar o webHook para redirecionar as mensagens do Telegram para a URL do AWS API Gateway.

*Código no arquivo pipeline-api.py*

***Análise Exploratória de Dados***:

### ETL.

A etapa de extração, transformação e carregamento (do inglês extraction, transformation and load ou ETL) é uma etapa abrangente responsável pela manipulação dos dados ingeridos de sistemas transacionais, ou seja, já persistidos em camadas cruas ou raw de sistemas analíticos.

Para isso, vamos utilizar uma função do AWS Lambda como motor de processamento e um bucket do AWS S3 como camada enriquecida para a persistência do dado processado. Para garantir a recorrência, vamos configurar uma regra do AWS Event Bridge como gatilho diáro da função.

Para isso será utilizado:

o AWS S3, na etapa de ETL, tem a função de passivamente armazenar as mensagens processadas de um dia em um único arquivo no formato Parquet. Para tanto, basta a criação de um bucket. Como padrão, vamos adicionar o sufixo -enriched ao seu nome.
O AWS Lambda, na etapa de ETL, tem a função de ativamente processar as mensagens captadas pelo bot do Telegram, persistidas na camada cru no bucket do AWS S3, e persisti-las na camada enriquecida, também em um bucket do AWS S3. Logo, vamos criar uma função que opera da seguinte forma:

*Código no arquivo pipeline-etl.py*

Para que a função funcione corretamente, algumas configurações precisam ser realizadas.

Variáveis de ambiente
Note que o código exige a configuração de duas variáveis de ambiente: AWS_S3_BUCKET e AWS_S3_ENRICHED com os nomes dos bucket do AWS S3 da camada cru e enriquecida, respectivamente. Para adicionar variáveis de ambiente em uma função do AWS Lambda, basta acessar configurações -> variáveis de ambiente no console da função.

Permissão
Precisamos adicionar a permissão de escrita nos buckets do AWS S3 para a função do AWS Lambda no AWS IAM.

Recursos
O timeout padrão de funcões do AWS Lambda é de 3 segundos. Para a função, vamos aumentar o tempo para 5 minutos, principalmente para lidar com o IO (input/output) de arquivos do AWS S3.

Camadas
Por fim, note que o código da função utiliza o pacote Python PyArrow. Contudo, o ambiente padrão do AWS Lambda possui poucos pacotes externos instalado, como o pacote Python boto3, logo o PyArrow não será encontrado e a execução da função falhará. Existem algumas formas de adicionar pacotes externos no ambiente de execução do AWS Lambda, um deles é a criação de camadas ou layers, onde podemos fazer o upload dos pacotes Python direto na plataforma ou através de um bucket do AWS S3. Vamos então seguir com a última opção, onde teremos que:

o AWS EventBridge, na etapa de ETL, tem a função de ativar diariamente a função de ETL do AWS Lambda, funcionando assim como um scheduler.
Apresentação
A etapa de apresentação é reponsável por entregar o dado para os usuários (analistas, cientistas, etc.) e sistemas (dashboards, motores de consultas, etc.), idealmente através de uma interface de fácil uso, como o SQL, logo, essa é a única etapa que a maioria dos usuários terá acesso. Além disso, é importante que as ferramentas da etapa entregem dados armazenados em camadas refinadas, pois assim as consultas são mais baratas e o dados mais consistentes.

AWS Athena

Na etapa de apresentação, o AWS Athena tem função de entregar o dados através de uma interface SQL para os usuários do sistema analítico. Para criar a interface, basta criar uma tabela externa sobre o dado armazenado na camada mais refinada da arquitetura, a camada enriquecida.

![image](https://github.com/Vi4Na/Data-Pipeline-on-Telegram/assets/136501829/6ae7ff5b-3333-4acc-9fdd-0eacb23127ff)


> **Importante**: Toda vez que uma nova partição é adicionada ao repositório de dados, é necessário informar o `AWS Athena` para que a ela esteja disponível via SQL. Para isso, use o comando SQL `MSCK REPAIR TABLE <nome-tabela>` para todas as partições. Toda vez que uma nova partição é adicionada ao repositório de dados, é necessário informar o `AWS Athena` para que a ela esteja disponível via SQL.

![image](https://github.com/Vi4Na/Data-Pipeline-on-Telegram/assets/136501829/1cb585f8-ac5e-40be-ad1c-e8c848dc4f02)

### Análise de Dados.
Com o dado disponível, usuário podem executar as mais variadas consultas analíticas. Seguem alguns exemplos:

**Quantidade de mensagens por dia.**

![image](https://github.com/Vi4Na/Data-Pipeline-on-Telegram/assets/136501829/0258a25b-fb52-4b26-880d-36fb28523ee9)

**Quantidade de mensagens por usuário por dia.**

![image](https://github.com/Vi4Na/Data-Pipeline-on-Telegram/assets/136501829/204ebb0c-4cd7-4be9-aa89-4f05b9f34dc1)

**Média do tamanho das mensagens por usuário por dia.**

![image](https://github.com/Vi4Na/Data-Pipeline-on-Telegram/assets/136501829/ff7f9f11-7f60-4a09-b812-b09f11ceb3ff)

**Quantidade de mensagens por hora por dia da semana por número da semana.**

![image](https://github.com/Vi4Na/Data-Pipeline-on-Telegram/assets/136501829/08592abd-dd04-4487-a08c-59e01b864954)
