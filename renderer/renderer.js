// const startExtractionButton = document.getElementById('startExtraction');
// const startAgentButton = document.getElementById('startAgent');
// const outputElement = document.getElementById('output');
 
// function appendToOutput(message) {
//   // This replaces both \n and escaped \\n newlines with <br> tags
//   const formattedMessage = message.replace(/\\n/g, '<br>').replace(/\n/g, '<br>');
//   outputElement.innerHTML += formattedMessage + '<br>';
//   outputElement.scrollTop = outputElement.scrollHeight;
// }
 
// startExtractionButton.addEventListener('click', async () => {
//   appendToOutput('Starting email extraction...');
//   await window.electronAPI.startExtraction();
// });
 
// startAgentButton.addEventListener('click', async () => {
//   appendToOutput('Starting agent...');
//   try {
//     const result = await window.electronAPI.startAgent();
//     // appendToOutput(`Extraction completed`);
//   } catch (error) {
//     appendToOutput(`Error starting agent: ${error}`);
//   }
// });
 
// window.electronAPI.onAgentLog((message) => {
//   appendToOutput(`${message}`);
// });
 
// window.electronAPI.onAgentError((message) => {
//   appendToOutput(`Agent Error: ${message}`);
// });
const startExtractionButton = document.getElementById('startExtraction');
const startAgentButton = document.getElementById('startAgent');
const outputElement = document.getElementById('output');

function appendToOutput(message) {
    // Replacing newline characters without adding unnecessary <br> tags
    const formattedMessage = message.replace(/\\n/g, '').replace(/\n/g, '');
    outputElement.innerHTML += formattedMessage;
    outputElement.scrollTop = outputElement.scrollHeight;
}

startExtractionButton.addEventListener('click', async () => {
    appendToOutput('Starting email extraction...');
    await window.electronAPI.startExtraction();
});

startAgentButton.addEventListener('click', async () => {
    appendToOutput('Starting agent...');
    try {
        const result = await window.electronAPI.startAgent();
    } catch (error) {
        appendToOutput(`Error starting agent: ${error}`);
    }
});

window.electronAPI.onAgentLog((message) => {
    appendToOutput(`${message}`);
});

window.electronAPI.onAgentError((message) => {
    appendToOutput(`Agent Error: ${message}`);
});

