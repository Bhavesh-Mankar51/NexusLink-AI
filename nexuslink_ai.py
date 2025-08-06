from typing import Tuple
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def nexuslink_ai_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template = f"""
        given the Linkedin information {information} about a person from I want you to create:
        1. a short summary
        2. two intersecting acts about them
        \n{format_instructions} 
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOllama(temperature=0, model="gpt-3.5-turbo")

    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(input={"information": linkedin_data})
    return res, linkedin_data.get("photoUrl")

if __name__ == "__main__":
    load_dotenv()
    print("NexusLink AI Enter")
    nexuslink_ai_with(name="Bhavesh Mankar")

