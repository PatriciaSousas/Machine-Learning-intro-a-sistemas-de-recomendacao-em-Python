# Machine-Learning-intro-a-sistemas-de-recomendacao-em-Python

O algoritmo de k-vizinhos mais próximos (KNN) é um algoritmo de aprendizado de máquina simples e supervisionado que pode ser usado para resolver problemas de classificação e regressão
Classificação: Sub-categoria de aprendizagem supervisionada, são geralmente usados quando as previsoes são de natureza distinta(sim ou não)


- Eu consigo iniciar a recomendação entendendo que tipo de dados eu possuo para analisar aqui por exemplo eu tenho dados das notas que foram avaliadas e os filmes mais assistidos, a partir dos filmes e das notas começa a grupar por filmes , trazendo uma classificao natural dos filmes mais avaliados 
e podemos entender que esse filmes são os que podemos recomendar (hiposete) 

- Uma segunda maneira de fazer a recomendação é pela media das notas dos filmes, eu consigo usar a media nesse calculo quando os valores são mais ou menos de forma uniforme, sem grandes discrepancias 
e aqui eu consigo observar que não necessariamente o mais popular em notas é o mais assitido pelos o usuarios 

- Levo em  consideração a populariedade dos filmes,isso impacta diretamente nos resultados e no impacto dos filmes como também a recomendação por genêro também é um caminho para recomendar mais filmes para o usuario trilhar

- Posso seguir um recomendação por genêro também, considerando apenas os filmes que um usuario assistiu sem a corroboração de outras informações, aqui eu tenho um ponto importante
que é a recomendação por genero mais assististido conseguindo trilhar o que o usuario mais gosta 

- Uma outra maneira de recomendação seria por usuario, entendendo a pontuação que cada usuario deu em um determinado filme e e trazendo um comparativo por notas, exemplo: qual seria a diferença? é proxímo? será que Joao gostaria do mesmo filme que Maria recomendou?

joao pontou X filme com 4.5
Maria pontou X filme com 5 


