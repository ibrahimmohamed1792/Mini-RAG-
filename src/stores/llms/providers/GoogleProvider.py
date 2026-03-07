from ...llms import LLMEnums,LLMInterface
from ...llms.LLMInterface import LLMInterface 
from google import genai
import os
from dotenv import load_dotenv
from google.genai import types
import logging 


class GoogleProvider (LLMInterface):
    def __init__(self,
                 api_key:str,
                 default_max_input_tokens:int=1000,
                 default_max_output_tokens:int=1000,
                 default_temperature :float=.1):
        
        
        
        
        self.default_max_input_tokens=default_max_input_tokens
        self.default_max_output_tokens=default_max_output_tokens
        self.default_tempreture=default_temperature 
        
        self.generation_model_id=None

        self.embedding_model_id=None
        self.embedding_model_dim=None
        self.api_key = api_key if api_key else os.getenv("GOOGLE_API_KEY")
        self.client=genai.Client(api_key=self.api_key)
        self.logger=logging.getLogger(__name__)

    
    def set_generation_model(self,model_id:str):
        self.generation_model_id=model_id

    def set_embedding_model(self,model_id:str,embedding_dim:int):
        self.embedding_model_id=model_id
        self.embedding_model_dim=embedding_dim

    def embed_text(self,text:str,document_type:str):
        if  not self.client :
            self.logger.error("Google client wasn't set")
            return None
        
        if not self.embedding_model_id :
            self.logger.error("embedding model not selected")
            return None
        
        response = self.client.models.embed_content(
        model=self.embedding_model_id,
         config={
          'output_dimensionality': self.embedding_model_dim
        },
        
        contents=text
           )
        
        if not response or not response.embeddings or len(response.embeddings)==0 or not response.embeddings:
            self.logger.error("embedding has failed")
        
        return response.embeddings[0].values
    
    def generate_text(self,prompt:str,chat_history:list=[],max_output_tokens:int=None,temperature :float=None):
        if  not self.client :
            self.logger.error("Google client wasn't set")
            return None
        
        if not self.generation_model_id :
            self.logger.error("generation model not selected")
            return None
        
        max_output_tokens= max_output_tokens if max_output_tokens else self.default_max_output_tokens
        temperature =temperature  if temperature  else self.default_tempreture
        # Ensure chat_history is a list if None is passed
        if chat_history is None:
            chat_history = []
        
        # If a string was accidentally passed, wrap it in the proper format or handle it
        if isinstance(chat_history, str):
            # If it's a string, we treat it as an initial user message or log a warning
            chat_history = [self.construct_prompt(prompt=chat_history, role=LLMEnums.GOOGLEENUMS.USER.value)]

            current_messege=self.construct_prompt(prompt=prompt,role=LLMEnums.GOOGLEENUMS.USER.value)
            full_content=chat_history+[current_messege]


            current_message = self.construct_prompt(prompt=prompt, role=LLMEnums.GOOGLEENUMS.USER.value)
            
            # Now both sides are lists, so + works!
            full_content = chat_history + [current_message]

        
        response = self.client.models.generate_content(
            model=self.generation_model_id,
            
            config=types.GenerateContentConfig(
            
            temperature=temperature,
            max_output_tokens=max_output_tokens),
            
            
            
        contents=full_content
    )
        
        return response.text

    





    def construct_prompt(self,prompt:str,role:str):
        return {"role":role,"parts":[{"text":prompt}]}



    

