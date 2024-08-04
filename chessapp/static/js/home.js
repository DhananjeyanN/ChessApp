document.addEventListener('DOMContentLoaded', () => {
    const joinQueue = document.getElementById('join-queue')
    const csrftoken = getCookie('csrftoken');

        async function joinQ() {
        console.log('JOINED QUEUE');
        const response = await fetch('/join_queue/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        });
        if (!response.ok) {
            console.error('Failed to join!!!', response.status);
            return;
        }
        const data = await response.json();
        console.log(data, 'REsPONSe');
    }

    joinQueue.addEventListener('click', ()=>{

    })
})