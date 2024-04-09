import ollama

def summarize(paragraph:str):
    client = ollama.Client(host='http://localhost:11434')
    response = client.chat(model='gemma', messages=[
    {   
        'role': 'user',
        'content': f'Summarize the following paragraphin JSON format without modifying the original meaning, mandatory keys in JSON format are [companyName,newsSentiment,trend] and any other relevant keys. - {paragraph}',
    },
    ],
    stream=False,options={'temperature':0.0,'seed':24})
    #print(response,"\n\n\n")
    return (response['message']['content'])





    
