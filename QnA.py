from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def create_bot(NAME):
    Bot = ChatBot(name = NAME,
                  read_only = False,
                  logic_adapters = [
                    {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': 'I am sorry, but I do not understand. Please try again.',
                        'maximum_similarity_threshold': 0.90
                    }],
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")
    return Bot

def custom_train(Bot):
    trainer = ChatterBotCorpusTrainer(Bot)
    trainer.train("./data/QAList.yml")

def get_start_chatbot(Bot, message):
    response = Bot.get_response(message)
    return response