from typing import Tuple
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from output_parsers import Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def nexuslink_ai_with(name: str) -> Tuple[Summary, str]:
    """
    Main function to orchestrate the AI agent.
    1. Looks up a LinkedIn profile URL.
    2. Scrapes the profile data.
    3. Uses an LLM to generate a summary and facts based on the data.
    """
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
        given the Linkedin information {information} about a person, I want you to create:
        1. a short, professional summary
        2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template
    )
    
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    
    structured_llm = llm.with_structured_output(Summary)


    chain = summary_prompt_template | structured_llm
    
    res = chain.invoke(input={"information": linkedin_data})


    if not isinstance(res, Summary):
        res = Summary(**res)
    
    return res, linkedin_data.get("photoUrl", "")

if __name__ == "__main__":
    load_dotenv()
    print("NexusLink AI Enter")
    
    summary_result, picture_url = nexuslink_ai_with(name="Sundar Pichai")
    print(summary_result)
    print(picture_url)
