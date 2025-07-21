"""
Módulo para gerenciar datas especiais e eventos.
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class SpecialDates:
    """Classe para gerenciar datas especiais e eventos."""
    
    def __init__(self):
        """Inicializa a classe com as configurações de datas especiais."""
        self.dates = self._load_dates()
    
    def _load_dates(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Carrega todas as datas especiais.
        
        Returns:
            Dicionário com as datas especiais por tipo
        """
        return {
            'black_friday': [
    ('2013-11-29', 'Black Friday'),
    ('2014-11-28', 'Black Friday'),
    ('2015-11-27', 'Black Friday'),
    ('2016-11-25', 'Black Friday'),
    ('2017-11-24', 'Black Friday'),
    ('2018-11-23', 'Black Friday'),
    ('2019-11-29', 'Black Friday'),
    ('2020-11-27', 'Black Friday'),
    ('2021-11-26', 'Black Friday'),
    ('2022-11-25', 'Black Friday'),
    ('2023-11-24', 'Black Friday'),
    ('2024-11-29', 'Black Friday'),
    ('2025-11-28', 'Black Friday'),
    ('2026-11-28', 'Black Friday')
],

        'carnaval': [
    ('2013-02-11', 'Carnaval'),
    ('2014-03-03', 'Carnaval'),
    ('2015-02-16', 'Carnaval'),
    ('2016-02-08', 'Carnaval'),
    ('2017-02-27', 'Carnaval'),
    ('2018-02-12', 'Carnaval'),
    ('2019-03-04', 'Carnaval'),
    ('2020-02-24', 'Carnaval'),
    ('2021-02-15', 'Carnaval'),
    ('2022-02-28', 'Carnaval'),
    ('2023-02-20', 'Carnaval'),
    ('2024-02-12', 'Carnaval'),
    ('2025-03-04', 'Carnaval'),
    ('2026-02-17', 'Carnaval')
],

        'confraternizacao_universal': [
    ('2013-01-01', 'Confraternização Universal'),
    ('2014-01-01', 'Confraternização Universal'),
    ('2015-01-01', 'Confraternização Universal'),
    ('2016-01-01', 'Confraternização Universal'),
    ('2017-01-01', 'Confraternização Universal'),
    ('2018-01-01', 'Confraternização Universal'),
    ('2019-01-01', 'Confraternização Universal'),
    ('2020-01-01', 'Confraternização Universal'),
    ('2021-01-01', 'Confraternização Universal'),
    ('2022-01-01', 'Confraternização Universal'),
    ('2023-01-01', 'Confraternização Universal'),
    ('2024-01-01', 'Confraternização Universal'),
    ('2025-01-01', 'Confraternização Universal'),
    ('2026-01-01', 'Confraternização Universal')
],

        'copa_do_mundo': [
    ('2014-06-12', 'Copa do Mundo'),
    ('2014-06-17', 'Copa do Mundo'),
    ('2014-06-23', 'Copa do Mundo'),
    ('2014-06-28', 'Copa do Mundo'),
    ('2014-07-04', 'Copa do Mundo'),
    ('2014-07-08', 'Copa do Mundo'),
    ('2014-07-12', 'Copa do Mundo'),
    ('2018-06-14', 'Copa do Mundo'),
    ('2018-06-17', 'Copa do Mundo'),
    ('2018-06-22', 'Copa do Mundo'),
    ('2018-07-02', 'Copa do Mundo'),
    ('2018-07-06', 'Copa do Mundo'),
    ('2022-11-20', 'Copa do Mundo'),
    ('2022-11-24', 'Copa do Mundo'),
    ('2022-11-28', 'Copa do Mundo'),
    ('2022-12-02', 'Copa do Mundo'),
    ('2022-12-05', 'Copa do Mundo'),
    ('2022-12-09', 'Copa do Mundo'),
    ('2026-07-11', 'Copa do Mundo')
],       

        'covid':[
        ('2020-03-01', 'Covid') 
],

            


            
            'liquidacoes': [
                ('2020-01-06', 'Liquidação de Verão'),
                ('2020-07-06', 'Liquidação de Inverno'),
                ('2021-01-04', 'Liquidação de Verão'),
                ('2021-07-05', 'Liquidação de Inverno'),
                ('2022-01-03', 'Liquidação de Verão'),
                ('2022-07-04', 'Liquidação de Inverno'),
                ('2023-01-02', 'Liquidação de Verão'),
                ('2023-07-03', 'Liquidação de Inverno'),
                ('2024-01-02', 'Liquidação de Verão'),
                ('2024-07-01', 'Liquidação de Inverno')
            ]
        }
    
    def get_all_dates(self) -> pd.DataFrame:
        """
        Retorna todas as datas especiais em um DataFrame.
        
        Returns:
            DataFrame com todas as datas especiais
        """
        dates_list = []
        
        for tipo, datas in self.dates.items():
            for data, evento in datas:
                dates_list.append({
                    'data': pd.to_datetime(data),
                    'tipo': tipo,
                    'evento': evento
                })
        
        df = pd.DataFrame(dates_list)
        df = df.sort_values('data')
        return df
    
    def get_dates_by_type(self, tipo: str) -> pd.DataFrame:
        """
        Retorna as datas especiais de um tipo específico.
        
        Args:
            tipo: Tipo de data especial (feriados, black_friday, etc.)
            
        Returns:
            DataFrame com as datas especiais do tipo especificado
        """
        if tipo not in self.dates:
            raise ValueError(f"Tipo '{tipo}' não encontrado")
        
        dates_list = []
        for data, evento in self.dates[tipo]:
            dates_list.append({
                'data': pd.to_datetime(data),
                'tipo': tipo,
                'evento': evento
            })
        
        return pd.DataFrame(dates_list)
    
    def is_special_date(self, date: str) -> bool:
        """
        Verifica se uma data é especial.
        
        Args:
            date: Data a ser verificada (formato: YYYY-MM-DD)
            
        Returns:
            True se a data for especial, False caso contrário
        """
        date = pd.to_datetime(date)
        all_dates = self.get_all_dates()
        return date in all_dates['data'].values
    
    def get_special_date_info(self, date: str) -> Dict[str, str]:
        """
        Retorna informações sobre uma data especial.
        
        Args:
            date: Data a ser verificada (formato: YYYY-MM-DD)
            
        Returns:
            Dicionário com informações da data especial
        """
        date = pd.to_datetime(date)
        all_dates = self.get_all_dates()
        info = all_dates[all_dates['data'] == date]
        
        if len(info) == 0:
            return None
        
        return {
            'data': info['data'].iloc[0].strftime('%Y-%m-%d'),
            'tipo': info['tipo'].iloc[0],
            'evento': info['evento'].iloc[0]
        } 

def marcar_evento_range(df, nome_coluna, datas_evento, days_before=0, days_after=0):
    """
    Marca 1 na coluna nome_coluna para datas dentro do range de cada data de evento.
    """
    df[nome_coluna] = 0
    for data_evento in pd.to_datetime(datas_evento):
        start_range = data_evento - pd.Timedelta(days=days_before)
        end_range = data_evento + pd.Timedelta(days=days_after)
        df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), nome_coluna] = 1
    return df 