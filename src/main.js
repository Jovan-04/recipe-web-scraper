const { PythonShell } = require('python-shell')

class Ingredient {
  constructor (name, amount, unit) {
    this.name = name
    this.amount = amount
    this.unit = unit
  }
}


function main () {
  const ingredientList = document.getElementById('ingredInText').value
  const ingredientLines = ingredientList.split('\n')

  let ingredients = []

  for (const line of ingredientLines) {
    let result = parseIngredient(line)

    if (result === "manual") {
      // if result is a manual parsing request, act on it and call again
    }

    ingredients.push(result)
  } 
  
  // ingredients is now an array of Ingredient objects [...]

  for (const ing of ingredients) {
    // ing is an instance of Ingredient
    // convert ing.name into target product id and add as a property; maybe `.identifier`
    // show best guesses for products and allow user to adjust
  }

  // do a bunch of calculations, starting with converting everything to target prices
  // then, send all that crap to the dom lmao
}

async function runPython(file, args) {
  const { success, err = '', results } = await new Promise((resolve, reject) => {
    PythonShell.run(file, { args: args }, (err, results) => {
      if (err) {
        reject({ success: false, err: err})
      }
      resolve({ success: true, results: results})
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

function convertToWeight(ingredient) {
  // we'll need to do a lot of unit conversions; perhaps we can use some data structure to do that?
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
