window.addEventListener('DOMContentLoaded', initiateGUI);

const OPENING_CRAWL =
`
It is a period of civil war.
Rebel spaceships, striking
from a hidden base, have won
their first victory against
the evil Galactic Empire.
<br><br>
During the battle, Rebel
spies managed to steal secret
plans to the Empire's
ultimate weapon, the DEATH
STAR, an armored space
station with enough power to
destroy an entire planet.
<br><br>
Pursued by the Empire's
sinister agents, Princess
Leia races home aboard her
starship, custodian of the
stolen plans that can save
her people and restore
freedom to the galaxy.....
<br><br>
...<br>
...<br>
...<br>
<br>
This is not that story.
`

async function initiateGUI() {
  var input = document.getElementById('input');
  var scenario = document.getElementById('scenario');
  var iprompt = document.getElementById('iprompt');
  var card = document.getElementById('card');
  var skipTextCrawl = false;

  input.value = '';  // clear input textarea
  input.addEventListener('keydown', processEnter);
  await displayScenario(OPENING_CRAWL);
  imprompt.innerHTML = "Enter anything below to continue";
}

async function processEnter(e) {
  if (e.code !== 'Enter') return;

  skipTextCrawl = true;

  e.preventDefault(); // don't allow multi-line input
  if (!input.validity.valid) return; // don't allow empty input (minLength = 2)

  let inputText = input.value;
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
    <br><br>
    ...
    <br><br>
    You should close this tab now.
    `;
    console.error(error)
  });
}

async function displayScenario(text) {
  imprompt.classList.add("hidden");
  input.minLength = 0;
  input.maxLength = 0;

  imprompt.innerHTML = "What do you do?";
  skipTextCrawl = false;

  let len = text.length;

  for(let i = 1; i <= len + 1; i++) {
    if (skipTextCrawl) i = len + 1;
    scenario.innerHTML = text.substring(0, i);
    scenario.scrollIntoView(false); // make bottom of text visible
    await new Promise(resolve => setTimeout(resolve, 8)); // sleep for x ms
  }

  input.maxLength = 30;
  input.minLength = 2;
  imprompt.classList.remove("hidden");
}
