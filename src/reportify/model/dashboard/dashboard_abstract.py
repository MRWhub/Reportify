from pydantic import BaseModel, field_validator, model_validator
from typing import List, Any , Callable, Optional
import os
from dotenv import load_dotenv
import airbyte as ab
from datetime import datetime
class AbstractDashboard(BaseModel): #Estava escrito AbstractDasboard
    streams: List[str]
    repo: str = ""
    token: str = ""
    cache: Any = None
    save_func: Optional[Callable] = None
    def model_post_init(self, __context):

        print(f"🔑 Usando repositório: {self.repo}"
              f" com token: {self.token[:4]}... (ocultando o restante)")
        self.fetch_data()
        

    def fetch_data(self):
        print(f"🔄 Buscando issues para {self.repo}...")
        try:
            source = ab.get_source(
                "source-github",
                install_if_missing=True,
                config={
                    "repositories": [self.repo],
                    "credentials": {"personal_access_token": self.token},
                },
            )
            source.check()
            source.select_streams(self.streams)
            cache = ab.get_default_cache()
            source.read(cache=cache)
            self.cache = cache


        except Exception as e:
            print(f"❌ Erro ao buscar: {str(e)}")

