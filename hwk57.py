from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

MODEL = "gemini-3.5-flash-lite"

@tool
def search_hotel(city: str) -> str:
    """Returns a list of hotels in a given city with their price per night in GEL."""
    hotel_data = {
        "tbilisi": [
            ("Megobrebi", 120),
            ("Hilton", 180),
            ("Radisson", 250),
        ],
        "batumi": [
            ("Sea View Hotel", 150),
            ("Boulevard Inn", 200),
            ("Black Sea Resort", 320),
        ],
        "kutaisi": [
            ("Imereti Guesthouse", 90),
            ("Kutaisi Central Hotel", 140),
        ],
    }

    hotels = hotel_data.get(city.strip().lower())
    if not hotels:
        return f"No hotels found in {city}."

    lines = [f"- {name} — {price} GEL/night" for name, price in hotels]
    return f"Hotels in {city}:\n" + "\n".join(lines)


@tool
def get_exchange_rate(currency: str) -> str:
    """Returns the exchange rate of a currency (e.g. USD, EUR, GBP) against the Georgian lari (GEL)."""

    rates = {
        "USD": 2.70,
        "EUR": 3.15,
        "GBP": 3.60,
    }

    code = currency.strip().upper()
    rate = rates.get(code)
    if rate is None:
        return f"Exchange rate for {currency} is not available."

    return f"1 {code} = {rate:.2f} GEL"


@tool
def search_attractions(city: str) -> str:
    """Returns a list of popular tourist attractions in a given city."""

    attractions_data = {
        "tbilisi": ["Narikala Fortress", "Old Tbilisi", "Mtatsminda Park"],
        "batumi": ["Batumi Boulevard", "Ali and Nino Statue", "Batumi Botanical Garden"],
        "kutaisi": ["Bagrati Cathedral", "Gelati Monastery", "Prometheus Cave"],
    }

    attractions = attractions_data.get(city.strip().lower())
    if not attractions:
        return f"No attractions found for {city}."

    lines = [f"- {place}" for place in attractions]
    return f"Popular attractions in {city}:\n" + "\n".join(lines)


llm = ChatGoogleGenerativeAI(
    model=MODEL
)

tools = [search_hotel, get_exchange_rate, search_attractions]
tools_by_name = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)

question = input("Enter your question: ")

messages = [
    SystemMessage(content=("""
        You are a helpful travel assistant for Georgia. 
        Use the available tools to answer questions about hotels, 
        exchange rates and attractions.
        """
    )),
    HumanMessage(content=question),
]
response = llm_with_tools.invoke(messages)

while response.tool_calls:
    messages.append(response)

    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"Executing tool: {tool_name}")
        print(f"Tool arguments: {tool_args}")

        selected_tool = tools_by_name.get(tool_name)
        if selected_tool is None:
            result = f"Error: unknown tool '{tool_name}'."
        else:
            result = selected_tool.invoke(tool_args)

        messages.append(ToolMessage(
            tool_call_id=tool_call["id"],
            content=str(result)
        ))

    response = llm_with_tools.invoke(messages)

print("Final response from the model:")
print(response.text)
