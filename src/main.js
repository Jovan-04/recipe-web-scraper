const { PythonShell } = require('python-shell')
const cache = require('../assets/cache.json')
const densities = require('../assets/densities.json')

class Ingredient {
  constructor (amount, unit, name) {
    this.amount = amount
    this.unit = unit
    this.name = name
  }
}

const fromXToGrams = { // multiply X by this number to get grams
  'ounce': 28.35,
  'pound': 453.5,
  'gram': 1.0,
  'kilogram': 1000.0
}

const fromXToCubCM = { // multiply X by this number to get cubic cm/ml
  'teaspoon': 4.929,
  'tablespoon': 14.787,
  'fluid ounce': 29.574,
  'cup': 240.0,
  'quart': 946.353,
  'pint': 473.176,
  'gallon': 3785.410,
  'liter': 1000.0,
  'milliliter': 1
}

async function main () {
  const ingredientList = document.getElementById('ingredInText').value
  const ingredientLines = ingredientList.split('\n')

  let ingredients = []

  for (const line of ingredientLines) {
    let result = await parseIngredient(line)

    if (result === "manual") {
      // if result is a manual parsing request, act on it and call again
    }

    ingredients.push(result)
  } 
  
  // ingredients is now an array of Ingredient objects [...]

  let ingredientsByWeight = []
  for (const ing of ingredients) {
    ingWeight = convertToWeight(ing)
    ingredientsByWeight.push(ingWeight)
    // update Ingredient instance to reflect the new weight
    // search cache to link ing.name into target & walmart product ids and add as a property; .targetID and .walmartID respectively
    // show best guesses for products and allow user to adjust; display parts of their web pages?

  }

  console.log(ingredientsByWeight)

  const retailer = document.getElementById('selectRetailer').value
  const toDom = []
  let netPrice = 0

  for (const ing of ingredientsByWeight) {
    const centsPerGram = cache[ing.name][retailer]['cents_per_gram']
    const price = parseFloat(((ing.amount * centsPerGram) / 100).toFixed(2))
    console.log(`${ing.amount}g of ${ing.name} costs $${price} from ${retailer}.`)
    output = `${ing.amount}g ${ing.name}: $${price}`
    
    toDom.push(output)
    netPrice += price
  }

  const target = document.getElementById("ingredOut")
  target.innerHTML = ""

  for (const ing of toDom) {
    const p = document.createElement('p')
    p.innerHTML = ing
    target.appendChild(p)
  }

  document.getElementById('netCost').value = netPrice

}

async function runPython(file, args) {
  const { success, err = '', results } = await new Promise((resolve, reject) => {
    PythonShell.run(file, { args: args }, (err, results) => {
      if (err) {
        reject({ success: false, err: err, results: null })
      }
      resolve({ success: true, err: null, results: results})
    })
  })
  return [success, err, results]
}


async function parseIngredient (line) {
  results = await runPython('parseIngredient.py', [line])

  if (results[0] === false) {
    console.error(results[1])
    return "manual"
  }

  const ingredient = new Ingredient(...(JSON.parse(results[2][0].replaceAll("'", '"'))))
  return ingredient
}

async function manualParse(line) {
  return parseIngredient(line) // need some way to let user parse the ingredient. or is that something we won't need? 
}

function convertToWeight(ingredient) {
  // if it's a unit of weight, convert directly to grams, no density needed
  if (['ounce', 'pound', 'gram', 'kilogram'].includes(ingredient.unit)) {
    const newAmount = ingredient.amount * fromXToGrams[ingredient.unit]
    const newUnit = 'gram'
    return new Ingredient(newAmount, newUnit, ingredient.name)
  }

  // if it's a unit of volume, first convert it into cubic cm; then, cubic cm => grams using density (grams per cubic cm)
  if (['teaspoon', 'tablespoon', 'fluid ounce', 'cup', 'quart', 'pint', 'gallon', 'liter', 'milliliter'].includes(ingredient.unit)) {
    const mlAmount = ingredient.amount * fromXToCubCM[ingredient.unit] // volume converted to mL

    const newAmount = densities[ingredient.name] * mlAmount
    const newUnit = 'gram'
    return new Ingredient(newAmount, newUnit, ingredient.name)
  }

}

function ingredientPrice (pricePerWeight, weight) {
  return pricePerWeight * weight // convert units & format here if needed; return as a string?
}

function checkPrice (tid) {
  // send api requests with python
  // use beautiful soup lib if the api doesn't work, but hopefully we won't have to touch that lol

  // how do we want to return this? price per unit of weight?
}

function updateScaleText() {
  label = document.getElementById("serSclCostLabel")
  select = document.getElementById("adjustMenu")
  texts = {
    '0': 'Servings: ',
    '1': 'Scale To: ',
    '2': 'Target Cost: $'
  }
  label.innerHTML = texts[select.selectedIndex]
}
