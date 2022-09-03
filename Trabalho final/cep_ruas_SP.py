from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import numpy as np
import pandas as pd
from pandas import DataFrame
import chromedriver_binary


class BotCep:
    def __init__(self):
        self.bot = webdriver.Chrome()
        self.dados = np.array(pd.read_csv('Sao paulo - Sheet1.csv'))
        self.ruas = self.dados[:, 0]
        self.ceps = []

    def faz_consulta(self):
        ceps = self.ceps
        ruas = self.ruas
        bot = self.bot
        for rua in ruas:
            bot.get('https://buscacepinter.correios.com.br/app/endereco/index.php')
            bot.find_element(By.XPATH, '//*[@id="tipoCEP"]').click()
            bot.find_element(By.XPATH,
                             "//*[@id='tipoCEP']/optgroup/option[contains(.,'Localidade/Logradouro')]").click()
            rua_tratada = ''.join([i for i in rua if not i.isdigit()])
            nome_rua = rua_tratada.replace(', São Paulo', '').replace(',', '').strip()
            sp = ', São Paulo'
            if sp not in rua_tratada:
                rua_tratada = rua_tratada + sp
            bot.find_element(By.XPATH, '//*[@id="endereco"]').send_keys(rua_tratada)
            bot.find_element(By.XPATH, '//*[@id="btn_pesquisar"]').click()
            sleep(1)
            resultado = bot.find_element(By.XPATH, '//*[@id="mensagem-resultado"]').text
            if resultado == 'Não há dados a serem exibidos':
                ceps.append(00000 - 000)
                print(f'Não foi possível localizar a rua {rua}')
            else:
                cep = 0
                nao_encontrou = True
                while nao_encontrou:
                    try:
                        try:  # Caso o endereco seja de fato uma rua, sera atribuido o cep da rua
                            cep = bot.find_element(By.XPATH,
                                                   f'//*[@id="resultado-DNEC"]/tbody/tr[contains(td[1], "{nome_rua}") and contains(td[3], "São Paulo")]/td[4]').text
                            nao_encontrou = False
                        except:  # Caso contrario, sera um bairro, e assim, o cep atribuido sera da primeira rua do bairro que o bot encontrar
                            cep = bot.find_element(By.XPATH,
                                                   f'//*[@id="resultado-DNEC"]/tbody/tr[contains(td[2], "{nome_rua}") and contains(td[3], "São Paulo")]/td[4]').text
                            nao_encontrou = False
                    except:
                        try:
                            bot.find_element(By.XPATH, '//*[@id="navegacao-resultado"]/a[2]').click()
                        except:
                            cep = 00000 - 000
                            nao_encontrou = False
                            print(f'A rua {rua} não está localizada em SP')
                ceps.append(cep)
        self.ceps = ceps

    def cria_csv(self):
        cep = self.ceps
        rua = self.dados[:, 0]
        area_m2 = self.dados[:, 2]
        quartos = self.dados[:, 3]
        banheiros = self.dados[:, 4]
        vagas = self.dados[:, 5]
        preco = self.dados[:, 6]
        arquivo = {'RUA': rua, 'CEP': cep, 'AREA': area_m2, 'QUARTOS': quartos, 'BANHEIROS': banheiros, 'VAGAS': vagas, 'PRECO': preco}
        arquivo = DataFrame(arquivo)
        arquivo.to_csv('Casas_SP_Final.csv', index=False)


if __name__ == '__main__':
    bot = BotCep()
    bot.faz_consulta()
    bot.cria_csv()
