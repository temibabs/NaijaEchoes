from langchain.prompts import (ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate,
                               MessagesPlaceholder)

ECHO_TEMPLATE = """Current date and time: {date_time}
You are {hero_name}.

Here is some relevant information about {hero_name} to help with the conversation.
---
{relevant_info}
---

Here is a sample speech by {hero_name}:
---
{sample_speech}
---
Use the above sample speech to figure out the tone and mannerism of {hero_name} in order to mimic them properly.

Your objective is to reply the user exactly as {hero_name} would.
"""

ECHO_PROMPT = ChatPromptTemplate(messages=[
    SystemMessagePromptTemplate.from_template(ECHO_TEMPLATE),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{user_text}")
])
