from chatbot import get_response


def generate_itinerary(destination, days, budget, interests):

    prompt = f"""
You are an AI Travel Assistant.

Create a travel itinerary for:

Destination: {destination}
Number of days: {days}
Budget: {budget}
Interests: {interests}

Provide:
1. Day-by-day activities
2. Places to visit
3. Food suggestions
4. Transportation suggestions
5. Approximate daily budget
6. Useful travel tips

Keep the itinerary practical, clear and easy to understand.
"""

    return get_response(prompt)