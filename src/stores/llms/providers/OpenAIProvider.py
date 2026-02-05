from ..llms import LLMInterface
from openai import OpenAI
import logging 
from ..llms import LLMEnums

class OpenAIProvider(LLMInterface):
    def __init__(self,api_key:str,api_url:str,
                 
                 default_max_input_tokens:int=1000,
                 default_max_output_tokens:int=1000,
                 default_tempreture:float=.1):
        
        self.api_key=api_key
        self.api_url=api_url
        
        self.default_max_input_tokens=default_max_input_tokens
        self.default_max_output_tokens=default_max_output_tokens
        self.default_temperature=default_tempreture
        
        self.generation_model_id=None

        self.embedding_model_id=None
        self.embedding_model_dim=None
        self.client=OpenAI(api_key=self.api_key,
                           base_url=self.api_url)
        
        self.logger=logging.getLogger(__name__)


    def set_generation_model(self,model_id:str):
        self.generation_model_id=model_id

    def set_embedding_model(self,model_id:str,embedding_dim:int):
        self.embedding_model_id=model_id
        self.embedding_model_dim=embedding_dim

    def generate_text(self,prompt:str,chat_history:list=[],max_output_tokens:int=None,temperature :float=None):
        if  not self.client :
            self.logger.error("OPENAI client wasn't set")
            return None
        
        if not self.generation_model_id :
            self.logger.error("generation model not selected")
            return None
        
        max_output_tokens= max_output_tokens if max_output_tokens else self.default_max_output_tokens
        temperature =temperature  if temperature  else self.default_temperature

        chat_history.append( self.construct_prompt(prompt=prompt,
                                                   role=LLMEnums.OPENAIENUMS.USER.value)
        )
        response=self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature 
        )
        if not response or  len(response.choices)==0 or not response.choices or not response.choices[0].message:
             self.logger.error("a problem occured generating response")
             return None

        return response.choices[0].message["content"]

    def process_prompt(self,text:str):

        text=text[:self.default_max_input_tokens].strip()









    def embed_text(self,text:str,document_type:str):
        if  not self.client :
            self.logger.error("OPENAI client wasn't set")
            return None
        
        
        
        if not self.embedding_model_id :
            self.logger.error("embedding model not selected")
            return None
        self.process_prompt(text=text)
        response=self.client.embeddings.create(model=self.embedding_model_id,
                                               dimensions=self.embedding_model_dim if self.embedding_model_dim else 1024 ,
                                               input=text)
        

        if not response or not response.data or len(response.data)==0 or not response.data[0].embedding:
            self.logger.error("embedding has failed")

        
        return response.data[0].embedding
    


    def construct_prompt(self,prompt:str,role:str):
        return {
            "role": role,
            "content":self.process_prompt(prompt)
        }

    
