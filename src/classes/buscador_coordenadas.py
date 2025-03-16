# buscador_coordenadas.py
import pandas as pd
import requests
import time
from datetime import datetime
from typing import List, Optional
from .coordenada_municipio import CoordenadaMunicipio

class BuscadorCoordenadas:
    def __init__(self, user_agent: str = "mg-municipios/1.0 (+https://seu-site.com)"):
        self.user_agent = user_agent
        self.delay = 2  # segundos entre requisições
        self.last_request = datetime.now()
        self.coordenadas: List[CoordenadaMunicipio] = []
        
    def _wait_if_necessary(self):
        now = datetime.now()
        time_diff = (now - self.last_request).total_seconds()
        
        if time_diff < self.delay:
            time.sleep(self.delay - time_diff)
        self.last_request = now
    
    def buscar_coordenada(self, municipio: str) -> Optional[CoordenadaMunicipio]:
        self._wait_if_necessary()
        
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': f"{municipio}, Minas Gerais, Brasil",
            'format': 'json',
            'limit': 1,
            'extratags': True
        }
        headers = {'User-Agent': self.user_agent}
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 403:
                print(f"Erro 403 para {municipio}. Aguardando 30 segundos...")
                time.sleep(30)
                return self.buscar_coordenada(municipio)
                
            response.raise_for_status()
            dados = response.json()
            
            if dados:
                return CoordenadaMunicipio(
                    municipio=municipio,
                    latitude=float(dados[0]['lat']),
                    longitude=float(dados[0]['lon'])
                )
                
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar {municipio}: {str(e)}")
            
        return None

    def processar_cidades(self, df: pd.DataFrame) -> List[CoordenadaMunicipio]:
        print("Iniciando busca de coordenadas...")
        cidades = df['municipio'].unique()
        total = len(cidades)
        
        for i, cidade in enumerate(cidades, 1):
            if i % 10 == 0:
                print(f"Processando cidade {i} de {total}")
                
            coordenada = self.buscar_coordenada(cidade)
            if coordenada:
                self.coordenadas.append(coordenada)
                
        return self.coordenadas