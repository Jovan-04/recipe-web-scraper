// import modules we're using
const { PythonShell } = require('python-shell')
const fs = require('fs')

// import stuff from other files
const cache = require('../assets/cache.json')
const densities = require('../assets/gramsPerCubicCM.json')
const gramsCount = require('../assets/gramsPerCount.json')

const { Ingredient, sleep, retailers, fromXToGrams, fromXToCubCM, waitUntilClose, updateScaleText } = require('./utils.js')


async function calculateRecipeCosts() { // runs when the 'calculate' button is clicked
  const ingredientList = document.getElementById('ingredInText').value
  const ingredientLines = ingredientList.split('\n') // split text input box into individual lines

  let ingredients = []

  for (const line of ingredientLines) {
    let result = await parseIngredient(line)

    if (result === "manual") {
      result = await manualParse(line)
      // if result is a manual parsing request, act on it and call again
    }

    if (result === 'None') continue

    ingredients.push(result)
  }

  // ingredients is now an array of Ingredient objects [...]
  const ingredientNames = new Set() // these are all the ingredients we need to get prices for
  const ingredientsDensity = new Set()
  const ingredientsCount = new Set()

  for (const ing of ingredients) {
    ingredientNames.add(ing.name)
    if (['count'].includes(ing.unit)) ingredientsCount.add(ing.name)
    if (['ounce', 'pound', 'gram', 'kilogram', 'teaspoon', 'tablespoon', 'fluid ounce', 'cup', 'quart', 'pint', 'gallon', 'liter', 'milliliter']
    .includes(ing.unit)) ingredientsDensity.add(ing.name)
  }

  await checkGramsPerCubicCM(ingredientsDensity) // check that all necessary ingredients in our recipe have a density

  await checkGramsPerCount(ingredientsCount) // check that all necessary ingredients in our recipe have a weight/count

  await updateIngredients(ingredientNames) // update cached prices for all ingredients in our recipe

  let ingredientsByWeight = []
  for (const ing of ingredients) { // convert all our ingredients to grams for use internally
    ingWeight = convertToWeight(ing)
    ingredientsByWeight.push(ingWeight)
  }

  console.log(ingredientsByWeight) // add more console.logs so that it's easier to track what's going on through the console?

  const retailer = document.getElementById('selectRetailer').value // figure out what retailer we're getting prices from
  const toDom = []
  let netPrice = 0
  let modifier = 1

  const input = document.getElementById("serSclCostInput")
  const select = document.getElementById("adjustMenu")

  if (document.getElementById('cbAdjust').checked) { // checkbox for recipe scaling
    switch (select.selectedIndex) { // switch based on which scaling option the user selected
      case 0: // scale factor
        modifier = parseFloat(input.value)
        break

      case 1: // servings
        const recServ = document.getElementById('servingIn').value
        const targetServ = input.value
        modifier = targetServ / recServ
        break

      case 2: // cost
        let origPrice = 0
        const targetPrice = parseFloat(input.value)
        for (const ing of ingredientsByWeight) { // calculate the cost without scaling
          const centsPerGram = cache[ing.name][retailer]['cents_per_gram']
          const price = parseFloat(((ing.amount * centsPerGram) / 100).toFixed(2))
          origPrice += price
        }
        modifier = Math.round(targetPrice / origPrice) // calculate an approximate modifier to estimate target cost
        break
    }
  }

  for (const ing of ingredientsByWeight) { // calculate final price for each item
    const centsPerGram = cache[ing.name][retailer]['cents_per_gram']
    const price = parseFloat(((ing.amount * centsPerGram * modifier) / 100).toFixed(2))
    const amount = ing.amount * modifier
    const name = ing.name
    console.log(`${amount}g of ${name} costs $${price} from ${retailer}.`)
    output = `${amount.toFixed(1)}g ${name}: $${price}`

    toDom.push(output)
    netPrice += price
  }

  const target = document.getElementById("ingredOut") // clear current output
  target.innerHTML = ""

  const p = document.createElement('p') // send modifier info to dom
  p.innerHTML = `Recipe Breakdown (${modifier}x original quantities):`
  target.appendChild(p)

  for (const ing of toDom) { // send all ingredients to dom
    const p = document.createElement('p')
    p.innerHTML = ing
    target.appendChild(p)
  }

  document.getElementById('netCost').value = netPrice.toFixed(2) // send final price to dom
}

async function runPython(file, args) { // runs specified python file with an array of args
  const { success, err = '', results } = await new Promise((resolve, reject) => {
    PythonShell.run(file, { args: args }, (err, results) => {
      if (err) {
        reject({ success: false, err: err, results: null })
      }
      resolve({ success: true, err: null, results: results })
    })
  })
  return [success, err, results]
}


async function parseIngredient(line) { // parses an ingredient from a line of text, and returns an Ingredient instance
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
  // need some way to let user parse the ingredient. or is that something we won't need? 
}

function convertToWeight(ingredient) { // convert an ingredient from any unit to one in grams
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

  // if it's a count, convert directly to weight using the count conversions
  if (['count'].includes(ingredient.unit)) {
    const newAmount = ingredient.amount * gramsCount[ingredient.name]
    const newUnit = 'gram'
    return new Ingredient(newAmount, newUnit, ingredient.name, ingredient.price)
  }

  throw new Error(`Invalid unit ${ingredient.unit} for weight conversion`)
}

async function updateIngredients(ingredients) { // updates the prices of ingredients needed in the recipe
  const entriesToCreate = [] // change to using a set?

  for (const ing of ingredients.values()) {
    if (cache.hasOwnProperty(ing)) { // check timestamp and update if needed
      console.log(`${ing} found in cache`)
      const now = Math.round((Date.now()) / 1000)

      for (const rtlr of retailers) {
        const product = cache[ing][rtlr]
        const time = product['unix_time_updated']
        if ((now - time) > 1209600) { // cached price is more than two weeks old, update
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

    for (const rtlr of retailers) { // create a div for each retailer
      allSearchResults[rtlr] = {}
      const rtlrDiv = popup.document.createElement('div')
      rtlrDiv.setAttribute('id', rtlr)
      rtlrDiv.innerHTML = `<h4> ${rtlr.toUpperCase()} </h4>`

      for (const ing of entriesToCreate) { // add search results for each product to that retailer's div 
        const searchResults = await getSearchResults(rtlr, ing)
        allSearchResults[rtlr][ing] = searchResults

        const para = popup.document.createElement('p')
        const button = popup.document.createElement('button')
        button.innerText = 'Change'
        button.onclick = function () { // big nasty function that doesn't work quite right :(
          this.disabled = true
          let i = 0
          for (const res of allSearchResults[rtlr][ing]) {
            if (i >= 7) break
            const p = popup.document.createElement('p')

            const b = popup.document.createElement('button')
            b.innerText = 'Select'
            b.onclick = function () { // how to do this recursively??
              popup.console.log(this.parentNode)
              popup.console.log(this.parentNode.innerHTML)

              const newThing = this.parentNode
              // newThing.innerHTML = this.parentNode.innerHTML

              popup.console.log(newThing)
              popup.console.log(newThing.innerHTML)

              const nb = newThing.querySelector('button')
              const func = this.parentNode.parentNode.querySelector('button').onclick

              // popup.console.log(func)
              // popup.console.log(nb)

              nb.addEventListener('click', func)
              nb.innerText = 'Change'
              nb.disabled = true

              // popup.console.log(func)
              // popup.console.log(nb)

              // popup.console.log(this.parentNode.parentNode)

              this.parentNode.parentNode.innerHTML = newThing.innerHTML
            }

            p.innerHTML = `<b>${ing.toUpperCase()}:</b> ${res}`
            p.appendChild(b)
            this.parentNode.appendChild(p)

            i++
          }

          const cp = popup.document.createElement('p')
          cp.className = ing

          const cb = popup.document.createElement('button')
          cb.innerText = 'Select'
          cb.onclick = function () {
            console.log(this.innerText)
            this.parentNode.parentNode.innerHTML = `<b>${ing.toUpperCase()}:</b> Custom - (UID): ${this.parentNode.querySelector('input').value} <button disabled=true> Change </button>`
          }

          cp.innerHTML = `<b>${ing.toUpperCase()}:</b> Custom - (UID): <input type="number">`
          cp.appendChild(cb)
          this.parentNode.appendChild(cp)
        }
        para.innerHTML = `<b>${ing.toUpperCase()}:</b> ${searchResults[0]}`
        para.appendChild(button)

        rtlrDiv.appendChild(para)
      }

      const container = popup.document.body
      container.append(rtlrDiv)
    }

    popup.console.log(allSearchResults)
    await waitUntilClose(popup) // waits for popup menu to close, meaning we've submitted our ingredient choices

    const termToUID = {}
    for (const rtlr of retailers) { // gets the products we just submitted for each retailer
      const div = popup.document.getElementById(rtlr)

      termToUID[rtlr] = {} // create a temporary cache

      div.querySelectorAll('p').forEach((prod) => { // extract the product number from each entry, and save to a temporary cache
        const p = prod.innerText
        const key = p.slice(0, p.indexOf(':')).toLowerCase()
        const identifier = p.slice(p.lastIndexOf('(UID): ') + 6, -6).trim()

        termToUID[rtlr][key] = identifier
      })
    }
    console.log(termToUID)

    for (const rtlr of retailers) {
      const now = Math.round((Date.now()) / 1000) // get current unix time in seconds
      for (const [term, identifier] of Object.entries(termToUID[rtlr])) { // save each item in the temporary cache to the appropriate location in the permanent cache
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
  fs.writeFile('../assets/cache.json', JSON.stringify(cache), (err) => { // save the cache stored in program memory to a file on the disk
    if (err) throw err
    console.log('file saved')
  })
}

async function checkGramsPerCubicCM(ingredients) { // checks to make sure all ingredients in our recipe have a valid density
  const densitiesToGet = new Set()

  for (const ing of ingredients) {
    if (densities.hasOwnProperty(ing)) continue
    densitiesToGet.add(ing)
  }

  for (const ing of densitiesToGet) {
    // first, check if there are any ingredients already existing that look like they could match
    // substrings, unique matches, levenshtein distance?

    // if there are, confirm with user
    // create a new entry with the same density, but under the key `ing`

    // if there are no similar enough strings, prompt user to input a density in grams/mL
    // create a new entry with the input density, under the key `ing`

    // profit!
  }
}

async function checkGramsPerCount(ingredients) {
  const gramsCountToGet = new Set()

  for (const ing of ingredients) {
    if (gramsCount.hasOwnProperty(ing)) continue
    gramsCountToGet.add(ing)
  }

  for (const ing of gramsCountToGet) {
    // first, check if there are any ingredients already existing that look like they could match
    // substrings, unique matches, levenshtein distance?

    // if there are, confirm with user
    // create a new entry with the same density, but under the key `ing`

    // if there are no similar enough strings, prompt user to input a density in grams/mL
    // create a new entry with the input density, under the key `ing`

    // profit!
  }
}

async function getIngredientPrice(retailer, identifier, name) { // gets an ingredient's price and returns in cents per gram
  const results = await runPython('./checkPrice.py', [retailer, identifier]) // runs the 'checkPrice.py' file with cmd-line args as the retailer we want the product from, as well as the product's identifier

  if (!results[0]) { // if the script fails, log the error to the console
    console.error(results[1])
    return
  }

  const price = new Ingredient(...JSON.parse(results[2][0].replaceAll("'", '"').replaceAll('"name"', `"${name}"`))) // create a new Ingredient object from the results we got
  const priceGrams = convertToWeight(price) // convert it to grams
  const pricePerGram = (100 * parseFloat(priceGrams.price)) / priceGrams.amount // convert to cents per gram

  return pricePerGram // and return that value
}

async function getSearchResults(retailer, query) { // gets a list of search results for a particular query
  const results = await runPython('./searchResults.py', [retailer, query]) // runs the 'searchResults.py' file with cmd-line args as the retailer we want to search, as well as the search query

  if (!results[0]) { // if the script fails, log the error to the console
    console.error(results[1])
    return
  }

  const products = JSON.parse(results[2][0].replaceAll("'", '"')) // parse the json from the python file

  return products // and return it as an array
}
