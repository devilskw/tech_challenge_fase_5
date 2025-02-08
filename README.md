# Hackaton- Fase 5


## Integrantes

Samuel Kazuo Watanabe
kazuo_w@hotmail.com

Jonathan Maximo da Silva
jonathan.desenv@gmail.com


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

### Dataset para baixar imagens de facas

Pesquisando na internet, vimos outros artigos e estudos que também trabalharam com treino de modelos para facas, onde indicavam dataset para treino do modelo contendo uma gama de imagens positivas e negativas de facas, o que apoia muito o nosso trabalho e estaremos utilizando aqui. Abaixo, a url da fonte do dataset para apoiar caso desejemos utilizar (deverá ser feito o download para a pasta assets/in/training do projeto).

[Knifes Images Database](https://kt.agh.edu.pl/~matiolanski/KnivesImagesDatabase/)

Segundo informações, ele possui 9340 exemplos negativos e 3359 exemplos positivos. Como o uso é somente para estudo/trabalho, ele pede para citar o artigo: [CCTV object detection with fuzzy classification and image enhancement, Andrzej MATIOLAŃSKI, Aleksandra MAKSIMOWA, Andrzej DZIECH, Multimedia Tools and Applications, 2015, pages 1-16, ISSN 1573-7721, doi:10.1007/s11042-015-2697-z
Available at: http://link.springer.com/article/10.1007%2Fs11042-015-2697-z](http://link.springer.com/article/10.1007%2Fs11042-015-2697-z)

### Vamos utilizar o VENV

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

Para debugar a aplicação, você poderá instalar através do comando abaixo:

```
.venv/Scripts/pip.exe install -r requirements.txt
```

ou então instalar manualmente

```
# .venv/Scripts/pip.exe install unrar
.venv/Scripts/pip.exe install --upgrade fastai
.venv/Scripts/pip.exe install --upgrade opencv-python
.venv/Scripts/pip.exe install --upgrade matplotlib
```




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
