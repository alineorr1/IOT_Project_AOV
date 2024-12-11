#Libraries
import os
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
#logging config
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Logger Config
logger = logging.getLogger('myAppLogger')

#%%

def chat_gpt_summary(api_key: str, 
                     input_text: str) -> str:
    """
    Parameters
    ----------
    api_key : str
        Open AI api key.
    input_text : str
        Text to analyze.

    Returns
    -------
    str
        The chat gpt response.
    
    daily_activity_string = json.dumps(cleaned_activity, indent=4)
    df_json = merged_df_final.to_json(orient="records", indent=4)

    """
    
    os.environ['OPENAI_API_KEY'] = api_key

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], 
                                                   chunk_size=1200,
                                                   chunk_overlap=0)

    chunks = text_splitter.create_documents([input_text])

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7,
        max_tokens=1200,
        )

    # tokens = llm.get_num_tokens(input_text)

    map_prompt = """
    Write a concise summary of the following, emphasizing on personal health information:
    "{text}"
    CONCISE SUMMARY:
    """
    combine_prompt = """
    Write a concise summary of the following text delimited by triple backquotes.
    Return your response in the most important bullet points which covers the key health points 
    of the text for healthcare purposes.
    What should I take care the most? Answer me as if you were a doctor.
    ```{text}```
    BULLET POINT SUMMARY:
    """
    
    combine_prompt_template = PromptTemplate(template=combine_prompt, 
                                             input_variables=["text"])

    map_prompt_template = PromptTemplate(template=map_prompt, 
                                         input_variables=["text"])

    chain = load_summarize_chain(llm=llm, 
                                 chain_type='map_reduce',
                                 map_prompt=map_prompt_template,
                                 combine_prompt=combine_prompt_template,
                                 verbose=True)

    summary = chain.run(chunks)

    return summary

