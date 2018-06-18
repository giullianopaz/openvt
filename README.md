# Ajuda para configurar e executar a OpenVT - Open Vocabulary Tree

## Passo 0 - Instalar OpenCV e dependências

	Tutorial: [https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/]

## Passo 1 - Instalar MySQL
    
    Tutorial: [https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04]

    $ pip install msqlclient

## Passo 2 - Compilar biblioteca C++ 
    
    Acessar a pasta c_modules/ e executar:
	
	$ sudo python3 setup.py build_ext --inplace

## Passo 3 - Compilar biblioteca Cython
	
	Acessar a pasta cython_modules/ e executar:
    
    $ cython cp_utils.pyx 

    $ sudo python3 setup.py build_ext --inplace

## Passo 4 - Extrair descritores do conjunto de imagens

	$ python3 extract.py

## Passo 5 - Executar aplicação

    $ python3 app.py