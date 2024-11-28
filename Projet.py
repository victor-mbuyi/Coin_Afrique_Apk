import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import re
import plotly.express as px 




st.markdown("<h1 style='text-align: center; color: blue;'>COIN AFRIQUE DATA APK</h1>", unsafe_allow_html=True)

st.markdown(""" 

**This application enables efficient web scraping of data from coin afrique across multiple pages. Additionally, users can directly download the extracted data from the app 
            without needing to run the scraping process again.**  

**Data source:** [coin-Afrique-villas](https://sn.coinafrique.com/categorie/villas) 
            --[coin-Afrique-terrains](https://sn.coinafrique.com/categorie/terrains)--[coin-Afrique-Appartements](https://sn.coinafrique.com/categorie/appartements)

""")


# Background function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


@st.cache_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def load(dataframe, title, key, key1) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key1):
        # st.header(title)

        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

        csv = convert_df(dataframe)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key = key)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fonction for web scraping vehicle data
def load_villas_df(mul_page):
    # create a empty dataframe df
    df = pd.DataFrame()
    # loop over pages indexes
    for p in range(1, int(mul_page)+1): 
        url=f'https://sn.coinafrique.com/categorie/villas?page={p}'
        # get the html code of the page using the get function requests
        res=get(url)
        # store the html code in a beautifulsoup objet with a html parser (a parser allows to easily navigate through the html code)
        soup = bs(res.text , 'html.parser')
        # get all containers that contains the informations of each car
        containers=soup.find_all('div',class_='col s6 m4 l3')
        # scrape data from all the containers
        data = []
        for container in containers: 
            try:
                # Extraire les informations nécessaires
                id_types = container.find('p', class_='ad__card-description').text.strip().split()
                id_type = id_types[0]

                # Get address
                address = container.find('p', class_='ad__card-location').span.text.strip()

                # Scrape the price
                price = container.find('p', class_='ad__card-price').text.strip().replace(' ', '').replace('CFA', '')

                # Get image link
                img_link = container.find('a', class_='card-image ad__card-image waves-block waves-light').img['src']

                # Extract the number of pieces
                number_piece = container.find('p', class_='ad__card-description').text.strip()
                extracted_number = re.search(r'\d+', number_piece)
                number_of_part = extracted_number.group()
                if int(number_of_part)>50:
                    number_of_part=np.nan
                # Create the Description based on the condition for 'piece'
                description = "Il s'agit du nombre de mètres carrés" if int(number_of_part) > 50 else ''

                # Create the dictionary for the current container
                dic = {
                    'id_type': id_type,
                    'price': price,
                    'adress': address,
                    'number_of_part': number_of_part,
                    'img_link': img_link,
                    'Description': description}

                # Append the dictionary to the data list
                data.append(dic)
                
            except: 
                pass
        
        DF = pd.DataFrame(data)
        df= pd.concat([df, DF], axis =0).reset_index(drop = True) 
    return df   

def load_terrains(mul_page):
    # create a empty dataframe df
    df=pd.DataFrame()
    # loop over pages indexes
    for page in range (1,int(mul_page)+1):
        url=f'https://sn.coinafrique.com/categorie/terrains?page={page}'
        #get the html code of the page using the get function reauests
        res=get(url)
        # store the html code in a beautifulsoup object zith a html panser
        soup=bs(res.text,'html.parser')
        # get all containers that contains the informations of each car
        containers=soup.find_all('div',class_='col s6 m4 l3')
        data=[]
        for container in containers:
            try:
    
                #scrape area
                info=container.find('p',class_='ad__card-description').text
                info_research = re.search(r'(\d+)\s?m²', info)
                area= info_research.group()

                #scrape the price
                price=container.find('p',class_='ad__card-price').text.strip().replace(' ','').replace('CFA','')

                #get address
                address = container.find('p',class_='ad__card-location').span.text.strip()

                # get image link
                img_link=container.find('a',class_='card-image ad__card-image waves-block waves-light').img['src']

    
                dic={'area':area,
                'adress':address,
                'price' : price,
                'img_link':img_link}
            
                data.append(dic)
            except:
                pass
        DF=pd.DataFrame(data)
        df=pd.concat([df,DF], axis=0 ).reset_index(drop=True)

    return df   



def load_appartements(mul_page):
    # create a empty dataframe df
    df=pd.DataFrame()
    # loop over pages indexes
    for page in range (1,int(mul_page)+1):
        url=f'https://sn.coinafrique.com/categorie/appartements?page={page}'
        #get the html code of the page using the get function reauests
        res=get(url)
        # store the html code in a beautifulsoup object zith a html panser
        soup=bs(res.text,'html.parser')
        # get all containers that contains the informations of each car
        containers=soup.find_all('div',class_='col s6 m4 l3')
        data=[]
        for container in containers:
            try:
    
                #get number of parts
                number_piece = container.find('p', class_='ad__card-description').text.strip()
                extracted_number = re.search(r'\d+', number_piece)
                if extracted_number:
                    number_of_part = extracted_number.group()
                else:
                    number_of_part="Aucune correspondance trouvée pour le nombre de pièces."
                #scrape the price
                price=container.find('p',class_='ad__card-price').text.strip().replace(' ','').replace('CFA','')
                #get address
                address = container.find('p',class_='ad__card-location').span.text.strip()
                # get image link
                img_link=container.find('a',class_='card-image ad__card-image waves-block waves-light').img['src']
            
                dic={'number_of_part':number_of_part,
                    'adress':address,
                    'price' : price,
                    'img_link':img_link}
                data.append(dic)    
            
            except:
                pass
        DF=pd.DataFrame(data)
        df=pd.concat([df,DF], axis=0 ).reset_index(drop=True)

    return df   





st.sidebar.header('User Input Features')
Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(2, 119)]))
Choices = st.sidebar.selectbox('Options', [ 'Dashbord of the data','Scrape data using beautifulSoup', 'Data craped using webscraper',  'Fill the form'])



add_bg_from_local('img_file.jpg') 

local_css('style.css')  


if  Choices == 'Dashbord of the data': 
    df1 = pd.read_csv('clean_villa.csv')
    df2 = pd.read_csv('clean_area.csv')
    df3 = pd.read_csv('clean_appartement.csv')




     # calculate KPI
    df1['price'] = pd.to_numeric(df1['price'], errors='coerce')
    moyenne_prix1 = df1['price'].mean()
    nombre1= moyenne_prix1/1000
    average_price1= round(nombre1, 1)

    # calculate KPI
    df2['price'] = pd.to_numeric(df2['price'], errors='coerce')
    moyenne_prix2 = df2['price'].mean()
    nombre2= moyenne_prix2/1000
    average_price2= round(nombre2, 1)


    # calculate KPI
    df3['price'] = pd.to_numeric(df3['price'], errors='coerce')
    moyenne_prix3 = df3['price'].mean()
    nombre3= moyenne_prix3/1000
    average_price3= round(nombre3, 1)



    
    first_column, second_column,third_column=st.columns(3)

    with first_column:
        st.subheader('average price villa :')
        st.write(f'FCFA {average_price1}')
    with second_column:
        st.subheader('average price Area :')
        st.write(f'FCFA {average_price2}')
    with third_column:
        st.subheader('average price Appartement :')
        st.write(f'FCFA {average_price3}')

    st.divider()
 

    #plot bar chat to show price per brand
    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(10, 10))  # Un seul axe

        # Création du boxplot
        sns.boxplot(data=df1, y="number_of_part", ax=ax, color="lightgreen")
        ax.set_title("Boxplot of part numbers")
        ax.set_xlabel("")  # Pas de texte sur l'axe x
        ax.set_ylabel("Values")
        ax.tick_params(axis='x', bottom=False, labelbottom=False)  # Masquer les étiquettes x

        # Ajuster l'espacement
        plt.tight_layout()

        # Afficher dans Streamlit
        st.pyplot(fig)

        
    with col2:
        plot2 = plt.figure(figsize=(10, 10))
        # Extraire les données des 5 premières places les plus achetes
        adress = df2.adress.value_counts()[:5]
        labels = adress.index  # 
        sizes = adress.values  # Valeurs correspondantes

        # Créer un graphique circulaire
        plt.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',  # Pourcentage affiché
            startangle=90,  # Départ du graphique à 90°
            colors=plt.cm.Pastel1.colors,  # Palette de couleurs
            wedgeprops={"edgecolor": "black"}  # Bordure des segments
        )
        plt.title('Five most popular places')
        st.pyplot(plot2)



    st.divider()


    col3, col4= st.columns(2)

    df3_filtered = df3[df3['address'].isin(df3['address'].unique()[:5])]

    with col3:
        # Création de la figure
        plot3 = plt.figure(figsize=(10, 10))
        
        # Création du diagramme à barres
        sns.barplot(data=df3_filtered, x='address', y="price", palette="viridis")
        
        # Configuration du titre et des axes
        plt.title('Price distribution by location (Top 5)', fontsize=16)
        plt.xlabel('Lieu', fontsize=14)
        plt.ylabel('Prix', fontsize=14)
        plt.xticks(rotation=45)  # Rotation des étiquettes si nécessaire
        
        # Affichage dans Streamlit
        st.pyplot(plot3)



    with col4:
        # Résumer les données
        df_summary = df1.groupby("address")["price"].mean().reset_index()  # Moyenne des prix par address
        df_summary = df_summary.sort_values(by="address")  # Tri par address pour une évolution cohérente

        # Limiter aux 5 premières adresses
        df_summary = df_summary.head(5)  # Conserver uniquement 5 valeurs

        # Configurer les données pour le graphique
        labels = df_summary["address"]  # Les adresses comme étiquettes
        values = df_summary["price"]    # Moyenne des prix correspondants

        # Créer le graphique d'évolution
        plot4 = plt.figure(figsize=(10, 10))  # Taille du graphique
        plt.plot(labels, values, marker='o', linestyle='-', color='b', label="Prix moyen")  # Courbe avec marqueurs

        # Ajouter des titres et des légendes
        plt.title("Price distribution by location (Top 5)")
        plt.xlabel("Address")
        plt.ylabel("Prix moyen")
        plt.xticks(rotation=45)  # Rotation des étiquettes pour lisibilité
        plt.legend(loc="upper right")  # Légende pour la courbe

        # Afficher le graphique
        st.pyplot(plot4)

elif Choices=='Scrape data using beautifulSoup':

    villas_data_mul_pag = load_villas_df(Pages)
    terrains_data_mul_pag = load_terrains(Pages)
    appartements_data_mul_pag = load_appartements(Pages)
    
    load(villas_data_mul_pag, 'villas data', '1', '101')
    load(terrains_data_mul_pag, 'terrains data', '2', '102')
    load(appartements_data_mul_pag, 'appartements data', '3', '103')

elif Choices == 'Data craped using webscraper': 
    data_villas1 = pd.read_csv('my_villa.csv')
    data_terrains1 = pd.read_csv('my_terrains.csv') 
    data_appartemets1 = pd.read_csv('my_appart.csv') 

    load(data_villas1, 'Villas data', '1', '101')
    load(data_terrains1, 'Terrains data', '2', '102')
    load(data_appartemets1, 'Appartements data', '3', '103')


else :
    components.html("""
    <iframe src="https://ee.kobotoolbox.org/x/0a9QkpJU" width="800" height="1100"></iframe>
    """,height=1100,width=800)



















 


