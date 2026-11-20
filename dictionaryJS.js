const content = document.querySelector('.pokeDisplay');
const gen_size = document.getElementById('gen_No');
const searchBar = document.getElementById('searchBar');
const gen_butt = document.querySelectorAll('.btn');

let pokeData = [];
let newGen = '';
const generations = [];

const fetchData = async () => {
  await fetch('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')
    .then((res) => res.json())
    .then((data) => {
      const fetches = data.results.map((item) => {
        return fetch(item.url)
          .then((res) => res.json())
          .then((data) => {
            return {
              id: data.id,
              name: data.name,
              img: data.sprites.front_default,
              types: data.types,
              height: data.height,
              weight: data.weight,
            };
          });
      });
      Promise.all(fetches).then((res) => {
        pokeData = res;
        pokeCards('');
      });
    });
};
const genSize = () => {
  gen_butt.forEach((button) =>
    button.addEventListener('click', () => {
      let gen = button.getAttribute('id');
      console.log('Button GEN is ', gen);
      newGen = gen;
      console.log('NEw GEN is ', newGen);
      generation(newGen);
    })
  );
};
genSize();

const pokeCards = (searchString) => {
  const cards = pokeData
    .filter((pokemon) => {
      return pokemon.name.toLowerCase().includes(searchString);
    })
    .map((pokemon) => {
      const pokemonTypes = pokemon.types.map((item) => {
        return `<span class="type"> ${item.type.name}  </span>`;
      });
      return `<div class="card">
    <p>#${pokemon.id}</p>
    <img src="${pokemon.img}" alt="${pokemon.name}" />
    <h3 class="name_card">${pokemon.name}</h3>
    <div>
    <div class="types">${pokemonTypes.join('')}</div>
    <p>
    <span>${pokemon.height} cm</span>
    <span>${pokemon.weight.toFixed(1)} kg</span>
    </p>
    </div>
    </div>`;
    })
    .join('');
  content.innerHTML = cards;
};

fetchData();

const fetchPokemonForSpecies = async (speciesName) => {
  const pokemonResponse = await fetch(
    `https://pokeapi.co/api/v2/pokemon/${speciesName}`
  );

  if (pokemonResponse.ok) {
    return pokemonResponse.json();
  }

  const speciesResponse = await fetch(
    `https://pokeapi.co/api/v2/pokemon-species/${speciesName}`
  );
  if (!speciesResponse.ok) {
    return null;
  }

  const species = await speciesResponse.json();
  const defaultVariety = species.varieties.find((variety) => variety.is_default);
  if (!defaultVariety) {
    return null;
  }

  const varietyResponse = await fetch(defaultVariety.pokemon.url);
  return varietyResponse.ok ? varietyResponse.json() : null;
};

const generation = async (generationId) => {
  console.log('NewGEN is IN FUNCTION ', generationId);
  const url = `https://pokeapi.co/api/v2/generation/${generationId}/`;
  console.log(url);
  await fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log('Data Dump');
      console.log(data);
      let sizeGen = data.pokemon_species.length;
      gen_size.innerHTML = `The generation size is: ${sizeGen}`;
      const fetches2 = data.pokemon_species.map((result) => {
        return fetchPokemonForSpecies(result.name).then((pokemon) => {
          if (!pokemon) {
            return null;
          }

          return {
            id: pokemon.id,
            name: pokemon.name,
            img: pokemon.sprites?.front_default,
            types: pokemon.types,
            height: pokemon.height,
            weight: pokemon.weight,
          };
        });
      });
      return Promise.all(fetches2).then((response2) => {
        pokeData = response2.filter((pokemon) => pokemon);
        pokeCards('');
      });
    });
};

searchBar.addEventListener('keyup', (e) => {
  const searchString = e.target.value.toLowerCase();
  console.log(searchString);
  pokeCards(searchString);
});

const getTypeString = (type) => {
  return `<p>${type.type.name}</p>`;
};
