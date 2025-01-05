from ChatbotManager import MedicalAssistant
import json
import time
from tools import get_suggest_disease

class DiseaseCheckerBot:
    def __init__(self):
       print("initiating the disease bot app")
       self.medAssist = None
       self.diseases = json.load(open('C:/Users/UGUPTA6/Pearson_Projects/DiseaseBot/functions.json'))
    
       
    def launchApp(self):
        self.medAssist = MedicalAssistant("Setting up the Chatbot")
        self.medAssist.initialize()
        self.userPromt()

    def userPromt(self):
        print("Type 'exit' to kill the application")
        while(True):
            query = input("Query: ")
            if query == 'exit':
                break
            self.execute(query)

    def execute(self, query):
       # print("the user query is "+query)
       # self.DiseaseCache.lookup(query)

        self.medAssist.create_message(query)

        run = self.medAssist.create_run()

        while(True):
            time.sleep(5)
            status = self.medAssist.retriveStatus(run.id)

            # output = MedicalAssistant.createCompletion(query)
            # print(output)

            if status.status == "completed":
               messages = self.medAssist.getMessages()
               data = json.loads(messages.model_dump_json(indent=3))
               print(data['data'][0]['content'][0]['text']['value'])
               break

            elif status.status == "requires_action":
               # print(status.status)
                required_actions = status.required_action.submit_tool_outputs.model_dump()
               # print("req sts",required_actions)
                tools_response = status.required_action
               # print(tools_response)
                tools_outputs = []
                
                response = json.loads(tools_response.model_dump_json(indent=2))
               # response = json.loads(tools_response.model_dump_json(indent = 2))
                #Runs through list of required actions and matches them to pre-existing functions
                for function in required_actions["tool_calls"]:
                    name = function['function']['name']
                    # arguments = json.loads(function['function']['arguments'])
               # print(arguments)
                if name == "get_suggested_disease":
                    symptoms = json.loads(response['submit_tool_outputs']['tool_calls'][0]['function']['arguments'])['symptom']
                    guess = get_suggest_disease(symptoms)

                tools_outputs = [{
                                "tool_call_id": function['id'],
                                "output": str(guess)
                            }]

                run = self.medAssist.rerun(run.id, tools_outputs= tools_outputs)   

            else:
                print(status.status)