const { PythonShell } = require('python-shell')
const fs = require('fs')
const cache = require('../assets/cache.json')
const densities = require('../assets/densities.json')
const { resolve } = require('path')
const { once } = require('events')

const sleep = ms => new Promise((resolve) => setTimeout(resolve, ms)) // put this in utils.js

class Ingredient {
  constructor (amount, unit, name, price) {
    this.amount = amount
    this.unit = unit
    this.name = name
    this.price = price
  }
}

const retailers = ['target', 'walmart']

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

    if (result === 'None') continue

    ingredients.push(result)
  }
  
  // ingredients is now an array of Ingredient objects [...]
  const ingredientNames = new Set() // these are all the ingredients we need to get prices for
  for (const ing of ingredients) {
    ingredientNames.add(ing.name)
  }

  await updateIngredients(ingredientNames)

  let ingredientsByWeight = []
  for (const ing of ingredients) {
    ingWeight = convertToWeight(ing)
    ingredientsByWeight.push(ingWeight)
  }

  console.log(ingredientsByWeight)

  const retailer = document.getElementById('selectRetailer').value
  const toDom = []
  let netPrice = 0
  let modifier = 1

  const input = document.getElementById("serSclCostInput")
  const select = document.getElementById("adjustMenu")

  //   label.innerHTML = texts[select.selectedIndex]
  if (document.getElementById('cbAdjust').checked) {
    switch (select.selectedIndex) {
      case 0:
        modifier = parseFloat(input.value)
        break

      case 1:
        const recServ = document.getElementById('servingIn').value
        const targetServ = input.value
        modifier = targetServ / recServ
        break
        
      case 2:
        let tempPrice = 0
        const targetPrice = parseFloat(input.value)
        for (const ing of ingredientsByWeight) {
          const centsPerGram = cache[ing.name][retailer]['cents_per_gram']
          const price = parseFloat(((ing.amount * centsPerGram) / 100).toFixed(2))
          tempPrice += price
        }
        modifier = Math.round(targetPrice / tempPrice)
        break
    }
  }

  for (const ing of ingredientsByWeight) { // calculte final price
    const centsPerGram = cache[ing.name][retailer]['cents_per_gram']
    const price = parseFloat(((ing.amount * centsPerGram * modifier) / 100).toFixed(2))
    const amount = ing.amount * modifier
    const name = ing.name
    console.log(`${amount}g of ${name} costs $${price} from ${retailer}.`)
    output = `${amount.toFixed(1)}g ${name}: $${price}`
    
    toDom.push(output)
    netPrice += price
  }

  const target = document.getElementById("ingredOut")
  target.innerHTML = ""

  const p = document.createElement('p') // add modifier info
  p.innerHTML = `Recipe Breakdown (${modifier}x original quantities):`
  target.appendChild(p)

  for (const ing of toDom) {
    const p = document.createElement('p')
    p.innerHTML = ing
    target.appendChild(p)
  }

  document.getElementById('netCost').value = netPrice.toFixed(2)

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

  if (results[2][0] === '[0, None, None]') return 'None' // empty line got parsed, ignore it

  const ing = JSON.parse(results[2][0].replaceAll("'", '"').replaceAll('None', null))

  const ingredient = new Ingredient(...ing)
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
    return new Ingredient(newAmount, newUnit, ingredient.name, ingredient.price)
  }

  // if it's a unit of volume, first convert it into cubic cm; then, cubic cm => grams using density (grams per cubic cm)
  if (['teaspoon', 'tablespoon', 'fluid ounce', 'cup', 'quart', 'pint', 'gallon', 'liter', 'milliliter'].includes(ingredient.unit)) {
    const mlAmount = ingredient.amount * fromXToCubCM[ingredient.unit] // volume converted to mL

    const newAmount = densities[ingredient.name] * mlAmount
    const newUnit = 'gram'
    return new Ingredient(newAmount, newUnit, ingredient.name, ingredient.price)
  }
}

async function updateIngredients(ingredients) {
  const entriesToCreate = []

  for (const ing of ingredients.values()) {
    if (cache.hasOwnProperty(ing)) { // check timestamp and update if needed
      console.log(`${ing} found in cache`)
      const now = Math.round((Date.now()) / 1000)

      for (const rtlr of ['target']/* retailers*/) {
        const product = cache[ing][rtlr]
        const time = product['unix_time_updated']
        if ((now - time) > /*1209600*/10) { // cached price is more than two weeks old, update
          const cpg = await getIngredientPrice(rtlr, product['identifier'], ing)
          product['cents_per_gram'] = parseFloat(cpg.toFixed(4))
          product['unix_time_updated'] = now
        }
      }
      
    } else {
      console.log(`${ing} not found in cache`)
      entriesToCreate.push(ing)
    }
  }

  if (entriesToCreate.length > 0) {
    const popup = window.open('./popup.html', undefined, "width=600,height=400")
    const allSearchResults = {}
  
    for (const rtlr of retailers) {
      allSearchResults[rtlr] = {}
      const rtlrDiv = popup.document.createElement('div')
      rtlrDiv.setAttribute('id', rtlr)
      rtlrDiv.innerHTML = `<h4> ${rtlr.toUpperCase()} </h4>`

      for (const ing of entriesToCreate) {
        const searchResults = await getSearchResults(rtlr, ing)
        allSearchResults[rtlr][ing] = searchResults

        const para = popup.document.createElement('p')
        const button = popup.document.createElement('button')
        button.innerText = 'Change'
        button.onclick = function () {
          popup.console.log(this.parentNode.textContent)
        }
        para.innerHTML = `<b>${ing.toUpperCase()}:</b> ${searchResults[0]}`
        para.appendChild(button)

        rtlrDiv.appendChild(para)
      }

      const container = popup.document.body
      container.append(rtlrDiv)
    }

    popup.console.log(allSearchResults)
    await waitUntilClose(popup)

    const termToUID = {}
    for (const rtlr of retailers) {
      const div = popup.document.getElementById(rtlr)
      termToUID[rtlr] = {}
      div.querySelectorAll('p').forEach((prod) => {
        const p = prod.innerText
        termToUID[rtlr][p.slice(0, p.indexOf(':')).toLowerCase()] = p.slice(p.lastIndexOf('(UID): ')+6, -6).trim()
      })
    }
    console.log(termToUID)

    for (const rtlr of retailers) {
      const now = Math.round((Date.now()) / 1000)
      for (const [term, identifier] of Object.entries(termToUID[rtlr])){
        const cpg = await getIngredientPrice(rtlr, identifier, term)
        
        if (!cache.hasOwnProperty(term)) { cache[term] = {} }

        cache[term][rtlr] = {
          "unix_time_updated": now,
          "cents_per_gram": parseFloat(cpg.toFixed(4)),
          "identifier": identifier
        }
      }
    }
  }

  console.log('saving file...')
  fs.writeFile('../assets/cache.json', JSON.stringify(cache), (err) => {
    if (err) throw err
    console.log('file saved')
  })
}

async function getIngredientPrice(retailer, identifier, name) {
  const results = await runPython('./checkPrice.py', [retailer, identifier])

  if (!results[0]) {
    console.error(results[1])
    return
  }

  const price = new Ingredient(...JSON.parse(results[2][0].replaceAll("'", '"').replaceAll('"name"', `"${name}"`)))
  const priceGrams = convertToWeight(price)
  const pricePerGram = (100 * parseFloat(priceGrams.price)) / priceGrams.amount

  return pricePerGram
}

async function getSearchResults(retailer, query) {
  const results = await runPython('./searchResults.py', [retailer, query])

  if (!results[0]) {
    console.error(results[1])
    return
  }

  const products = JSON.parse(results[2][0].replaceAll("'", '"'))

  return products
}


function waitUntilClose(window) { // more utils!!!
  return new Promise((resolve) => {
    function onClose() {
      window.removeEventListener('unload', onClose)
      resolve()
    }
    window.addEventListener('unload', onClose)
  })
}

function updateScaleText() { // move to a utils.js file
  const label = document.getElementById("serSclCostLabel")
  const select = document.getElementById("adjustMenu")
  const texts = {
    '0': 'Scale To: ',
    '1': 'Servings: ',
    '2': 'Target Cost: $'
  }
  label.innerHTML = texts[select.selectedIndex]
}
