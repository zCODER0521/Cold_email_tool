import os
from dotenv import load_dotenv 
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv() 
   
class Chain: 
    def __init__(self):
        self.llm = ChatGroq( model="llama3-70b-8192",    
    temperature=0, 
    groq_api_key=os.getenv("GROQ_API_KEY")
        )
    
    def extract_jobs(self,cleaned_text):
         
        prompt_extract = PromptTemplate.from_template(
    """ 
    ## SCRAPED TEXT FROM WEBSITE: 
    {page_data}
    The scraped text is from career's page of a website.
    Your job is to extract the job postings and return them in json format containing the following
    keys:role,skills,description.
    Return them in valid json. 
    ### NO PREAMBLE :
    """ 
)
        chain_extract=prompt_extract | self.llm 
        
        res=chain_extract.invoke(input={'page_data':cleaned_text}) 
        
        try:
            json_parser=JsonOutputParser ()
            res=json_parser.parse(res.content) 
            
        except OutputParserException:
            raise Exception("Context too big.Unable to pursue jobs")
        return res if isinstance(res,list) else[res]
    
    def write_mail(self,job,links):
        
        prompt_email=PromptTemplate.from_template(
    """ 
    ### JOB DESCRIPTION:
      {job_description}
    ### INSTRUCTION:
    You are Raj a business development executive at XYZ.XYZ is an AI and software based company dedicated to seamless integration of business 
    processes through the use of automated tools.
    Your job is to write a cold email to clients regarding the job mentioned above describing the capability 
    in fulfilling their needs.
    Also add the most relevant ones from the following links to showcase Raj's portfolio:{link_list}
    Remember you are Raj,BDE at XYZ.
    Do not provide a PREAMBLE.
    ### EMAIL (NO PREAMBLE):
    """ 
) 

        chain_email=prompt_email | self.llm
        res=chain_email.invoke({"job_description":str(job),"link_list":links})       
        return res 