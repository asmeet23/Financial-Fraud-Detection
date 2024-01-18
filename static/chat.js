const chat = {
    1: {
        text: 'List your disaster',
        options: [
            {
                text: 'Earthquake',
                next: 2
            },
          {
                text: 'Cyclone',
                next: 7
          },
          {
                text: 'Landslide',
                next: 9
          },
          {
                text: 'Flood',
                next: 8
          },
        ]
    },
    2: { //Earthquake manager
        text: 'Move away from the windows and outside walls, try to cover your head under a strong table.',
        next: 3
    },
    3: {
        text: 'Emergency services have your location details, someone will come help you',
        options: [
            {
                text: "i want to call services",
                next: 4
            },
            {
                text: "Show me area map",
                next: 6
            }
        ]
    },
    4: {
        text: 'Disaster management - 108\n Emergency service - 112 \n Fire - 101 \n N.D.M.A. - 011-24363260',
      next: 5
    },
    5: {
        text: 'Want more help?',
        options: [
            {
                text: "Back to Disaster list",
                next: 1
            },
          {
              text: 'No, thank you',
              next: 10
          }
        ]
    },
    6: {
        text: 'Navigate to your location',
        options: [
            {
                text: "Go to Maps",
                url: "https://maps.google.com/maps?q='+latitude+','+longitude+'&amp;z=15&amp;output=embed"
            }
        ]
    },
  7: { //Cyclone
    text: 'You should remain in shelters until informed by those in charge that you may return home. Any loose and dangling wire from the lamp post should be strictly avoided. People should keep away from disaster areas unless you are required to assist.',
    next : 3  
},
  8: { //Flood
    text: 'Do not enter deep, unknown waters; use a stick to check water depth. Come back home only when officials ask you to do so. Make a family communications plan. Clean and disinfect everything that got wet.',
    next : 3
},
  9: { //Landslide
    text: 'Try and get out of the path of the landslide or mudflow. Run to the nearest high ground in a direction away from the path. If rocks and other debris are approaching, run for the nearest shelter such as a group of trees or a building. If escape is not possible, curl into a tight ball and protect your head.',
    next : 3
},
  10: {
    text: 'You will be saved. Don\'t worry'
  },
};


const bot = function () {

    const peekobot = document.getElementById('peekobot');
    const container = document.getElementById('peekobot-container');
    const inner = document.getElementById('peekobot-inner');
    let restartButton = null;

    const sleep = function (ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    };

    const scrollContainer = function () {
        inner.scrollTop = inner.scrollHeight;
    };

    const insertNewChatItem = function (elem) {
        //container.insertBefore(elem, peekobot);
        peekobot.appendChild(elem);
        scrollContainer();
        //debugger;
        elem.classList.add('activated');
    };

    const printResponse = async function (step) {
        const response = document.createElement('div');
        response.classList.add('chat-response');
        response.innerHTML = step.text;
        insertNewChatItem(response);

        await sleep(1500);

        if (step.options) {
            const choices = document.createElement('div');
            choices.classList.add('choices');
            step.options.forEach(function (option) {
                const button = document.createElement(option.url ? 'a' : 'button');
                button.classList.add('choice');
                button.innerHTML = option.text;
                if (option.url) {
                    button.href = option.url;
                } else {
                    button.dataset.next = option.next;
                }
                choices.appendChild(button);
            });
            insertNewChatItem(choices);
        } else if (step.next) {
            printResponse(chat[step.next]);
        }
    };

    const printChoice = function (choice) {
        const choiceElem = document.createElement('div');
        choiceElem.classList.add('chat-ask');
        choiceElem.innerHTML = choice.innerHTML;
        insertNewChatItem(choiceElem);
    };

    const disableAllChoices = function () {
        const choices = document.querySelectorAll('.choice');
        choices.forEach(function (choice) {
            choice.disabled = 'disabled';
        });
        return;
    };

    const handleChoice = async function (e) {

        if (!e.target.classList.contains('choice') || 'A' === e.target.tagName) {
            // Target isn't a button, but could be a child of a button.
            var button = e.target.closest('#peekobot-container .choice');

            if (button !== null) {
                button.click();
            }

            return;
        }

        e.preventDefault();
        const choice = e.target;

        disableAllChoices();

        printChoice(choice);
        scrollContainer();

        await sleep(1500);

        if (choice.dataset.next) {
            printResponse(chat[choice.dataset.next]);
        }
        // Need to disable buttons here to prevent multiple choices
    };

    const handleRestart = function () {
        startConversation();
    }

    const startConversation = function () {
        printResponse(chat[1]);
    }

    const init = function () {
        container.addEventListener('click', handleChoice);

        restartButton = document.createElement('button');
        restartButton.innerText = "SOS & Restart";
        restartButton.classList.add('restart');
        restartButton.addEventListener('click', handleRestart);

        container.appendChild(restartButton);

        startConversation();
    };

    init();
}

bot();