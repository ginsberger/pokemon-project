import requests

pokemon_url = 'https://pokeapi.co/api/v2/pokemon/'


def get_pokemon_by_name(pokemon_name):
    return requests.get(url=pokemon_url + pokemon_name,verify=False).json()


def get_next_in_evolution_chain(pokemon_name):
    pokemon_data = get_pokemon_by_name(pokemon_name)
    species_url = pokemon_data["species"]["url"]
    species_info = requests.get(url=species_url,verify=False).json()
    evolution_chain_url = species_info["evolution_chain"]["url"]
    evolution_info = requests.get(url=evolution_chain_url,verify=False).json()
    return get_evolves_to_from_chain(evolution_info, pokemon_name)



def get_evolves_to_from_chain(chain_info, pokemon_name):
    chain = chain_info["chain"]
    
    while chain["species"]["name"] != pokemon_name:
        chain = chain["evolves_to"][0]

    if not chain["evolves_to"]:
        return None
    
    return chain["evolves_to"][0]["species"]["name"]