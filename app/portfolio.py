import uuid
import chromadb
import pandas as pd
from chromadb.config import Settings
class Portfolio:
    def __init__(self,file_path=r"C:\Users\nidhi\OneDrive\Desktop\Cold Email(GEN AI)\app\resource\companies_portfolio.csv"):
        self.file_path=file_path
        self.data=pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection=self.chroma_client.get_or_create_collection(name='portfolio')
        self.data.columns = self.data.columns.str.strip().str.lower().str.replace(" ", "_")
 
    def load_portfolio(self): 
        if not self.collection.count():
             for _, row in self.data.iterrows():
                 self.collection.add(documents=row["techstack"],
                       metadatas=[{"links":row["links"]}],  
                       ids=[str(uuid.uuid4())])        
    
    def query_links(self,skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas',[])