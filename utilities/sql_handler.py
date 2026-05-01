from utilities.custom_types import FilePath

import sqlite3
from datetime import datetime
from typing import Literal, List, Tuple

class SQL():
    def __init__(self):
        # accessed by two dependent public method so left declaration here
        self.__settings_obj = None
        self.__settings_cursor = None
        
    def __alternative_func_extract(self, widget_tok: int, table_code: Literal[0, 1, 2]) -> int|None:
        db_obj = sqlite3.connect(FilePath('tokens.db'))
        db_cursor = db_obj.cursor()
        
        table = 'ShiftFunc' if table_code == 0 else 'AlphaFunc' if table_code == 1 else 'StoredVar'
        statement = f'SELECT token FROM {table} WHERE widget_token = {widget_tok};'
        db_cursor.execute(statement)
        token = db_cursor.fetchall()
        
        db_obj.close()
        
        # double index as output of fetchall is:
        # [(record1), (record2), (column1, column2, column3)]
        return token[0][0] if token != [] else None
    
    def find_shift_func(self, widget_tok: int) -> int | None:
        return self.__alternative_func_extract(widget_tok, 0)
    
    def find_alpha_func(self, widget_tok: int) -> int | None:
        return self.__alternative_func_extract(widget_tok, 1)
    
    def find_store_func(self, widget_tok: int) -> int | None:
        return self.__alternative_func_extract(widget_tok, 2)
    
    def __settings_db_prep(self) -> None:
        self.__settings_obj = sqlite3.connect(FilePath('settings_and_variables.db'))
        self.__settings_cursor = self.__settings_obj.cursor()
    
    def save_current_states(self, settings: Tuple[int], var: Tuple[float]) -> None:
        if self.__settings_obj == None:
            self.__settings_db_prep()
            
        now = datetime.now().timestamp()
        
        for table, values in {'Settings': settings, 'Variables': var}.items():
            values_str = [str(_) for _ in values]
            insert_statement = f'INSERT INTO {table} VALUES ({now}, {", ".join(values_str)});'
            
            latest_record = self.retrieve_current_states(table)
  
            if latest_record != values:
                self.__settings_cursor.execute(insert_statement)
                self.__settings_obj.commit()
    
    def retrieve_current_states(self, choice: Literal['Settings', 'Variables']) -> list[int] | list[float] | None:
        if self.__settings_obj == None:
            self.__settings_db_prep()
            
        statement = f'SELECT * FROM {choice} ORDER BY UNIX_timestamp DESC LIMIT 1;'

        self.__settings_cursor.execute(statement)
        record = self.__settings_cursor.fetchall()
        
        if record == []: return None
        if choice == 'Variables': return [float(_) for _ in record[0][1:]]
        else: return record[0][1:] 
    
    def get_txt_from_token(self, token: int) -> str:
        db_obj = sqlite3.connect(FilePath('token_to_text.db'))
        db_cursor = db_obj.cursor()
        
        db_cursor.execute(f'SELECT text FROM token_to_text WHERE token={token};')
        text = db_cursor.fetchall()[0][0]
        db_obj.close()
        return text

    def get_op_attribute(self) -> dict[int, list[int]]:
        statement = 'SELECT * FROM Operations;'

        db_obj = sqlite3.connect(FilePath('op_expr_eva_attribute.db'))
        db_cursor = db_obj.cursor()
        
        db_cursor.execute(statement)
        attr_array = db_cursor.fetchall()
        db_obj.close()
        
        return dict([(_[0], _[1:]) for _ in attr_array])
            
    def __del__(self):
        if self.__settings_obj != None:
            self.__settings_obj.close()
