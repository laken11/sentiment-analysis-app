const inputForm = document.querySelector('#input-form');
const outputDiv = document.querySelector('#output');
const resultDepression = document.querySelector('#dep');
const resultBipolarDisorder = document.querySelector('#bi');
const resultSchizophrenia = document.querySelector('#sch');
const resultPsychosis = document.querySelector('#psy');
const resultPtsd = document.querySelector('#ptsd');
const resultP = document.querySelector('#result');

async function postData(url, requestData) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        return await response.json()
    } catch (error) {
        console.error('Error:', error);
    }
}

inputForm.addEventListener('submit', async e => {
    e.preventDefault();
    const inputText = document.querySelector('#input-text').value;
    if (inputText.length === 0 || inputText === '') {
        resultP.textContent = "Please provide a text to analyse";
        outputDiv.style.display = 'block';
    } else {
        const loader = document.getElementById('loader');  // Get the loader element
        outputDiv.style.display = 'none';
        loader.style.display = 'block';  // Show the loader

        // Define the request data
        const requestData = {
            statement: inputText
        };
        const response = await postData("/backend/analyse", requestData);
        // Hide the loader after receiving the response
        loader.style.display = 'none';
        if (!response['status']) {
            resultP.textContent = "An error occurred";
        } else {
            const depression = response["message"]["Depression"];
            const Bipolar_Disorder = response["message"]["Bipolar Disorder"]
            const Schizophrenia = response["message"]["Schizophrenia"]
            const Psychosis = response["message"]["Psychosis"]
            const Ptsd = response["message"]["Ptsd"]
            resultDepression.textContent = `Depression: ${depression}`
            resultBipolarDisorder.textContent = `Bipolar Disorder: ${Bipolar_Disorder}`
            resultSchizophrenia.textContent = `Schizophrenia: ${Schizophrenia}`
            resultPsychosis.textContent = `Psychosis: ${Psychosis}`
            resultPtsd.textContent = `PTSD: ${Ptsd}`;
            resultP.textContent = ""
            outputDiv.style.display = 'block';
        }
    }

});


