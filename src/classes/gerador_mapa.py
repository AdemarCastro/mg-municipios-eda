# gerador_mapa.py
import folium
from folium.plugins import HeatMap
import branca.colormap as cm
import pandas as pd
from .coordenada_municipio import CoordenadaMunicipio
from typing import List

class GeradorMapa:
    def __init__(self, dados: List[CoordenadaMunicipio]):
        self.dados = dados
        
    def criar_mapa(self, df: pd.DataFrame) -> folium.Map:
        mapa = folium.Map(location=[-18.9227, -47.9189], zoom_start=7)
        
        dados_heatmap = [
            [coord.latitude, coord.longitude, coord.escolarizacao]
            for coord in self.dados
            if coord.escolarizacao is not None
        ]
        
        HeatMap(dados_heatmap, radius=15).add_to(mapa)

        for idx, row in df.iterrows():
            tooltip_text = f"{row['municipio']}: {row['escolarizacao']}%"
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                tooltip=tooltip_text,
                icon=folium.DivIcon(html='<div style="width:20px; height:20px; opacity:0;"></div>')
            ).add_to(mapa)
        
        min_val = min(coord.escolarizacao for coord in self.dados if coord.escolarizacao is not None)
        max_val = max(coord.escolarizacao for coord in self.dados if coord.escolarizacao is not None)

        colormap = cm.linear.YlOrRd_09.scale(min_val, max_val)
        colormap.caption = 'Taxa de Escolarização'
        colormap.add_to(mapa)
        
        return mapa