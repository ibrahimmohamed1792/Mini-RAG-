import os


class template_praser:

    def __init__(self,language:str=None,default_language:str="en"):

        self.language=language
        self.default_language=default_language
        self.currnet_path=os.path.dirname(os.path.abspath(__file__))


    def set_language(self,language:str):
        if not language:
            self.language=self.default_language


        language_path=os.path.join(self.currnet_path,"locales",language)

        if not os.path.exists(language_path):
            self.language=self.default_language

        self.language=language


    def get(self,group:str,key:str,vars:dict={}):

        if not group or not key:
            return None
        
        group_path=os.path.join(self.currnet_path,"locales",self.language,f"{group}.py")
        targeted_language=self.language

        if not os.path.exists(group_path):
            group_path=os.path.join(self.currnet_path,"locales",self.default_language,f"{group}.py")
            targeted_language=self.default_language

        module=__import__(f"stores.llms.templates.locales.{targeted_language}.{group}",fromlist=[group])

        if not module:
            return None
        
        attributes=getattr(module,key)

        return attributes.safe_substitute(vars)





        

        