from app import app
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import json
from flask import jsonify

@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    navegador = webdriver.Chrome()
    pessoas = ["Brain+Lag", "Why", "Dankpot7", "Romance+Dawn", "Dreadway", "Cinza+Falso", "Shallan+Davar"]
    #pessoas = ["Brain+Lag", "Why"]
    elos = []
    dados = []
    win_rate = []
    campeoes = []

    for nome in pessoas:
        campeao = []
        
        # Entra no perfil da pessoa
        navegador.get(f"https://br.op.gg/summoner/userName={nome}")
        
        # Atualiza o perfil
        #navegador.find_element_by_xpath('//*[@id="SummonerRefreshButton"]').click()
        
        time.sleep(1)
        
        # Pega os dados
        elo = navegador.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[2]/div[1]/div[2]/div/div[2]').text
        dado = navegador.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[2]/div[1]/div[2]/div/div[3]').text
        win = navegador.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[2]/div[1]/div[2]/div/div[4]').text
        
        # Campeões jogados
        for i in range(1,11):
            campeao.append(navegador.find_element_by_xpath(f'//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]/div[{i}]/div/div[1]/div[2]/div[4]/a').text)
        
        navegador.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[4]/a').click()
        time.sleep(2)
        
        for i in range(1,11):
            campeao.append(navegador.find_element_by_xpath(f'//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[4]/div[{i}]/div/div[1]/div[2]/div[4]/a').text)
        
        elos.append(elo)
        dados.append(dado)
        win_rate.append(win)
        campeoes.append(campeao)

    pdls = []
    vitorias_derrotas = []
    taxa = []
    nomes = []

    for i in range(len(dados)):
        pdl = dados[i][:2]
        pdls.append(pdl)
        
        v_d = dados[i][6:]
        vitorias_derrotas.append(v_d)
        
        tx = win_rate[i][8:]
        taxa.append(tx)
        
        nm = pessoas[i].replace("+", " ")
        nomes.append(nm)

    dataframe = pd.DataFrame()

    dataframe["Invocador"] = nomes
    dataframe["Elo"] = elos
    dataframe["PLDs"] = pdls
    dataframe["Partidas"] = vitorias_derrotas
    dataframe["WinRate"] = taxa
    dataframe["Campeões"] = campeoes

    dataframe = dataframe.sort_values("WinRate", ascending=False)
    dataframe = dataframe.reset_index(drop=True)

    dataframe.to_json(f"{nomes[0]}.json")

    dick = dataframe.to_dict()

    return jsonify(dick)