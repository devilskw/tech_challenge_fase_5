# Hackaton- Fase 5


## Integrantes

Samuel Kazuo Watanabe
kazuo_w@hotmail.com

Jonathan Maximo da Silva
jonathan.desenv@gmail.com

Samuel Rodrigues De Barros Mesquita Neto
samuelr.neto98@gmail.com


## Sobre o desafio

O Desafio é criar um sistema para a empresa fictícia "Fiap VisionGuard" que utilize Inteligência Artificial para identificar objetos cortantes (facas, tesouras e similares) e emitir alertas para a central de segurança.

A empresa tem o objetivo de validar a viabilidade dessa feature, e para isso, será necessário fazer um MVP para detecção supervisionada desses objetos.


### Objetivos

-  Construir ou buscar um dataset contendo imagens de facas, tesouras e outros objetos cortantes em diferentes condições de ângulo e iluminação;
-  Anotar o dataset para treinar o modelo supervisionado, incluindo imagens negativas (sem objetos perigosos) para reduzir falsos positivos;
-  Treinar o modelo;
-  Desenvolver um sistema de alertas (pode ser um e-mail).


### Entregável

-  Documentação detalhando o fluxo utilizado para o desenvolvimento da solução;
-  Vídeo de até 15 minutos explicando a solução proposta;
-  Link do github do projeto.

---


# Fiap VisionGuard - Intelligent Threat Analyzer

O sistema "Intelligent Threat Analyzer" é um sistema inteligente capaz de identificar possíveis ameaças com arma branca, mais especificamente, facas, identificadas através de análise do objeto dos vídeos gravados.


## Desenvolvimento


### Ambiente local segmentado: vamos utilizar o VENV

Se ainda não está instalado o venv para este projeto:
```
python -m venv .venv
```

Caso deseje ativar o venv no Windows:

```
.venv/Scripts/activate.bat
```

Caso deseje desativar no Windows:

```
.venv/Scripts/deactivate.bat
```


### Bibliotecas usadas pela aplicação

Para debugar a aplicação, você poderá instalar através do comando abaixo (se disponível o arquivo '**requirements.txt**'):

```
.venv/Scripts/pip.exe install -r requirements.txt
```

ou então instalar manualmente

```
.venv/Scripts/pip.exe install --upgrade fastai
.venv/Scripts/pip.exe install --upgrade opencv-python
.venv/Scripts/pip.exe install --upgrade matplotlib
```


### Preparar o dataset com imagens de facas

Pesquisando na internet, vimos outros artigos e estudos que também trabalharam com treino de modelos para facas, onde indicavam dataset para treino do modelo contendo uma gama de imagens positivas e negativas de facas, o que apoia muito o nosso trabalho e estaremos utilizando aqui. Abaixo, a url da fonte do dataset para apoiar caso desejemos utilizar (deverá ser feito o download para a pasta assets/in/training do projeto).

[Knifes Images Database](https://kt.agh.edu.pl/~matiolanski/KnivesImagesDatabase/)

Segundo informações, ele possui 9340 exemplos negativos e 3359 exemplos positivos. Como o uso é somente para estudo/trabalho, ele pede para citar o artigo: [CCTV object detection with fuzzy classification and image enhancement, Andrzej MATIOLAŃSKI, Aleksandra MAKSIMOWA, Andrzej DZIECH, Multimedia Tools and Applications, 2015, pages 1-16, ISSN 1573-7721, doi:10.1007/s11042-015-2697-z
Available at: http://link.springer.com/article/10.1007%2Fs11042-015-2697-z](http://link.springer.com/article/10.1007%2Fs11042-015-2697-z).

Os passos abaixo deverão ser realizados para debugar a aplicação, tendo em vista que não deixaremos disponbilizado os arquivos aqui devido às limitações de espaço para o Github pessoal.

-  Descompactar o arquivo RAR (É necessário ter na máquina um descompactador compatível com arquivos .rar) contendo o dataset para a pasta '***assets/in/training***'. Ao descompactar irá criar a pasta '**KnivesImagesDatabase**'. Se criar uma subpasta com o mesmo nome, mova para a pasta-pai para não ter problemas na hora de executar o programa;
-  Dentro desta pasta '**KnivesImagesDatabase**', copie e cole o arquivo '**prepare.bat**', que está na pasta '**assets/in/training**';
-  No prompt de comando do Windows, vá até a pasta '**assets/in/training/KnivesImagesDatabase**' e execute o script '**prepare.bat**'. O processo poderá demorar alguns minutos;
-  A pasta '**assets/in/training/KnivesImagesDatabase** deverá conter as imagens .BMP com prefixo '***threat***' ou '***no-threat***'.

**Atualização**:

Adicionamos mais datasets para treinar o modelo novamente:

https://universe.roboflow.com/psa-co4la/cutter-cdfyg
https://universe.roboflow.com/dhruv-5dc1m/detect-2/dataset/1
https://universe.roboflow.com/object-detection-practice-dgcci/cutter-dchc8/dataset/2


Também imagens de não ameaças, como guarda-chuvas:
https://universe.roboflow.com/pruebas-0f3uc/umbrella-slab3/dataset/1
https://universe.roboflow.com/sulton/umbrelladetection



### Modelo criado

Para agilizar, vamos tentar deixar o(s) modelo(s) já criado(s) na pasta '**assets/out/training/**', tendo em vista que o treino do modelo poderá ser demorado (nos vários testes realizados, cada epoch do treino levou cerca de 35 minutos).


### Configurações para execução

O arquivo '**assets/config/config.json**' possui alguns parâmetros para configuração, sendo:

| variável | descricao | valores possiveis |
| --- | --- | --- |
| training | Estrutura para configurações de treinamento do modelo | - |
| training.train |  Indica se deseja ou não treinar um modelo. Se active for true, ele somente irá analisar um modelo informado | true ou false |
| training.debug | Para uso do time de desenvolvimento (permite algumas análises) | true ou false |
| training.model_filename | Indicação do nome do arquivo de modelo que deseja gerar, com extensão .PKL | - |
| training.input_path | Indicação da pasta onde se encontram os datasets, ou seja, as imagens de treino | - |
| training.output_path | Indicação da pasta onde será salvo o modelo treinado | - |
| training.qtd_epoch | Quantidade de epochs para treinamento do modelo | Um valor numérico inteiro maior que zero. |

| analyzer | Estrutura para configurações de análise de video | - |
| analyzer.webcam | Estrutura para configurações de análise com webcam | - |
| analyzer.webcam.active | Indica se a webcam deverá ser usada para análise de video. Em caso negativo, irá considerar o video no caminho indicado para análise | true ou false |
| analyzer.video | Estrutura para configurações de análise de video | - |
| analyzer.video.path | Estrutura para configurações de análise de video | - |
| analyzer.video.path.in | Indicação da pasta onde se encontram os videos para análise | - |
| analyzer.video.path.out | Indicação da pasta onde serão salvos os videos e demais arquivos processados/resultantes | - |
| analyzer.video.path.filenames | Lista de nomes dos videos para análise | - |






https://embarcados.com.br/processamento-de-imagens-com-opencv-no-raspberry-pi-zero/
https://www-geeksforgeeks-org.translate.goog/detect-an-object-with-opencv-python/?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc
https://learnopencv.com/moving-object-detection-with-opencv/
https://pypi.org/project/fastai/
https://medium.com/hackernoon/recognising-a-knife-in-an-image-with-machine-learning-c7479f80525
https://andreas-varotsis.medium.com/automating-knife-classification-with-machine-learning-3767d93d2789

https://medium.com/hackernoon/recognising-a-knife-in-an-image-with-machine-learning-c7479f80525
https://github.com/ruairidhwm/knife-finder
https://walkwithfastai.com/vision.clas.single_label
https://medium.com/@serverwalainfra/understanding-fastais-learner-object-13e6982b2eac



https://github.com/gdoteof/neuralnet_stuff/blob/master/kaggle_whales.ipynb
https://benjaminwarner.dev/2021/10/01/inference-with-fastai
