from .LLMEnums import LLMEnum,OPENAIENUMS,GOOGLEENUMS
from ..llms.providers import OpenAIProvider,GoogleProvider

class LlmProviderFactory():
    def __init__(self,config:dict):
        self.config=config


    def create(self,provider:str):

        if provider == LLMEnum.GOOGLE.value:
         return GoogleProvider(api_key=self.config.GOOGLE_API_KEY,
                               default_max_input_tokens=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                               default_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                               default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE)
        
        if provider == LLMEnum.OPENAI.value:
           return OpenAIProvider(api_key=self.config.OPENAI_API_KEY,
                                 api_url=self.config.OPENAI_API_URL,
                                 default_max_input_tokens=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                                 default_max_output_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                                 default_tempreture=self.config.GENERATION_DAFAULT_TEMPERATURE
                                 )
        
        return None
        

         
