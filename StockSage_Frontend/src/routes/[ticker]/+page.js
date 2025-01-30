/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch }) {
    // const fromDate = '2024-01-01'
    // const toDate = '2025-01-21'

    const url = `http://127.0.0.1:8000/get-data/${params.ticker}/`
    
    let returnVal = undefined

    
    try {
        const response = await fetch(url, {
            Headers: {
                'Access-Control-Allow-Origin': 'http://localhost:5173/'
            }
        });
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        const json = await response.json();

        returnVal = json.response
    } catch (error) {
        console.error(error.message);
    }

    let data = []

    if (returnVal !== undefined) {
        for (const [key, val] of Object.entries(returnVal)) {
            let dict = {
                x: new Date(val['Date']),
                o: val['Open'],
                h: val['High'],
                l: val['Low'],
                c: val['Close'],
                v: val['Volume'],
            }
            data.push(dict)
        }
    }
    

    return {
        data: data,
        ticker: params.ticker.toString().toUpperCase(),
        // from: fromDate,
        // to: toDate,
        ok: returnVal ? true: false
    };
}

export const ssr = false