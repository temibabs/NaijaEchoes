from langchain.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate,
                               MessagesPlaceholder)

ECHO_TEMPLATE = """You are a {hero_name}.

Your role is to reply the user as {hero_name} would.

"""

ECHO_PROMPT = ChatPromptTemplate(messages=[
    SystemMessagePromptTemplate.from_template(ECHO_TEMPLATE),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{user_text}")
])
