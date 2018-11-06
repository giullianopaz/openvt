# OpenVT - Open Vocabulary Tree

OpenVT é uma aplicação CBIR (Content-Based Image Retrieval) escalável e de código aberto para buscar imagens semelhantes em uma extensa base de dados. Como base, para quantização e indexação das imagens, é utilizado o trabalho proposto por [Nister e Stewenius](https://ieeexplore.ieee.org/document/1641018/), o qual introduz uma estrutura hierárquica denominada *Vocabulary Tree*.

A maior parte da aplicação foi escrita em Python. Contudo, para um melhor desempenho, alguns módulos foram escritos em [Cython](http://cython.org/) e C++. Para o tratamento e extração de informações das imagens foi utilizada a biblioteca de Visão Computacional [OpenCV](https://opencv.org/). Por fim, para a criação da interface web da OpenVT, foi utilizado o [Flask](http://flask.pocoo.org/).

### Visão geral da aplicação

![teste](https://github.com/giullianopaz/OpenVT/blob/master/visao_geral.png "Visão Geral")

### Exemplos de execução da OpenVT

#### Busca por face em uma base de dados com 400 imagens de faces
![](https://github.com/giullianopaz/OpenVT/blob/master/face.png "Busca por Face")

#### Busca por girassol em uma base de dados com 300 imagens diversas
![](https://github.com/giullianopaz/OpenVT/blob/master/girassol.png "Busca por Girassol")

#### Busca pela Torre Pisa em uma base de dados com 300 imagens diversas
![](https://github.com/giullianopaz/OpenVT/blob/master/pisa.png "Busca pela Torre Pisa")

Mais informações podem ser obtidas no documento **Monografia.pdf**, o qual explica cada detalhe da OpenVT.

### Tutorial para instalação da OpenVT (Em breve container Docker)

#### Passo 0 - Instalar OpenCV e dependências

[Como instalar OpenCV 3 no Ubuntu 16.04](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)

#### Passo 1 - Instalar MySQL

[Como instalar MYSQL no Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04)
	
	$ pip install msqlclient

#### Passo 2 - Compilar biblioteca C++ 
	
	Acessar a pasta c_modules/ e executar:
	
	$ sudo python3 setup.py build_ext --inplace

#### Passo 3 - Compilar biblioteca Cython
	
	Acessar a pasta cython_modules/ e executar:
    	
	$ cython cp_utils.pyx 

    	$ sudo python3 setup.py build_ext --inplace

#### Passo 4 - Extrair descritores do conjunto de imagens

	$ python3 extract.py

#### Passo 5 - Executar aplicação

   	$ python3 app.py
