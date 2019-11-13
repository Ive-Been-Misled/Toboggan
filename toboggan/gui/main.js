window.addEventListener('DOMContentLoaded', initiateGUI);

async function initiateGUI() {
  var skipTextCrawl = false;

  input.value = '';  // clear input textarea
  input.addEventListener('keydown', processEnter);
  text = await sendInput('look around')
  await displayScenario('' + text);
  //imprompt.innerHTML = "What do you do?";
}

consoleHistory = []
commandIndex = -1

async function processEnter(e) {
  if (e.code === 'ArrowUp') {
    if(commandIndex < consoleHistory.length - 1) {
      commandIndex++;
    }
    if(consoleHistory.length > 0) {
      input.value = consoleHistory[commandIndex]
    }
  }

  if (e.code === 'ArrowDown') {
    if(commandIndex > -1) {
      commandIndex--;
    }
    if(commandIndex == -1) {
      input.value = ''
    } else {
      if(consoleHistory.length > 0) {
        input.value = consoleHistory[commandIndex]
      }
    }
  }

  if (e.code !== 'Enter') return;

  skipTextCrawl = true;

  e.preventDefault(); // don't allow multi-line input
  if (!input.validity.valid) return; // don't allow empty input (minLength = 2)

  let inputText = input.value;
  consoleHistory.unshift(inputText)
  input.value = '';  // clear input textarea

  card.classList.add("loading");
  text = await sendInput(inputText);
  card.classList.remove("loading");

  displayScenario(text);
}

async function sendInput(inputText) {
  return fetch('/api', {
    method: 'POST',
    body: inputText,
    headers: {
      'Content-Type': 'text/plain'
    }
  })
  .then(response => response.text())
  .catch(function(error) {
    scenario.innerHTML = `
    No response from server.
    <br><br>
    The world is dead.
    `;
    imprompt.innerHTML = "You should close this tab now";
    console.error(error)
  }); 
}

async function displayScenario(text) {
  if (text === undefined) return;

  imprompt.classList.add("hidden");
  input.minLength = 0;
  input.maxLength = 0;

  //imprompt.innerHTML = "What do you do?";
  skipTextCrawl = false;

  let len = text.length;
  
  for(let i = 1; i <= len + 1; i++) {
    if (skipTextCrawl) i = len + 1;
    if (text[i] == '<') {
      i = i + 3;
      if (text[i + 1] == '/' || text[i + 1] == 'b') i = i + 1;
    }
    scenario.innerHTML = text.substring(0, i);
    scenario.scrollIntoView(false); // make bottom of text visible
    await new Promise(resolve => setTimeout(resolve, 8)); // sleep for x ms
  }

  input.maxLength = 30;
  input.minLength = 2;
  imprompt.classList.remove("hidden");
}
