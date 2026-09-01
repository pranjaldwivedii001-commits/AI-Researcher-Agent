from agents import build_search_agent, build_scrape_agent , writer_chain

def run_research_agent(topic : str) -> dict :
    state={}

    print("search agent is working.....")

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"find recent , reliable and detailed info abour the: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content
    """print("search result:", state['search_results'])""" 

    print("reader agent is scraping importand info....")

    reader_agent = build_scrape_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user", 
            f"based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"search results:\n{state['search_results'][0:800]}"
        )]
    })
    state['scraped_content'] = reader_result['messages'][-1].content
    """print("scraped content", state['scraped_content'])"""

    research_combined = (
        f"search result : {state['search_results']}"
        f"scraped_result : {state['scraped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("Report", state['report'])
    return state

if __name__ == "__main__":
    topic = input("enter a research topic: ")
    run_research_agent(topic)


"""from agents import build_search_agent, build_scrape_agent, writer_chain

def run_research_pipeline():
    topic = input("Enter a research topic: ")
    
    print("🔍 Search agent is working...")
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable, and detailed info about: {topic}")]
    })
    
    # Extract text from search agent output
    search_data = search_result["messages"][-1].content
    
    print("🌐 Scrape agent is working...")
    scrape_agent = build_scrape_agent()
    scrape_result = scrape_agent.invoke({
        "messages": [("user", f"Extract key technical insights or content related to: {topic}")]
    })
    
    # Extract text from scrape agent output
    scrape_data = scrape_result["messages"][-1].content
    
    # Combine research data
    combined_research = f"--- Search Results ---\n{search_data}\n\n--- Scraped Data ---\n{scrape_data}"
    
    print("✍️ Writer chain is generating your final report...")
    final_report = writer_chain.invoke({
        "topic": topic,
        "research": combined_research
    })
    
    print("\n" + "="*40 + "\nFINAL RESEARCH REPORT\n" + "="*40)
    print(final_report)

if __name__ == "__main__":
    run_research_pipeline()"""


