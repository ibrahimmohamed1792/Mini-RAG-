from pydantic import BaseModel
from typing import Optional


class Push_request(BaseModel):

    do_reset: Optional[int] =0 


class Search_request(BaseModel):
    text:str
    limit: Optional[int] = 5
