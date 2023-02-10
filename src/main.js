function main () {
  const ingredientList = document.getElementById('ingredIn')
  const ingredientLines = ingredientList.split('\n')

  const ingredients = []

  for (const line of ingredientLines) {
    let result = parseIngredient(line)
    // if result is a manual parsing request, act on it and call again

    ingredients.push(result)
  } 
  
  // ingredients is now a 2d array: [['1 cup', 'ap flour'], ['1 1/2 c.', 'granulated sugar'], ['4oz', 'whole milk']]

  for (const ing of ingredients) {
    //ing is ['1 cup', 'ap flour'] or similar
    //convert text into a target product id and amount by weight?
    //show best guesses for products and allow user to adjust
  }

  // we now have a 2d array of [wght, tid]
  // alternatively, we might be able to make a map (dictionary in python) {
  // 'ap flour': [wght, tid],
  // ...
  // }

  // for each element in the map, get the total price of it, update the map?

  // then, send all that shit to the dom lmao
}

function parseIngredient (line) {
  let amount
  let ingredient
  // parse stuff with python lol

  // return a manual parsing request if it fails some check; will need troubleshooting

  return [amount, ingredient]
}

function convertToWeight(amount, ingredient) {
  // how the hell are we gonna do this lmao
}

function convertToTID (ingredient) {
  // again, how the hell are we gonna do this lmao
}

function ingredientPrice (pricePerWeight, weight) {
  return pricePerWeight * weight // convert units & format here if needed; return as a string?
}

function checkPrice (tid) {
  // send api requests with python
  // use beautiful soup lib if the api doesn't work, but hopefully we won't have to touch that lol

  // how do we want to return this? price per unit of weight?
}