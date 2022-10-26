#!/usr/bin/env python
# coding: utf-8

# # Bibliotecas

# In[147]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:





# ### 1- Análise

# In[148]:


filmes = pd.read_csv('movies.csv')                #carregamento dataset
filmes.columns=['Filmes', 'Titulo', 'Gênero']
filmes = filmes.set_index("Filmes")
filmes


# In[149]:


notas = pd.read_csv('ratings.csv')
notas.columns=['usuarioid', 'filmeId', 'Nota', 'momento']
notas


# In[150]:


notas.describe                  #as notas chegam de 3 a 5 estrelas de avaliações


# # Primeira tentativa de recomendação

# In[151]:


total_de_votos = notas['filmeId'].value_counts()   #filmes mais avaliados apartir das notas é o 356
total_de_votos 


# In[152]:


filmes.loc[356]               #busco pelo index e o filmes Age of Innocence, The (1993) foi o mais avaliado


# In[153]:


filmes['total_de_votos'] = total_de_votos  #inclui no dataframe o total de votos por filme
filmes.head()


# In[154]:


filmes.sort_values("total_de_votos",ascending =False).head() #aqui a heuristica traz uma recomendação apartir dos numeros de notas e filmes 


# In[155]:


notas_medias = notas.groupby('filmeId').mean()['Nota'] #nota media dos filmes 
notas_medias


# In[156]:


filmes['notas_medias'] = notas_medias  #inclui a media dos filmes no dataframe


# In[157]:


filmes.head(10)                      #se eu recomendar pela media das notas Jumaji fica em primeiro lugar na recomendação 


#  ## Segunda Heurística

# In[158]:


filmes.query('total_de_votos >=10').sort_values("total_de_votos",ascending =False).head() #fiz uma ordenação onde eu anulei os numero abaixo de 10 notos e refletindo somente a media


# In[159]:


filmes_com_mais_de_50_votos = filmes.query('total_de_votos >=50').sort_values("total_de_votos",ascending =False).head() #fiz uma nova ordenação trazendo mais dados 
filmes_com_mais_de_50_votos


# ##  Recomendação baseada em similaridade de genero

# In[160]:


eu_assisti = [1, 21, 19, 10, 11, 7, 2]  #selecionei os filmes que supostamente eu assisti para fazer uma recomendação por filme de genero similar
filmes.loc[eu_assisti]


# filmes.query("Gênero == 'Adventure|Children|Fantasy'")  #escolhi a última categoria de filme que eu assisti

# In[161]:


aventura_infantil_e_fantasia= filmes_com_mais_de_50_votos.query("Gênero=='Adventure|Children|Fantasy'")
aventura_infantil_e_fantasia.sort_values("notas_medias",ascending =False).head()               #chamei a query para ler/trazer os demais filmes que eu assisti e ordei pela nota media  


# ## Procurando usuarios similares -gerando novas recomendações

# Procurando usuarios similares é uma outra maneira de recomendação, buscando por usuarios que deram notas similares em determinado filmes 

# In[162]:


#joao = [4,4.5]
#maria = [5,5]  #Aqui eu criei um exemplo para distinguir dois possivéis usuarios dando notas para dois filmes diferentes 


# In[163]:


plt.plot(4,4.5, "go")     #plotei um grafico para entender a distencia que eles estão de acordo apenas com a nota que eles deram nos filmes, inclui um triângulo retângulo,e para calcular a distância entre João e Maria só preciso descobrir a hipotenusa desse triângulo.
plt.plot(5,5, "yo")
plt.legend(["Joao", "Maria"])
plt.title("Calcular a distancia entre usuários")

plt.plot([4, 5], [4.5, 4.5],color ="b", linestyle="-")
plt.plot([4, 5], [4.5, 5],color ="b", linestyle="-")
plt.plot([5, 5], [5, 4.5],color ="b", linestyle="-")


# In[164]:


joao = np.array([4,4.5])  #com array numpy eu consigo calcular a diferença entre os eixo x e y dos filmes avaliados 
maria =np.array([5,5]) 
joaquina= np.array([3.5,4.5])

joao -maria


# In[165]:


from math import sqrt       #calculo da hipotenusa e a diferença dos dois usuarios é de 1.18

def pitagoras(a,b):
    (delta_x, delta_y) = a-b
    return sqrt (delta_x * delta_x + delta_y * delta_y)
pitagoras(joao,maria)


# In[166]:


def pitagoras (a,b):          #posso aplica com numpy esse calculo
    return np.linalg.norm(a-b)
pitagoras(joao,maria)


# ### Exemplo com 3 vetores(usuarios)

# In[167]:


plt.plot(4,4.5, "go")    #posso aplicar esse mesmo calculo com mais vetores
plt.plot(5,5, "yo")
plt.plot (3.,5,4.5 ,"bo")
plt.legend(["Joao", "Maria", "joaquina"])
plt.title("Calcular a distancia entre usuários")


# In[168]:


#aqui eu consigo observa que Joaquina tem uma pontuação mais proxima do Joao (0.5) então quando eu for recomenda um filme eu irei ver os filmes da Joaquina primeiro 
print(pitagoras(joao,maria)) 
print (pitagoras(joao, joaquina))


# In[169]:


def distancia_vetores (a,b):          #renomei a função e aqui eu posso trazer mais de 1 vetor para analisar a diferença das pontuações do usuarios
    return np.linalg.norm(a-b)


# ### Implementando a distância entre usuários no  dataset

# In[170]:


def notas_usuarios(usuario):                            #extraindo as notas dos usuarios apartir das notas classificadas por cada filme
    notas_usuarios = notas.query("usuarioid == %d" %usuario)   
    notas_usuarios =notas_usuarios[['filmeId', 'Nota']].set_index("filmeId")
    return notas_usuarios


# In[171]:


notas_usuarios(1) #Usuario 1 classificou 16 filmes


# In[172]:


usuario1 =notas_usuarios(1)  #pego os usuarios 1 e 4 para gerar um modelo de comparação de vetores comparando cada usuario e cada classificação de filme
usuario4 =notas_usuarios(4)


# In[173]:


#eu quero apenas os filmes que os dois usuarios(usuarios 4 e 1) assistiram mesmo eu aplicando o join e ele considerar apenas os dados da esquerda
#exclui os dados com NULL para limpar os dois vetores, e calculo a distancia entre eles (a distancia aqui se refere ao quanto de pontuação ou ou outro deu na classificacao dos filmes

diferencas = usuario1.join(usuario4, lsuffix = "_esquerda", rsuffix = "_direita").dropna() 
distancia_vetores (diferencas['Nota_esquerda'],diferencas['Nota_direita'])


# In[174]:


def distancia_de_usuarios(usuario_id1, usuario_id2): #abrir um função para aplicar esse calculo de maneira mais rapida com os mesmos tratamentos acima
    notas1 =  notas_usuarios(usuario_id1)
    notas2= notas_usuarios(usuario_id2)
    diferencas = notas1.join(notas2, lsuffix = "_esquerda", rsuffix = "_direita").dropna() 
    distancia = distancia_vetores (diferencas['Nota_esquerda'],diferencas['Nota_direita'])
    return [usuario_id1, usuario_id2, distancia_vetores]


# In[175]:


distancia_de_usuarios(1,4)


# ##### Até esse momento eu fiz a comparação de dois vetores, de 3 vetores e calculei a distancia entre eles, aqui quando eu faço distancia é o quão proxímo ou não um usuario consegue chegar em recomendação
# ##### comparado a outro usuario exemplo (Patriciavetor1 e Rodrigovetor2 calculando a distancia das notas que da usuario classificou eu consigo ver o quão proxímo eu consigo recomendar seja em filmes ou em serie para esse usuario

# In[ ]:





# ###  Calculando a distância entre um e todos os usuários

# #### A ideia nesse momento não é trazer apenas 1 ou 2 comparativos de usuarios mais sim, varios! o que possibilitará que 1 usuario, passe por todo sistema, comparando filmes e notas e o sistema me traga qual é o mais compativél para recomendação

# In[176]:


quantidade_usuarios = len(notas['usuarioid'].unique()) 
quantidade_usuarios                                 #para fazer esse calculo eu trago a os usuarios por contas e vejo quantos usuarios unicos eu tenho na base


# In[177]:


## refatorei os vetore inclui em uma função para que todas as vezes que eu quiser rodar a diferença entre um usuario e outro seja mais facil. A ideia nessa analise e entender a distancia de um 
## usuario comparando todos os usuarios da base comparando por cada usuario 

voce_id=1

def distancia_de_todos(voce_id):
    todos_usuarios = notas['usuarioid'].unique()
    distancias= [distancia_de_usuarios(voce_id,usuario_id) for usuario_id in todos_usuarios]
    distancias= pd.DataFrame(distancias,columns= ['voce', 'outra_pessoa', 'distancia'])
    return distancias

distancia_de_todos(1).head()


# ### Ordenando usuários por distância e lidando com casos extremos

# In[178]:


## diferenças minimas entre os filmes assistidos dever ser maior que zero o que significa usuarios sem nada em comum devem ser colocados diatante um do outro 


# In[179]:


def distancia_de_usuarios(usuario_id1, usuario_id2, minimo = 5): 
    notas1 =  notas_usuarios(usuario_id1)
    notas2= notas_usuarios(usuario_id2)
    diferencas = notas1.join(notas2, lsuffix = "_esquerda", rsuffix = "_direita").dropna() 
    
    if (len(diferencas) < minimo):
        return [usuario_id1,usuario_id2, 100000]
    
    distancia = distancia_vetores (diferencas['Nota_esquerda'],diferencas['Nota_direita'])
    return [usuario_id1, usuario_id2, distancia_vetores]


# ### Calculando o usuarios mais proximos de mim

# In[180]:


def mais_proximo_de(voce_id):
    distancias = distancia_de_todos(voce_id)
    distancias= distancias.sort_values("distancia")
    distancias= distancias.set_index("outra_pessoa").drop(voce_id)
    return distancias


# In[181]:


mais_proximo_de(1)


# ### Parametro para teste e recomendação com KKK

# 

# In[ ]:


def mais_proximos_de(voce_id, n = None):
  distancias = distancia_de_todos(voce_id, n = n)
  distancias = distancias.sort_values("distancia")
  distancias = distancias.set_index("outra_pessoa").drop(voce_id)
  return distancias


# In[ ]:


def distancia_de_todos(voce_id, n = None):
  todos_os_usuarios = notas['usuarioId'].unique()
  if n:
    todos_os_usuarios = todos_os_usuarios[:n]
  distancias = [distancia_de_usuarios(voce_id, usuario_id) for usuario_id in todos_os_usuarios]
  distancias = pd.DataFrame(distancias, columns = ["voce", "outra_pessoa", "distancia"])
  return distancias


# In[ ]:


def distancia_de_usuarios(usuario_id1, usuario_id2, minimo = 5):
  notas1 = notas_do_usuario(usuario_id1)
  notas2 = notas_do_usuario(usuario_id2)
  diferencas = notas1.join(notas2, lsuffix="_esquerda", rsuffix="_direita").dropna()
  
  if(len(diferencas) < minimo):
    return None
  
  distancia =  distancia_de_vetores(diferencas['nota_esquerda'], diferencas['nota_direita'])
  return [usuario_id1, usuario_id2, distancia]


# In[ ]:


def distancia_de_todos(voce_id, numero_de_usuarios_a_analisar = None):
  todos_os_usuarios = notas['usuarioId'].unique()
  if numero_de_usuarios_a_analisar:
    todos_os_usuarios = todos_os_usuarios[:numero_de_usuarios_a_analisar]
  distancias = [distancia_de_usuarios(voce_id, usuario_id) for usuario_id in todos_os_usuarios]
  distancias = list(filter(None, distancias))
  distancias = pd.DataFrame(distancias, columns = ["voce", "outra_pessoa", "distancia"])
  return distancias


# In[ ]:


def mais_proximos_de(voce_id, numero_de_usuarios_a_analisar = None):
  distancias = distancia_de_todos(voce_id, numero_de_usuarios_a_analisar = numero_de_usuarios_a_analisar)
  distancias = distancias.sort_values("distancia")
  distancias = distancias.set_index("outra_pessoa").drop(voce_id)
  return distancias


# In[ ]:


mais_proximos_de(1, numero_de_usuarios_a_analisar = 50)


# In[ ]:


sugere_para(1, numero_de_usuarios_a_analisar=50).head()


# In[ ]:


sugere_para(1).head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




