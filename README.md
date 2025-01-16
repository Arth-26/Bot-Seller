# BOT-SELLER: Your promotions consultant!
![DBbanner](media/DB_banner.png)

## Visão Geral
O ***Dealer Bot*** é um projeto pensado na comunidade gamer que quer ficar por dentro de todas as promoções de todas as plataformas e lojas digitais em um único lugar.

O *Dealer Bot* foi produzido como um bot para a plataforma de comunicação [****DISCORD****](https://*Discord*.com/), a principal usada por todos os jogadores do mundo inteiro.

## Como Funciona?
O *Dealer Bot* tem duas fases de funcionamento: (1) A execução de eventos e a (2) busca de dados. 

### 1. Execução de eventos:
Utilizando a API do *Discord* disponibilizada gratuitamente para os desenvolvendores, foram desenvolvidos comandos que são executados pelos usuários do servidor do *Discord* onde o bot está presente ou comandos programados para serem executados periodicamente.

Quando os comandos são executados, eles executam a funcionalidade de busca de dados.

### 2. Busca de dados

Na etapa de busca de dados, o sistema irá utilizar da ferramenta *Beautiful Soap* para realizar a raspagem de dados no site [***gg.deals***](https://gg.deals), onde ele busca todos os jogos na promoção de acordo com a sessão, que será selecionada pelo próprio usuário ao executar um comando.

## Instalação

### Executando o código
**1. Clone o repositório do GitHub:** Comece clonando o repositório usando o comando:

`git clone git@github.com:Arth-26/Bot-Seller.git`

**2. Crie o ambiente virtual:** Crie o ambiente virtual onde irá ser instalado as depêndencias. Para isso, use o código:

`python -m virtualenv venv`

**3. Ative seu ambiente virtual:** Agora, ative seu ambiente virtual. 

Caso seu sistema operacional seja Windows, ative usando o seguinte código:

`venv/Scripts/activate`

Caso seja Linux ou MacOs, use:

`source venv/bin/activate`

**4. Instale as dependências do projeto:** Instale todas as bibliotecas e depêndencias que serão usadas no projeto usando o código:

`pip install -r requirements.txt`

**5. Agora execute o bot:**

`python deater_bot.py`

### Convidando o BOT para o seu servidor

Para convidar o bot para o seu servidor e utilizado, [`Clique aqui!`](https://discord.com/oauth2/authorize?client_id=1295436747437772812&permissions=1719631824813297&integration_type=0&scope=bot):


## Redes
<p align="left">
  <a href="mailto:artgomesalves@gmail.com" title="Gmail">
  <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail"/></a>
  <a href="https://www.linkedin.com/in/arthur-gomes-513070241?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" title="LinkedIn">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://github.com/Arth-26" title="GitHub">
  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
</p>




