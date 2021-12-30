const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_IMG = "chatbot.png";
const PERSON_IMG = "human.png";
const BOT_NAME = "Bob";
const PERSON_NAME = "You";

function get(selector, root = document) {
    return root.querySelector(selector);
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
}

function appendMessage(name, img, side, text) {
    const msgHTML = `
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

let msgList = [
    "How old are you?",
    "Now measure your temperature, tell me the interval.",
    "Are you having cough?",
    "Are you having a sore throat?",
    "Are you having a shortness of breath?",
    "Are you having a headache?",
    "Are you having runny nose or nasal congestion?"
];

let reply = [];
let cnt = 0;
let advice = '';
msgerForm.addEventListener("submit", event => {
    event.preventDefault();
    
    const usermsg = msgerInput.value;
    if(usermsg.toLowerCase()==='yes' || parseFloat(usermsg)>37) cnt++;
    reply.push(usermsg);
    if(!usermsg) return;
    appendMessage(PERSON_NAME, PERSON_IMG, "right", usermsg);
    msgerInput.value = "";

    let botmsg = msgList.shift();
    setTimeout(() => {
        if(botmsg!=undefined) appendMessage(BOT_NAME, BOT_IMG, "left", botmsg);
        else
        {
            if(cnt>2) advice = "You have many symptoms of Covid 19. You should immediately go to the nearest hospital or medical facility to take a test for Covid-19."
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
            
            let conclude = `
            <p>If you want to check again, click here: <a href = "file:///D:/Study/University/Semester%205/Artificial%20intelligence/Project/healthcheck/healthcheck.html?" target = "_self">Covid check</a></p>
            <p>If you want to ask me some questions or information related to Covid-19, click here: <a href = "http://127.0.0.1:5000/" target = "_self">Covid information</a></p>`;
            appendMessage(BOT_NAME, BOT_IMG, "left", conclude);
        }
    }, 500);
});