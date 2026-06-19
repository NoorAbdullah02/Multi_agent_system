import json

from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def stringify_pipeline_output(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        items = []
        for item in value:
            if isinstance(item, dict):
                if "text" in item:
                    items.append(item["text"])
                else:
                    items.append(json.dumps(item, indent=2))
            else:
                items.append(str(item))
        return "\n\n".join(items)
    if isinstance(value, dict):
        return json.dumps(value, indent=2)
    return str(value)


def run_research_pipeline(topic: str) -> dict:
    state = {}

    #search agent WOrking

    print("\n"+" ="*50)

    print("step-1 - search agent is working on the topic: ",topic)
    
    print("\n"+" ="*50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about the topic: {topic}")]
     })

    state['search_result'] = stringify_pipeline_output(search_result['messages'][-1].content)

    print("\n search result ", state['search_result'])

    #step 2 -- reader agent

    print("\n"+" ="*50)

    print("step-2 - reader agent is working on the topic: ",topic)
    
    print("\n"+" ="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user", 
        f"Read and extract key insights from the following search results: {state['search_result'][:800]}")]
    })

    state['scraped_content'] = stringify_pipeline_output(reader_result['messages'][-1].content)

    print("\n scraped content ", state['scraped_content'])

    #step 3 -- writer chain

    print("\n"+" ="*50)
    print("step-3 - writer chain is working on the topic: ",topic)
    print("\n"+" ="*50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_result']}\n\nSCRAPED CONTENT:\n{state['scraped_content']}"
    )

    writer_result = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    state['final_report'] = stringify_pipeline_output(writer_result)
    print("\n Final Report \n", state['final_report'])

    #critic report

    print("\n"+" ="*50)
    print("step-4 - critic chain is evaluating the report on the topic: ",topic)
    print("\n"+" ="*50)

    state['feedback'] = stringify_pipeline_output(critic_chain.invoke({
        "report": state['final_report']
    }))

    print("\n Critic Feedback \n", state['feedback'])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    run_research_pipeline(topic)







