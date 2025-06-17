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
            'feriados': [
                ('2020-01-01', 'Ano Novo'),
                ('2020-04-10', 'Sexta-feira Santa'),
                ('2020-04-12', 'Páscoa'),
                ('2020-04-21', 'Tiradentes'),
                ('2020-05-01', 'Dia do Trabalho'),
                ('2020-06-11', 'Corpus Christi'),
                ('2020-09-07', 'Independência do Brasil'),
                ('2020-10-12', 'Nossa Senhora Aparecida'),
                ('2020-11-02', 'Finados'),
                ('2020-11-15', 'Proclamação da República'),
                ('2020-12-25', 'Natal'),
                ('2021-01-01', 'Ano Novo'),
                ('2021-04-02', 'Sexta-feira Santa'),
                ('2021-04-04', 'Páscoa'),
                ('2021-04-21', 'Tiradentes'),
                ('2021-05-01', 'Dia do Trabalho'),
                ('2021-06-03', 'Corpus Christi'),
                ('2021-09-07', 'Independência do Brasil'),
                ('2021-10-12', 'Nossa Senhora Aparecida'),
                ('2021-11-02', 'Finados'),
                ('2021-11-15', 'Proclamação da República'),
                ('2021-12-25', 'Natal'),
                ('2022-01-01', 'Ano Novo'),
                ('2022-04-15', 'Sexta-feira Santa'),
                ('2022-04-17', 'Páscoa'),
                ('2022-04-21', 'Tiradentes'),
                ('2022-05-01', 'Dia do Trabalho'),
                ('2022-06-16', 'Corpus Christi'),
                ('2022-09-07', 'Independência do Brasil'),
                ('2022-10-12', 'Nossa Senhora Aparecida'),
                ('2022-11-02', 'Finados'),
                ('2022-11-15', 'Proclamação da República'),
                ('2022-12-25', 'Natal'),
                ('2023-01-01', 'Ano Novo'),
                ('2023-04-07', 'Sexta-feira Santa'),
                ('2023-04-09', 'Páscoa'),
                ('2023-04-21', 'Tiradentes'),
                ('2023-05-01', 'Dia do Trabalho'),
                ('2023-06-08', 'Corpus Christi'),
                ('2023-09-07', 'Independência do Brasil'),
                ('2023-10-12', 'Nossa Senhora Aparecida'),
                ('2023-11-02', 'Finados'),
                ('2023-11-15', 'Proclamação da República'),
                ('2023-12-25', 'Natal'),
                ('2024-01-01', 'Ano Novo'),
                ('2024-03-29', 'Sexta-feira Santa'),
                ('2024-03-31', 'Páscoa'),
                ('2024-04-21', 'Tiradentes'),
                ('2024-05-01', 'Dia do Trabalho'),
                ('2024-05-30', 'Corpus Christi'),
                ('2024-09-07', 'Independência do Brasil'),
                ('2024-10-12', 'Nossa Senhora Aparecida'),
                ('2024-11-02', 'Finados'),
                ('2024-11-15', 'Proclamação da República'),
                ('2024-12-25', 'Natal')
            ],
            'black_friday': [
                ('2020-11-27', 'Black Friday'),
                ('2021-11-26', 'Black Friday'),
                ('2022-11-25', 'Black Friday'),
                ('2023-11-24', 'Black Friday'),
                ('2024-11-29', 'Black Friday')
            ],
            'cyber_monday': [
                ('2020-11-30', 'Cyber Monday'),
                ('2021-11-29', 'Cyber Monday'),
                ('2022-11-28', 'Cyber Monday'),
                ('2023-11-27', 'Cyber Monday'),
                ('2024-12-02', 'Cyber Monday')
            ],
            'dia_maes': [
                ('2020-05-10', 'Dia das Mães'),
                ('2021-05-09', 'Dia das Mães'),
                ('2022-05-08', 'Dia das Mães'),
                ('2023-05-14', 'Dia das Mães'),
                ('2024-05-12', 'Dia das Mães')
            ],
            'dia_pais': [
                ('2020-08-09', 'Dia dos Pais'),
                ('2021-08-08', 'Dia dos Pais'),
                ('2022-08-14', 'Dia dos Pais'),
                ('2023-08-13', 'Dia dos Pais'),
                ('2024-08-11', 'Dia dos Pais')
            ],
            'dia_criancas': [
                ('2020-10-12', 'Dia das Crianças'),
                ('2021-10-12', 'Dia das Crianças'),
                ('2022-10-12', 'Dia das Crianças'),
                ('2023-10-12', 'Dia das Crianças'),
                ('2024-10-12', 'Dia das Crianças')
            ],
            'dia_namorados': [
                ('2020-06-12', 'Dia dos Namorados'),
                ('2021-06-12', 'Dia dos Namorados'),
                ('2022-06-12', 'Dia dos Namorados'),
                ('2023-06-12', 'Dia dos Namorados'),
                ('2024-06-12', 'Dia dos Namorados')
            ],
            'carnaval': [
                ('2020-02-25', 'Carnaval'),
                ('2021-02-16', 'Carnaval'),
                ('2022-03-01', 'Carnaval'),
                ('2023-02-21', 'Carnaval'),
                ('2024-02-13', 'Carnaval')
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