document.addEventListener('DOMContentLoaded', () => {
    const joinQueue = document.getElementById('join-game')
    const csrftoken = getCookie('csrftoken');

        async function joinQ() {
        console.log('JOINED QUEUE');
        const response = await fetch('/join_queue/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'play_state':'false'
            }
        });
        if (!response.ok) {
            console.error('Failed to join!!!', response.status);
            return;
        }
        const data = await response.json();
        console.log(data, 'REsPONSe');
    }

    async function checkState(){
            const response = await fetch('/join_queue/', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken, 'play_state':'true'}});

            if (!response.ok) {
                console.error('Failed to join!!!', response.status);
                return;
            }
            const data = await response.json();

    }

    joinQueue.addEventListener('click', ()=>{

        setInterval(joinQ, 1000);

    });
});