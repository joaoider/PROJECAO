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

        'dia_do_trabalhador': [
    ('2013-05-01', 'Dia do Trabalhador'),
    ('2014-05-01', 'Dia do Trabalhador'),
    ('2015-05-01', 'Dia do Trabalhador'),
    ('2016-05-01', 'Dia do Trabalhador'),
    ('2017-05-01', 'Dia do Trabalhador'),
    ('2018-05-01', 'Dia do Trabalhador'),
    ('2019-05-01', 'Dia do Trabalhador'),
    ('2020-05-01', 'Dia do Trabalhador'),
    ('2021-05-01', 'Dia do Trabalhador'),
    ('2022-05-01', 'Dia do Trabalhador'),
    ('2023-05-01', 'Dia do Trabalhador'),
    ('2024-05-01', 'Dia do Trabalhador'),
    ('2025-05-01', 'Dia do Trabalhador'),
    ('2026-05-01', 'Dia do Trabalhador')
],

        'eleicoes': [
    ('2018-10-07', 'Eleições'),
    ('2018-10-28', 'Eleições'),
    ('2022-10-02', 'Eleições'),
    ('2022-10-30', 'Eleições'),
    ('2024-10-06', 'Eleições'),
    ('2024-10-27', 'Eleições'),
    ('2026-10-04', 'Eleições'),
    ('2026-10-25', 'Eleições')
],

        'halloween': [
    ('2013-10-31', 'Halloween'),
    ('2014-10-31', 'Halloween'),
    ('2015-10-31', 'Halloween'),
    ('2016-10-31', 'Halloween'),
    ('2017-10-31', 'Halloween'),
    ('2018-10-31', 'Halloween'),
    ('2019-10-31', 'Halloween'),
    ('2020-10-31', 'Halloween'),
    ('2021-10-31', 'Halloween'),
    ('2022-10-31', 'Halloween'),
    ('2023-10-31', 'Halloween'),
    ('2024-10-31', 'Halloween'),
    ('2025-10-31', 'Halloween'),
    ('2026-10-31', 'Halloween')
],

        'independencia_do_brasil': [
    ('2013-09-07', 'Independência do Brasil'),
    ('2014-09-07', 'Independência do Brasil'),
    ('2015-09-07', 'Independência do Brasil'),
    ('2016-09-07', 'Independência do Brasil'),
    ('2017-09-07', 'Independência do Brasil'),
    ('2018-09-07', 'Independência do Brasil'),
    ('2019-09-07', 'Independência do Brasil'),
    ('2020-09-07', 'Independência do Brasil'),
    ('2021-09-07', 'Independência do Brasil'),
    ('2022-09-07', 'Independência do Brasil'),
    ('2023-09-07', 'Independência do Brasil'),
    ('2024-09-07', 'Independência do Brasil'),
    ('2025-09-07', 'Independência do Brasil'),
    ('2026-09-07', 'Independência do Brasil')
],

        'natal': [
    ('2013-12-25', 'Natal'),
    ('2014-12-25', 'Natal'),
    ('2015-12-25', 'Natal'),
    ('2016-12-25', 'Natal'),
    ('2017-12-25', 'Natal'),
    ('2018-12-25', 'Natal'),
    ('2019-12-25', 'Natal'),
    ('2020-12-25', 'Natal'),
    ('2021-12-25', 'Natal'),
    ('2022-12-25', 'Natal'),
    ('2023-12-25', 'Natal'),
    ('2024-12-25', 'Natal'),
    ('2025-12-25', 'Natal'),
    ('2026-12-25', 'Natal')
],

        'nossa_senhora_aparecida': [
    ('2013-10-12', 'Nossa Senhora Aparecida'),
    ('2014-10-12', 'Nossa Senhora Aparecida'),
    ('2015-10-12', 'Nossa Senhora Aparecida'),
    ('2016-10-12', 'Nossa Senhora Aparecida'),
    ('2017-10-12', 'Nossa Senhora Aparecida'),
    ('2018-10-12', 'Nossa Senhora Aparecida'),
    ('2019-10-12', 'Nossa Senhora Aparecida'),
    ('2020-10-12', 'Nossa Senhora Aparecida'),
    ('2021-10-12', 'Nossa Senhora Aparecida'),
    ('2022-10-12', 'Nossa Senhora Aparecida'),
    ('2023-10-12', 'Nossa Senhora Aparecida'),
    ('2024-10-12', 'Nossa Senhora Aparecida'),
    ('2025-10-12', 'Nossa Senhora Aparecida'),
    ('2026-10-12', 'Nossa Senhora Aparecida')
],

        'pascoa': [
    ('2013-03-31', 'Páscoa'),
    ('2014-04-20', 'Páscoa'),
    ('2015-04-05', 'Páscoa'),
    ('2016-03-27', 'Páscoa'),
    ('2017-04-16', 'Páscoa'),
    ('2018-04-01', 'Páscoa'),
    ('2019-04-21', 'Páscoa'),
    ('2020-04-12', 'Páscoa'),
    ('2021-04-04', 'Páscoa'),
    ('2022-04-17', 'Páscoa'),
    ('2023-04-09', 'Páscoa'),
    ('2024-03-31', 'Páscoa'),
    ('2025-04-20', 'Páscoa'),
    ('2026-04-05', 'Páscoa')
],

        'proclamacao_da_republica': [
    ('2013-11-15', 'Proclamação da República'),
    ('2014-11-15', 'Proclamação da República'),
    ('2015-11-15', 'Proclamação da República'),
    ('2016-11-15', 'Proclamação da República'),
    ('2017-11-15', 'Proclamação da República'),
    ('2018-11-15', 'Proclamação da República'),
    ('2019-11-15', 'Proclamação da República'),
    ('2020-11-15', 'Proclamação da República'),
    ('2021-11-15', 'Proclamação da República'),
    ('2022-11-15', 'Proclamação da República'),
    ('2023-11-15', 'Proclamação da República'),
    ('2024-11-15', 'Proclamação da República'),
    ('2025-11-15', 'Proclamação da República'),
    ('2026-11-15', 'Proclamação da República')
],

        'sexta_feira_santa': [
    ('2013-03-29', 'Sexta-Feira Santa'),
    ('2014-04-18', 'Sexta-Feira Santa'),
    ('2015-04-03', 'Sexta-Feira Santa'),
    ('2016-03-25', 'Sexta-Feira Santa'),
    ('2017-04-14', 'Sexta-Feira Santa'),
    ('2018-03-30', 'Sexta-Feira Santa'),
    ('2019-04-19', 'Sexta-Feira Santa'),
    ('2020-04-10', 'Sexta-Feira Santa'),
    ('2021-04-02', 'Sexta-Feira Santa'),
    ('2022-04-15', 'Sexta-Feira Santa'),
    ('2023-04-07', 'Sexta-Feira Santa'),
    ('2024-03-29', 'Sexta-Feira Santa'),
    ('2025-04-18', 'Sexta-Feira Santa'),
    ('2026-04-03', 'Sexta-Feira Santa')
],

        'dia_das_maes': [
    ('2013-05-12', 'Dia das Mães'),
    ('2014-05-11', 'Dia das Mães'),
    ('2015-05-10', 'Dia das Mães'),
    ('2016-05-09', 'Dia das Mães'),
    ('2017-05-08', 'Dia das Mães'),
    ('2018-05-07', 'Dia das Mães'),
    ('2019-05-06', 'Dia das Mães'),
    ('2020-05-05', 'Dia das Mães'),
    ('2021-05-04', 'Dia das Mães'),
    ('2022-05-03', 'Dia das Mães'),
    ('2023-05-02', 'Dia das Mães'),
    ('2024-05-01', 'Dia das Mães'),
    ('2025-04-30', 'Dia das Mães'),
    ('2026-04-29', 'Dia das Mães')
],

        'dia_de_finados': [
    ('2013-11-02', 'Dia de Finados'),
    ('2014-11-01', 'Dia de Finados'),
    ('2015-10-31', 'Dia de Finados'),
    ('2016-10-31', 'Dia de Finados'),
    ('2017-10-31', 'Dia de Finados'),
    ('2018-10-31', 'Dia de Finados'),
    ('2019-10-31', 'Dia de Finados'),
    ('2020-10-31', 'Dia de Finados'),
    ('2021-10-31', 'Dia de Finados'),
    ('2022-10-31', 'Dia de Finados'),
    ('2023-10-31', 'Dia de Finados'),
    ('2024-10-31', 'Dia de Finados'),
    ('2025-10-31', 'Dia de Finados'),
    ('2026-10-31', 'Dia de Finados')
],

        'dia_dos_namorados': [
    ('2013-07-07', 'Dia dos Namorados'),
    ('2014-07-07', 'Dia dos Namorados'),
    ('2015-07-07', 'Dia dos Namorados'),
    ('2016-07-07', 'Dia dos Namorados'),
    ('2017-07-07', 'Dia dos Namorados'),
    ('2018-07-07', 'Dia dos Namorados'),
    ('2019-07-07', 'Dia dos Namorados'),
    ('2020-07-07', 'Dia dos Namorados'),
    ('2021-07-07', 'Dia dos Namorados'),
    ('2022-07-07', 'Dia dos Namorados'),
    ('2023-07-07', 'Dia dos Namorados'),
    ('2024-07-07', 'Dia dos Namorados'),
    ('2025-07-07', 'Dia dos Namorados'),
    ('2026-07-07', 'Dia dos Namorados')
],

        'dia_dos_pais': [
    ('2013-08-12', 'Dia dos Pais'),
    ('2014-08-12', 'Dia dos Pais'),
    ('2015-08-12', 'Dia dos Pais'),
    ('2016-08-12', 'Dia dos Pais'),
    ('2017-08-12', 'Dia dos Pais'),
    ('2018-08-12', 'Dia dos Pais'),
    ('2019-08-12', 'Dia dos Pais'),
    ('2020-08-12', 'Dia dos Pais'),
    ('2021-08-12', 'Dia dos Pais'),
    ('2022-08-12', 'Dia dos Pais'),
    ('2023-08-12', 'Dia dos Pais'),
    ('2024-08-12', 'Dia dos Pais'),
    ('2025-08-12', 'Dia dos Pais'),
    ('2026-08-12', 'Dia dos Pais')
],

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
    
    def get_dates_for_event(self, event_name: str) -> List[str]:
        """
        Retorna a lista de datas para um evento específico.
        
        Args:
            event_name: Nome do evento (ex: 'black_friday', 'carnaval', etc.)
            
        Returns:
            Lista de datas no formato YYYY-MM-DD
        """
        if event_name not in self.dates:
            return []
        
        return [date for date, _ in self.dates[event_name]]
    
    def get_black_friday_dates(self) -> List[str]:
        """Retorna as datas do Black Friday."""
        return self.get_dates_for_event('black_friday')
    
    def get_carnaval_dates(self) -> List[str]:
        """Retorna as datas do Carnaval."""
        return self.get_dates_for_event('carnaval')
    
    def get_confraternizacao_universal_dates(self) -> List[str]:
        """Retorna as datas da Confraternização Universal."""
        return self.get_dates_for_event('confraternizacao_universal')
    
    def get_copa_do_mundo_dates(self) -> List[str]:
        """Retorna as datas da Copa do Mundo."""
        return self.get_dates_for_event('copa_do_mundo')
    
    def get_covid_dates(self) -> List[str]:
        """Retorna as datas do COVID."""
        return self.get_dates_for_event('covid')
    
    def get_dia_do_trabalhador_dates(self) -> List[str]:
        """Retorna as datas do Dia do Trabalhador."""
        return self.get_dates_for_event('dia_do_trabalhador')
    
    def get_eleicoes_dates(self) -> List[str]:
        """Retorna as datas das Eleições."""
        return self.get_dates_for_event('eleicoes')
    
    def get_halloween_dates(self) -> List[str]:
        """Retorna as datas do Halloween."""
        return self.get_dates_for_event('halloween')
    
    def get_independencia_do_brasil_dates(self) -> List[str]:
        """Retorna as datas da Independência do Brasil."""
        return self.get_dates_for_event('independencia_do_brasil')
    
    def get_natal_dates(self) -> List[str]:
        """Retorna as datas do Natal."""
        return self.get_dates_for_event('natal')
    
    def get_nossa_senhora_aparecida_dates(self) -> List[str]:
        """Retorna as datas de Nossa Senhora Aparecida."""
        return self.get_dates_for_event('nossa_senhora_aparecida')
    
    def get_pascoa_dates(self) -> List[str]:
        """Retorna as datas da Páscoa."""
        return self.get_dates_for_event('pascoa')
    
    def get_proclamacao_da_republica_dates(self) -> List[str]:
        """Retorna as datas da Proclamação da República."""
        return self.get_dates_for_event('proclamacao_da_republica')
    
    def get_sexta_feira_santa_dates(self) -> List[str]:
        """Retorna as datas da Sexta-Feira Santa."""
        return self.get_dates_for_event('sexta_feira_santa')
    
    def get_dia_das_maes_dates(self) -> List[str]:
        """Retorna as datas do Dia das Mães."""
        return self.get_dates_for_event('dia_das_maes')
    
    def get_dia_de_finados_dates(self) -> List[str]:
        """Retorna as datas do Dia de Finados."""
        return self.get_dates_for_event('dia_de_finados')
    
    def get_dia_dos_namorados_dates(self) -> List[str]:
        """Retorna as datas do Dia dos Namorados."""
        return self.get_dates_for_event('dia_dos_namorados')
    
    def get_dia_dos_pais_dates(self) -> List[str]:
        """Retorna as datas do Dia dos Pais."""
        return self.get_dates_for_event('dia_dos_pais')

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

def process_dia_do_trabalhador(df):
    """
    Processa o DataFrame para adicionar a coluna dia_do_trabalhador.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'dia_do_trabalhador' adicionada
    """
    dia_do_trabalhador = df.copy()
    
    # Inicializa a coluna dia_do_trabalhador com 0
    dia_do_trabalhador['dia_do_trabalhador'] = 0

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para o Dia do Trabalhador conforme fornecido
    specific_dates_dia_do_trabalhador = [
        '2013-05-01', '2014-05-01', '2015-05-01', '2016-05-01', '2017-05-01',
        '2018-05-01', '2019-05-01', '2020-05-01', '2021-05-01', '2022-05-01',
        '2023-05-01', '2024-05-01', '2025-05-01', '2026-05-01'
    ]
    specific_dates_dia_do_trabalhador = pd.to_datetime(specific_dates_dia_do_trabalhador)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'dia_do_trabalhador'] = 1

    # Aplicar a função ao DataFrame
    set_values(dia_do_trabalhador, specific_dates_dia_do_trabalhador, days_before, days_after)

    return dia_do_trabalhador

def process_eleicoes(df):
    """
    Processa o DataFrame para adicionar a coluna eleicoes.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'eleicoes' adicionada
    """
    eleicoes = df.copy()
    
    # Inicializa a coluna eleicoes com 0
    eleicoes['eleicoes'] = 0

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para as Eleições conforme fornecido
    specific_dates_eleicoes = [
        '2018-10-07', '2018-10-28', '2022-10-02', '2022-10-30', '2024-10-06', '2024-10-27', '2026-10-04', '2026-10-25'
    ]
    specific_dates_eleicoes = pd.to_datetime(specific_dates_eleicoes)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'eleicoes'] = 1

    # Aplicar a função ao DataFrame
    set_values(eleicoes, specific_dates_eleicoes, days_before, days_after)

    return eleicoes

def process_halloween(df):
    """
    Processa o DataFrame para adicionar a coluna halloween.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'halloween' adicionada
    """
    halloween = df.copy()
    
    # Inicializa a coluna halloween com 0
    halloween['halloween'] = 0

    # Definir o range de dias antes e depois
    days_before = 1
    days_after = 1

    # Lista de datas específicas para o Halloween, desde 2013 até 2025
    specific_dates_halloween = [
        '2013-10-31', '2014-10-31', '2015-10-31', '2016-10-31', '2017-10-31',
        '2018-10-31', '2019-10-31', '2020-10-31', '2021-10-31', '2022-10-31',
        '2023-10-31', '2024-10-31', '2025-10-31', '2026-10-31'
    ]
    specific_dates_halloween = pd.to_datetime(specific_dates_halloween)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'halloween'] = 1

    # Aplicar a função ao DataFrame
    set_values(halloween, specific_dates_halloween, days_before, days_after)

    return halloween

def process_independencia_do_brasil(df):
    """
    Processa o DataFrame para adicionar a coluna independencia_do_brasil.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'independencia_do_brasil' adicionada
    """
    independencia_do_brasil = df.copy()
    
    # Inicializa a coluna independencia_do_brasil com 0
    independencia_do_brasil['independencia_do_brasil'] = 0

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Independência do Brasil conforme fornecido
    specific_dates_independencia_do_brasil = [
        '2013-09-07', '2014-09-07', '2015-09-07', '2016-09-07', '2017-09-07',
        '2018-09-07', '2019-09-07', '2020-09-07', '2021-09-07', '2022-09-07',
        '2023-09-07', '2024-09-07', '2025-09-07', '2026-09-07'
    ]
    specific_dates_independencia_do_brasil = pd.to_datetime(specific_dates_independencia_do_brasil)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'independencia_do_brasil'] = 1

    # Aplicar a função ao DataFrame
    set_values(independencia_do_brasil, specific_dates_independencia_do_brasil, days_before, days_after)

    return independencia_do_brasil

def process_mes_do_ano(df):
    """
    Processa o DataFrame para adicionar a coluna monthofyear.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'monthofyear' adicionada
    """
    mesdoano = df.copy()
    mesdoano['value'] = mesdoano['ds'].dt.month_name()
    mesdoano.rename(columns={'value': 'mes_do_ano'}, inplace=True)

    # Mapeamento dos meses para números
    month_mapping = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    # Criar a nova coluna 'monthofyear' utilizando o mapeamento
    mesdoano['monthofyear'] = mesdoano['mes_do_ano'].map(month_mapping)

    # Remover a coluna 'mes_do_ano'
    mesdoano = mesdoano.drop(columns=['mes_do_ano'])

    return mesdoano 

def process_natal(df):
    """
    Processa o DataFrame para adicionar a coluna natal.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'natal' adicionada
    """
    natal = df.copy()
    
    # Inicializa a coluna natal com 0
    natal['natal'] = 0

    # Definir o range de dias antes e depois
    days_before = 7
    days_after = 0

    # Lista de datas específicas para o Natal, desde 2013 até 2025
    specific_dates_natal = [
        '2013-12-25', '2014-12-25', '2015-12-25', '2016-12-25', '2017-12-25',
        '2018-12-25', '2019-12-25', '2020-12-25', '2021-12-25', '2022-12-25',
        '2023-12-25', '2024-12-25', '2025-12-25', '2026-12-25'
    ]
    specific_dates_natal = pd.to_datetime(specific_dates_natal)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'natal'] = 1

    # Aplicar a função ao DataFrame
    set_values(natal, specific_dates_natal, days_before, days_after)

    return natal 

def process_nossa_senhora_aparecida(df):
    """
    Processa o DataFrame para adicionar a coluna nossa_senhora_aparecida.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'nossa_senhora_aparecida' adicionada
    """
    nossa_senhora_aparecida = df.copy()
    
    # Inicializa a coluna nossa_senhora_aparecida com 0
    nossa_senhora_aparecida['nossa_senhora_aparecida'] = 0

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para Nossa Senhora Aparecida conforme fornecido
    specific_dates_nossa_senhora_aparecida = [
        '2013-10-12', '2014-10-12', '2015-10-12', '2016-10-12', '2017-10-12',
        '2018-10-12', '2019-10-12', '2020-10-12', '2021-10-12', '2022-10-12',
        '2023-10-12', '2024-10-12', '2025-10-12', '2026-10-12'
    ]
    specific_dates_nossa_senhora_aparecida = pd.to_datetime(specific_dates_nossa_senhora_aparecida)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'nossa_senhora_aparecida'] = 1

    # Aplicar a função ao DataFrame
    set_values(nossa_senhora_aparecida, specific_dates_nossa_senhora_aparecida, days_before, days_after)

    return nossa_senhora_aparecida 

def process_pascoa(df):
    """
    Processa o DataFrame para adicionar a coluna pascoa.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'pascoa' adicionada
    """
    pascoa = df.copy()
    
    # Inicializa a coluna pascoa com 0
    pascoa['pascoa'] = 0

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Páscoa conforme fornecido
    specific_dates_pascoa = [
        '2013-03-31', '2014-04-20', '2015-04-05', '2016-03-27', '2017-04-16',
        '2018-04-01', '2019-04-21', '2020-04-12', '2021-04-04', '2022-04-17',
        '2023-04-09', '2024-03-31', '2025-04-20', '2026-04-05'
    ]
    specific_dates_pascoa = pd.to_datetime(specific_dates_pascoa)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'pascoa'] = 1

    # Aplicar a função ao DataFrame
    set_values(pascoa, specific_dates_pascoa, days_before, days_after)

    return pascoa

def process_proclamacao_da_republica(df):
    """
    Processa o DataFrame para adicionar a coluna proclamacao_da_republica.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'proclamacao_da_republica' adicionada
    """
    proclamacao_da_republica = df.copy()
    
    # Inicializa a coluna proclamacao_da_republica com 0
    proclamacao_da_republica['proclamacao_da_republica'] = 0

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Proclamação da República conforme fornecido
    specific_dates_proclamacao_da_republica = [
        '2013-11-15', '2014-11-15', '2015-11-15', '2016-11-15', '2017-11-15',
        '2018-11-15', '2019-11-15', '2020-11-15', '2021-11-15', '2022-11-15',
        '2023-11-15', '2024-11-15', '2025-11-15', '2026-11-15'
    ]
    specific_dates_proclamacao_da_republica = pd.to_datetime(specific_dates_proclamacao_da_republica)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'proclamacao_da_republica'] = 1

    # Aplicar a função ao DataFrame
    set_values(proclamacao_da_republica, specific_dates_proclamacao_da_republica, days_before, days_after)

    return proclamacao_da_republica

def process_sexta_feira_santa(df):
    """
    Processa o DataFrame para adicionar a coluna sexta_feira_santa.
    
    Args:
        df: DataFrame com coluna 'ds' (datas)
        
    Returns:
        DataFrame com a coluna 'sexta_feira_santa' adicionada
    """
    sexta_feira_santa = df.copy()
    
    # Inicializa a coluna sexta_feira_santa com 0
    sexta_feira_santa['sexta_feira_santa'] = 0

    # Intervalo de dias antes e depois é 0 para ambos, conforme especificado
    days_before = 0
    days_after = 0

    # Lista de datas específicas para a Sexta-Feira Santa conforme fornecido
    specific_dates_sexta_feira_santa = [
        '2013-03-29', '2014-04-18', '2015-04-03', '2016-03-25', '2017-04-14',
        '2018-03-30', '2019-04-19', '2020-04-10', '2021-04-02', '2022-04-15',
        '2023-04-07', '2024-03-29', '2025-04-18', '2026-04-03'
    ]
    specific_dates_sexta_feira_santa = pd.to_datetime(specific_dates_sexta_feira_santa)

    # Função para definir os valores no intervalo de datas específicas
    def set_values(df, specific_dates, days_before, days_after):
        for specific_date in specific_dates:
            start_range = specific_date - pd.Timedelta(days=days_before)
            end_range = specific_date + pd.Timedelta(days=days_after)
            df.loc[(df['ds'] >= start_range) & (df['ds'] <= end_range), 'sexta_feira_santa'] = 1

    # Aplicar a função ao DataFrame
    set_values(sexta_feira_santa, specific_dates_sexta_feira_santa, days_before, days_after)

    return sexta_feira_santa 