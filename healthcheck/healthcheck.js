// speech to text part
var speechRecognition = window.speechRecognition || window.webkitSpeechRecognition;
var recognition = new speechRecognition();
var content = '';
var textbox = $("#textInput");
recognition.continuous = true;

recognition.onresult = function(event){
    var current = event.resultIndex;
    var transcript = event.results[current][0].transcript;
    content +=transcript;
    textbox.val(content);
};

let cnt = 0;
$("#start-btn").click(function (event){
    if(cnt%2==0) 
    {
        $(".microphone-ico").css('color', 'red');
        if(content.length) {
            content +='';
        }
        recognition.start();
        cnt++;
    }
    else
    {
        $(".microphone-ico").css('color', 'black');
        content = '';
        recognition.stop();
        cnt++;
    }
});

textbox.on('input', function(){
    content = $(this).val();
});

function get(selector, root = document) {
    return root.querySelector(selector);
}

const msgerForm = get(".msger-inputarea"); //
const msgerInput = get(".msger-input");    // get element by class
const msgerChat = get(".msger-chat");      //

const BOT_IMG = "../static/chatbot.png";  // chatbot avatar
const PERSON_IMG = "../static/human.png"; // human avatar
const BOT_NAME = "Bob";
const PERSON_NAME = "You";

function formatDate(date) { // get the real time
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
}

function appendMessage(name, img, side, text) { // make the message box
    const msgHTML = // template
    `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text">${text}</div>
      </div>
    </div>
    `;
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}

var msgList = [ // list of chatbot's questions
    "How old are you?",
    "Now measure your temperature, tell me the interval.",
    "Are you having cough?",
    "Are you having a sore throat?",
    "Are you having a shortness of breath?",
    "Are you having a headache?",
    "Are you having runny nose or nasal congestion?"
];

var reply = []; // queue to store user's answers
let cntSymptoms = 0; // count the number of symptoms user has
let advice = ''; // chatbot's advice to user
msgerForm.addEventListener("submit", event => { // event each time user enter a message
    event.preventDefault();
    
    let usermsg = msgerInput.value; // the message user enters
    appendMessage(PERSON_NAME, PERSON_IMG, "right", usermsg);
    if(usermsg.toLowerCase().includes("yes")) 
    {
        usermsg = "Yes";
        cntSymptoms++;
    }
    else if(usermsg.toLowerCase().includes("no")) usermsg = "No";
    else if(parseFloat(usermsg)>37) cntSymptoms++;
    reply.push(usermsg); // push the user's message into queue
    if(!usermsg) return;
    msgerInput.value = "";

    let botmsg = msgList.shift(); // chatbot will ask in top-bottom order
    setTimeout(() => {
        if(botmsg!=undefined) appendMessage(BOT_NAME, BOT_IMG, "left", botmsg); 
        else // when chatbot already asked all questions
        {
            if(cntSymptoms>2) advice = "You have many symptoms of Covid 19. You should immediately go to the nearest hospital or medical facility to take a test for Covid-19."
            else advice = "You have no obvious symptoms related to Covid-19 😄. You should exercise regularly, avoid crowded gatherings and update the your health status with me daily."
            let review = `
            <p>Here are the details you have entered. Please review:</p>
            <p>Close contact with infected person: ${reply[0]}</p>
            <p>Age: ${reply[1]}</p>
            <p>Temperature: ${reply[2]}</p>
            <p>Having cough: ${reply[3]}</p>
            <p>Having a sore throat: ${reply[4]}</p>
            <p>Shortness of breath: ${reply[5]}</p>
            <p>Having headache: ${reply[6]}</p>
            <p>Runny nose or nasal congestion: ${reply[7]}</p>
            `;
            appendMessage(BOT_NAME, BOT_IMG, "left", review);
            appendMessage(BOT_NAME, BOT_IMG, "left", advice);
            // final bot's message
            let conclude = `
            <p>If you want to check again, click here: <a href = "file:///D:/Study/University/Semester%205/Artificial%20intelligence/Project/healthcheck/healthcheck.html?" target = "_self">Covid check</a></p>
            <p>If you want to ask me some questions or information related to Covid-19, click here: <a href = "http://127.0.0.1:5000/" target = "_self">Covid information</a></p>`;
            appendMessage(BOT_NAME, BOT_IMG, "left", conclude);
        }
    }, 800);
});
