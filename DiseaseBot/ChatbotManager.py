from openai import AzureOpenAI
import json

tools_list = json.load(open('C:/Users/UGUPTA6/Pearson_Projects/DiseaseBot/functions.json'))

class MedicalAssistant:
    
    def __init__(self, test):
        self.API_KEY="181834e9dfb84c5290ac02465c8898c2" 
        self.ENDPOINT="https://vue-sb-bi-openai.openai.azure.com/"
        print(test)   
        self.azureOpenaiClient = None
        self.chatAssistant = None
        self.chatThread = None

    def initialize(self):
        self.create_client()
        self.create_assistant()
        self.create_thread()

        
    def create_client(self):
        self.azureOpenaiClient  = AzureOpenAI(
            #api_key=os.getenv("API_KEY"),
            api_key= self.API_KEY,
            azure_endpoint= self.ENDPOINT,
            api_version="2024-05-01-preview"
        )
        
    def create_assistant(self):
       self.chatAssistant = self.azureOpenaiClient.beta.assistants.create(
            name = "Medical Assistant",
            instructions="You are a personal assistant for checking diseases that user may have based on symptoms provided. If the question I not related to anything medical then respond with Sorry I cannot help you with this.",
            tools=tools_list,
            model="gpt-4"
        )
      # print(self.chatAssistant)

    def create_thread(self):
        self.chatThread = self.azureOpenaiClient.beta.threads.create()
      #  print(self.chatThread)

    def create_message(self, query):
        message = self.azureOpenaiClient.beta.threads.messages.create(
            thread_id=self.chatThread.id,
            role="user",
            content=query
        )
        return message

    #Prepares a run enviornment with the current thread and assistant
    def create_run(self):
        run = self.azureOpenaiClient.beta.threads.runs.create(
            thread_id = self.chatThread.id,
            assistant_id = self.chatAssistant.id  
        )
        return run
    
    def retriveStatus(self, runId):
        status = self.azureOpenaiClient.beta.threads.runs.retrieve(
            thread_id = self.chatThread.id,
            run_id = runId
        )
        return status
    
    def getMessages(self):
        response_messages = self.azureOpenaiClient.beta.threads.messages.list( thread_id=self.chatThread.id)
        return response_messages
    
    def rerun(self, runId, tools_outputs):
       run = self.azureOpenaiClient.beta.threads.runs.submit_tool_outputs(
                        thread_id=self.chatThread.id,
                        run_id= runId,
                        tool_outputs=tools_outputs
                    )
       return run

