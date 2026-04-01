let reSendButton = document.getElementById('re-send');
let counterSpanElement = document.getElementById('counter');
const WAIT_TIME_SECONDS = 60;



function timer(seconds)
{
    reSendButton.style.pointerEvents = 'none';
    reSendButton.className = 'btn btn-secondary';
    let counter = seconds;

    let interval = setInterval(() => {
        counterSpanElement.innerText = `(${counter})`;
        counter--;
        if (counter < 0) {
            clearInterval(interval);
            reSendButton.style.pointerEvents = 'all';
            reSendButton.className = 'btn btn-primary';
            counterSpanElement.innerText = '';
            localStorage.removeItem('nextTimeSeconds');
        }
    }, 1000);
}



window.onload = function()
{
    let nextTimeSeconds = localStorage.getItem('nextTimeSeconds');
    if (nextTimeSeconds) {
        let now = Math.floor(Date.now() / 1000)
        let diff = (nextTimeSeconds - now);

        if (diff > 0) {
            timer(diff);
        }
    }
}



reSendButton.closest('form').onsubmit = function()
{
    let now = Math.floor(Date.now() / 1000) + WAIT_TIME_SECONDS;
    localStorage.setItem('nextTimeSeconds', now);

}