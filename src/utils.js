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

function tokenizedMatching(str1='', str2='') {
    const tokStr1 = str1.split(/[^A-Za-z0-9]+/)
    const tokStr2 = str2.split(/[^A-Za-z0-9]+/)

    tokStr1.filter(str => (str.length > 2))
    tokStr2.filter(str => (str.length > 2))

    for (const i of tokStr1) {
        for (const j of tokStr2) {
            if (levenshteinDistance(i, j) <= 2) {
                return true
            }
        }
    }

    return false
}

function levenshteinDistance(str1='', str2='') {
    const str1Limit = str1.length + 1
    const str2Limit = str2.length + 1
    const distance = Array(str1Limit)
    for (let i = 0; i < str1Limit; ++i) {
        distance[i] = Array(str2Limit)
    }
    for (let i = 0; i < str1Limit; ++i) {
        distance[i][0] = i
    }
    for (let j = 0; j < str2Limit; ++j) {
        distance[0][j] = j
    }

    for (let i = 1; i < str1Limit; ++i) {
        for (let j = 1; j < str2Limit; ++j) {
            const substitutionCost = (str1[i - 1] === str2[j - 1] ? 0 : 1)
            distance[i][j] = Math.min(
                distance[i - 1][j] + 1,
                distance[i][j - 1] + 1,
                distance[i - 1][j - 1] + substitutionCost
            )
        }
    }
    return distance[str1.length][str2.length]
}

function recursiveLevenshteinDistance(str1='', str2='') {
    if (str1.length === 0) return str2.length
    if (str2.length === 0) return str1.length

    if (str1[0] === str2[0]) return recursiveLevenshteinDistance(tail(str1), tail(str2))

    return 1 + Math.min(
        recursiveLevenshteinDistance(tail(str1), str2),
        recursiveLevenshteinDistance(str1, tail(str2)),
        recursiveLevenshteinDistance(tail(str1), tail(str2))
    )

    function tail(str) {
        return str.slice(1)
    }
}



module.exports = {
    Ingredient,
    sleep,
    retailers,
    fromXToGrams,
    fromXToCubCM,
    waitUntilClose,
    updateScaleText,
    levenshteinDistance,
    tokenizedMatching,
}
