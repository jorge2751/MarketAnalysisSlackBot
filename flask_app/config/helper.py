from flask_app.models.first_glance_bot import FirstGlanceBot


def initFirstGlanceBot(text, say):
    
    # Extract niche, city, and state from the user input
    try:
        state, niche, min_pop, max_pop = [x.strip() for x in text.split(",")]
    except ValueError:
        say("Please provide the input in the format 'state, niche, minimum population, maximum population'")
        return
    
    say(f"Running analysis for cities in {state}, offering {niche}, with populations between {min_pop} and {max_pop}...")
    
    # Use FirstGlanceBot to get a list of cities in the state with populations between min_pop and max_pop
    cities = FirstGlanceBot.get_cities(state, min_pop, max_pop)
    
    say(f"Found {len(cities)} cities in {state} with populations between {min_pop} and {max_pop}...")
    
    for city in cities:
        # Use FirstGlanceBot to get the google front page results
        location = f"{city}, {state}"
        search_results = FirstGlanceBot.get_search_results(niche, location)
        
        # If no results are found, skip to the next city
        if not search_results:
            say(f"No results found for {location}")
            continue
        
        # If map pack results are not found, skip to the next city
        if not search_results.get('map_pack'):
            say(f"No map pack results found for {location}")
            continue
        
        # Use FirstGlanceBot to process the map pack and organic results
        processed_map_pack = FirstGlanceBot.process_map_pack(search_results.get('map_pack'))
        processed_organic_results = FirstGlanceBot.process_organic_results(search_results.get('organic_results'))

        # Use FirstGlanceBot to count instances of prameters: city name in title, more than 10 reviews, and connected websites
        map_pack_analysis = FirstGlanceBot.analyze_map_pack(processed_map_pack, city)
        
        # Use FirstGlanceBot to count instances of parameters: city name in title, city name in link
        organic_analysis = FirstGlanceBot.analyze_organic_results(processed_organic_results, city)
        
        # Use FirstGlanceBot to compare niche to types of map pack results and descriptions of organic results
        type_and_description_analysis = FirstGlanceBot.analyze_types_and_descriptions(processed_map_pack, processed_organic_results, niche)

        # Use FirstGlanceBot to prepare the response in table format
        # table_response = FirstGlanceBot.prepare_response(map_pack_analysis, organic_analysis, type_and_description_analysis)
        # say(blocks=table_response)

        # Use FirstGlanceBot to decide weather or not to proceed with the analysis
        final_decision = FirstGlanceBot.decide_to_proceed(map_pack_analysis, organic_analysis, type_and_description_analysis)
        
        say(f"{final_decision} {location}")
    
    return "First glance analysis complete, bot terminating..."