document.addEventListener('DOMContentLoaded', () => {
    const joinGame = document.getElementById('join-game')
    const leaveGame = document.getElementById('leave-game')
    const prevGame = document.getElementById('prev-game')
    const quitGame = document.getElementById('quit-game')
    const message = document.getElementById('WFO')

    function getCookies(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;}

    const csrftoken = getCookies('csrftoken');

    getStatus()
    async function getStatus(){
        const response = await fetch('/user_game_state/', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken,}});
        if (!response.ok) {
            console.error('Failed To Get Status!!!', response.status);
            return;
        }

        const data = await response.json();
        console.log(data, 'REsPONSe');
        const gameplay_id = data.gameplay_id
        console.log(gameplay_id)
        if (data.status === 'no_game') {
            joinGame.style.display = 'inline-block';
        }
        else if (data.status === 'game_in_progess') {
            prevGame.style.display = 'inline-block';
            quitGame.style.display = 'inline-block';
        }
        else if (data.status === 'loading') {
            leaveGame.style.display = 'inline-block'
            message.style.display = 'block'
            waitForOpponent(gameplay_id)
        }
    }

    async function playGame() {
        console.log('STARTING GAME');
        const response = await fetch('/join_game/', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken,}});
        if (!response.ok) {
            console.error('Failed to start Game!!!', response.status);
            return;
        }
        const data = await response.json();
        console.log(data, 'REsPONSe');
        console.log(data.status)
        const gameplay_id = data.gameplay_id
        if (data.status === 'joined_game') {
            window.location.href = `/game_page/${gameplay_id}`
        }
        else if (data.status === 'initialized_game') {
            waitForOpponent(gameplay_id)
            joinGame.style.display = 'none'
            leaveGame.style.display = 'inline-block'
            message.style.display = 'block'

        }
        else if (data.status === 'no_game_found') {
            console.log('NO GAME FOUND FOR BLACK')
        }
    }

    async function waitForOpponent(gameplay_id){
        const interval = setInterval(async()=>{
            const response = await fetch('/check_status/', {method:'POST', headers:{'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}, body:JSON.stringify({gameplay_id:gameplay_id})});
            if (!response) {
                console.error('Failed To Check Game Status!!!', response.status);
                return;
            }
            const data = await response.json();
            if (data.is_ready){
                clearInterval(interval);
                window.location.href = `/game_page/${gameplay_id}`
            }
            },1000);
        }



    async function openGame() {
        const response = await fetch('/user_game_state/', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken,}});
        if (!response.ok) {
            console.error('Failed to start Game!!!', response.status);
            return;
        }
        const data = await response.json();
        console.log(data, 'REsPONSe');
        const gameplay_id = data.gameplay_id
        window.location.href = `/game_page/${gameplay_id}`
    }


    async function leaveQ(){
        console.log('LEAVING GAME');
        const response = await fetch('/leave_queue/', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken,}});
        if (!response.ok) {
            console.error('Failed To Delete!!!', response.status);
            return;
        }
        leaveGame.style.display = 'none'
        joinGame.style.display = 'inline-block'
    }

    async function quitG(){
        console.log('QUITING GAME');
        const response = await fetch('/close_game/', {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken,}});
        if (!response.ok) {
            console.error('Failed To Delete!!!', response.status);
            return;
        }
        prevGame.style.display = 'none'
        quitGame.style.display = 'none'
        joinGame.style.display = 'inline-block'
    }

    joinGame.addEventListener('click', ()=>{
        console.log('JOIN')
    playGame();
    });

    leaveGame.addEventListener('click', ()=>{
        console.log('LEAVE')
    leaveQ();
    message.style.display = 'none'
    });

    prevGame.addEventListener('click', ()=>{
        console.log('PREV')
    openGame();
    });

    quitGame.addEventListener('click', ()=>{
        console.log('QUIT')
    quitG();
    });

    function statusAlert() {
    console.log('ALERT!!!')
    Swal.fire({
    title:'Waiting For Opponent',
    text: 'Game is Loading',
    icon: 'warning',
    confirmButtonText:'Ok'
    });
}
});