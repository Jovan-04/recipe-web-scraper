class Ingredient {
    constructor(amount, unit, name, price) {
        this.amount = amount
        this.unit = unit
        this.name = name
        this.price = price
    }
}

const sleep = ms => new Promise((resolve) => setTimeout(resolve, ms))

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

function waitUntilClose(window) {
    return new Promise((resolve) => {
        function onClose() {
            window.removeEventListener('unload', onClose)
            resolve()
        }
        window.addEventListener('unload', onClose)
    })
}

function updateScaleText() {
    const label = document.getElementById("serSclCostLabel")
    const select = document.getElementById("adjustMenu")
    const texts = {
        '0': 'Scale To: ',
        '1': 'Servings: ',
        '2': 'Target Cost: $'
    }
    label.innerHTML = texts[select.selectedIndex]
}

module.exports = {
    Ingredient,
    sleep,
    retailers,
    fromXToGrams,
    fromXToCubCM,
    waitUntilClose,
    updateScaleText
}