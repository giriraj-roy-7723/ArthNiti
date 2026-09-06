from langchain_core.messages import RemoveMessage, SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.agent_state import BusinessAgentState

from src.config.config import GEMINI_MODEL_NAME

# Use the absolute cheapest model for background summarization
summary_llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL_NAME, temperature=0.1)


async def summarize_and_trim_memory(state: BusinessAgentState):
    messages = state["messages"]
    summary = state.get("summary", "")

    # We only summarize and trim if we exceed our rolling window (e.g., 12 messages)
    if len(messages) <= 15:
        return {"messages": []}

    # Extract the messages we are about to trim (keep the most recent 6)
    messages_to_summarize = messages[:-6]

    summary_prompt = (
        f"Here is the current summary of the conversation:\n{summary}\n\n"
        "Here are the new messages:\n"
        f"{[msg.content for msg in messages_to_summarize]}\n\n"
        "Update the summary to include the new information. Keep it concise."
    )

    response = await summary_llm.ainvoke([HumanMessage(content=summary_prompt)])
    new_summary = response.content

    # LangGraph removes messages from state when you return a RemoveMessage object with their IDs
    delete_commands = [RemoveMessage(id=m.id) for m in messages_to_summarize]

    return {"summary": new_summary, "messages": delete_commands}
