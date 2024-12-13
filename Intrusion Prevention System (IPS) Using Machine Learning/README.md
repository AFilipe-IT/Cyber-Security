
# 🚨 Sistema de Prevenção de Intrusões (IPS) com Machine Learning

Este projeto implementa um **Sistema de Prevenção de Intrusões** (Intrusion Prevention System - IPS) utilizando **Machine Learning** para detectar e bloquear automaticamente atividades maliciosas em redes de computadores. Após identificar um tráfego suspeito, o sistema bloqueia o endereço IP do atacante utilizando o **iptables**.

Este IPS foi construido em três etapas principais:

1. **Treinamento do Modelo**: Utiliza dados históricos para criar um modelo de Machine Learning capaz de identificar ataques.
2. **Configuração do Ambiente**: Prepara um ambiente (para teste testes) de rede e firewall (`iptables`) para bloqueio automatizado.
3. **Implementação do Modelo**: Captura pacotes em tempo real, realiza a detecção e aplica bloqueios automáticos.

## ⚙️ Funcionalidades

- 📡 **Monitoramento em Tempo Real**: Captura de tráfego de rede em tempo real.
- 🧠 **Detecção de Intrusões**: Identificação de tráfego malicioso usando Machine Learning.
- 🔒 **Bloqueio Automático**: Bloqueio de IPs suspeitos com `iptables`.

## 📄 Explicação dos Diretórios

- **`dataset/`**: Contém o conjunto de dados utilizado para treinar e testar o modelo.
- **`models/`**: Armazena o modelo de Machine Learning treinado e escolhido para a implementação (`model.pkl`).
- **`scripts/`**:
  - **`Attacker`**: Contém os scripts para gerar trafégo.
  - **`Client`**: Contém os scripts para executar o IPS.
- **`*.ipynb`**: Arquivos para treinamento do modelo.

## 🚀 Fluxo para a Execução do Projeto
### 1️⃣ **Criação do Modelo de Machine Learning**

Para recriar ou retreinar o modelo de Machine Learning, siga os passos abaixo para configurar o ambiente de desenvolvimento local. Caso não tenha um computador com GPU ou recursos suficientes, há uma opção alternativa de utilizar o **Google Colab**. Caso não deseja, basta utilizar o modelo salvo na pasta *modelos_salvos*.

#### 💻 **Configuração do Ambiente para Treinamento Local**

##### 1. Instalar o Anaconda

Faça o download e instale o **Anaconda Navigator** no seu sistema operacional:

🔗 [Download do Anaconda](https://www.anaconda.com/download)
🔗 [Download do Dataset](https://www.unb.ca/cic/datasets/ids-2017.html) e guarde no diretorio dataset/CICIDS2017

#### 2. Criar e Configurar o Ambiente Virtual

Abra o **Anaconda Prompt**, navegue até o diretório dos arquivos do projeto e execute os seguintes comandos:

```bash
# 1. Criar um ambiente virtual chamado 'SRproj' com Python 3.10
conda create -n SRproj python=3.10

# 2. Ativar o ambiente virtual
conda activate SRproj

# 3. Instalar o CUDA Toolkit e cuDNN (para quem possui GPU Nvidia)
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0

# 4. Instalar o kernel para Jupyter Notebook
conda install -c conda-forge ipykernel

# 5. Adicionar o kernel ao Jupyter Notebook
python -m ipykernel install --user --name=SRproj

# 6. Instalar o Jupyter Notebook e as dependências do projeto
pip install jupyter
pip install -r requirements.txt

# 7. Iniciar o Jupyter Notebook
jupyter notebook
```
📝 Executar os Notebooks
Execute os notebooks (.ipynb) em ordem numérica para retreinar o modelo, ajustando os parâmetros conforme necessário.

### 2️⃣ **Setup do Ambiente para Testes**

Neste passo, configuramos um ambiente de testes utilizando o **VirtualBox** para criar uma rede interna entre duas máquinas virtuais. Uma das máquinas executará o **IPS** e a outra será responsável por injetar pacotes do conjunto de dados de teste. A seguir, estão as etapas detalhadas para a configuração do ambiente:

#### 🖥️ **Ambiente Virtual**

1. **Criação de Máquinas Virtuais**: Utilizamos o **VirtualBox** para criar duas máquinas virtuais:
   - **Ubuntu**: Esta máquina será responsável por executar o **IPS**. 4GB de RAM e 20 de memoria foram suficientes.
   - **Linux Mint**: A segunda máquina será utilizada para injetar pacotes maliciosos do conjunto de dados para testar o sistema. Pode se utilizar uma distribuição mais leve no lugar

2. **Configuração de Rede**:
   - Criamos uma **NAT Network** no VirtualBox, o que permite que as máquinas virtuais se comuniquem entre si em uma rede interna e também tenham acesso à internet para a instalação dos pacotes necessários.

### 🔧 **Instalação dos Pacotes e Ferramentas**

#### Na máquina Ubuntu (que irá executar o IPS):

1. **Instalação do iptables**: O **iptables** é necessário para aplicar o bloqueio de IPs maliciosos detectados pelo sistema.
   - Para instalar o `iptables` e outras dependencias:
   ```bash
   sudo apt update && sudo upgrade -y
   sudo apt install python3
   sudo apt install iptables
   sudo apt install python3-scapy python3-numpy python3-joblib python3-pyshark python3-pandas python3-requests python3-json python3-subprocess
   sudo apt install wireshark
   ```
#### No Mint (que irá executar o IPS):

Instalação do Python e Scapy: O Linux Mint irá utilizar o Python e o Scapy para injetar pacotes maliciosos do conjunto de dados para o sistema de testes.
Para instalar:
```bash
sudo apt install python3
sudo apt install python3-scapy python3-pandas
```
### 3️⃣ Implementação do Modelo

Nesta etapa, o modelo treinado é integrado ao sistema IPS na máquina **Ubuntu**. A implementação é feita utilizando um script chamado `package_receive_controlled.py`. Este script monitora o tráfego de rede em tempo real, analisa os pacotes recebidos, faz previsões utilizando o modelo e bloqueia IPs maliciosos automaticamente com o **iptables**.

### 📝 **Descrição do Script**

O script `package_receive_controlled.py` realiza as seguintes tarefas:

1. **Captura Pacotes UDP** em uma interface de rede específica utilizando o **PyShark**.
2. **Decodifica o Payload** dos pacotes recebidos para o formato JSON.
3. **Envia os Dados** para uma API de previsão em execução local (`http://127.0.0.1:9000/predict`).
4. **Interpreta a Resposta** da API:
   - Se a resposta for `"1"` (indicando tráfego malicioso), o script verifica se o IP de origem já está bloqueado.
   - Se não estiver bloqueado, adiciona uma regra no **iptables** para bloquear o IP.
5. **Loga as Ações** realizadas no terminal.
---
Para executar o script basta entrar no diretorio scipts e executar o comando
``` bash
sudo python3 package_receive_controlled.py
```
O comando deve ser executado como sudo para permissões de monitoramento da interface. 
E o script *rest_controlled.py* que é a nossa api deve estar em execução.

### 4️⃣ **Testes e Validação do Sistema**
Após configurar o IPS na máquina Ubuntu, é necessário validar o sistema para garantir que ele detecta e bloqueia corretamente o tráfego malicioso. Para isso, utilizamos dois scripts na máquina Linux Mint:

- Script de Tráfego Benigno: Este script envia pacotes simulando tráfego benigno, permitindo verificar se o sistema IPS não gera bloqueios indevidos.
- Script de Tráfego Malicioso: Este script envia pacotes simulando tráfego malicioso, possibilitando verificar se o sistema IPS detecta e bloqueia os ataques corretamente.

#### 🚀 Execução dos Testes
Para realizar os testes, siga os seguintes passos na máquina Linux Mint:

Certifique-se de que a máquina Ubuntu com o IPS está ativa e aguardando pacotes para análise.
Execute o Script:

```bash
sudo python3 benign_traffic_sender.py
```
ou para trafego malicioso
```bash
sudo python3 malicious_traffic_sender.py
```

#### ✅ Resultados Esperados
- Para Tráfego Benigno:
O sistema IPS deve permitir o tráfego e não bloquear o IP da máquina que enviou os pacotes.
- Para Tráfego Malicioso:
O sistema IPS deve detectar os pacotes maliciosos e bloquear automaticamente o IP da máquina que realizou o envio.

#### 📝 Dica
Monitoramento em Tempo Real: Utilizar o Wireshark na máquina Ubuntu para monitorar os pacotes recebidos e as ações do IPS em tempo real.
Esses testes são essenciais para validar a eficácia do seu sistema de prevenção de intrusões e garantir que ele funciona conforme esperado.

## Autores

- [@Alberto Filipe](https://github.com/AFilipe-IT)
- Edmilson S. S. Almeida
- João Moura