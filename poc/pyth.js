const { PythonShell } = require('python-shell')

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


async function main() {
    const retailer = 'target'
    const identifier = 77640693
    
    const result = await runPython('../src/checkPrice.py', [retailer, identifier])

    return result
}

final = main()

setTimeout(() => {
    console.log(final)
}, 3000)