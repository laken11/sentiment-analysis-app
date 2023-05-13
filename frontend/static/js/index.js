const inputForm = document.querySelector('#input-form');
const outputDiv = document.querySelector('#output');
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
    const stressor = document.querySelector('#stressor').value;

    const loader = document.getElementById('loader');  // Get the loader element
    outputDiv.style.display = 'none';
    loader.style.display = 'block';  // Show the loader

    // Define the request data
    const requestData = {
        statement: inputText,
        stressor: stressor
    };
    const response = await postData("/backend/analyse", requestData);
    // Hide the loader after receiving the response
    loader.style.display = 'none';
    if (!response['status']) {
        resultP.textContent = "An error occurred";
    }
    resultP.textContent = response["message"];
    outputDiv.style.display = 'block';
});


