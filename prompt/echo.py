from langchain.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate,
                               MessagesPlaceholder)

ECHO_TEMPLATE = """Current date and time: {date_time}
You are {hero_name}.

Here is some relevant information about {hero_name} to help with the conversation.
---
{relevant_info}
---
Your role is to reply the user as {hero_name} would.
"""

ECHO_PROMPT = ChatPromptTemplate(messages=[
    SystemMessagePromptTemplate.from_template(ECHO_TEMPLATE),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{user_text}")
])
