from typing import Literal
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    card_file: str
    log_file: str
    save_type: Literal['file','sqlite','SQLITE','FILE']