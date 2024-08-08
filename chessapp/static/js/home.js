document.addEventListener('DOMContentLoaded', () => {
    const joinGame = document.getElementById('join-game')
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
        return cookieValue;
    }
    const csrftoken = getCookies('csrftoken');

        async function playGame() {
        console.log('STARTING GAME');
        const response = await fetch('/join_game/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        });
        if (!response.ok) {
            console.error('Failed to start Game!!!', response.status);
            return;
        }
        const data = await response.json();
        console.log(data, 'REsPONSe');
        const gameplay_id = data.gameplay_id
            if (data.status === 'joined_game') {
                window.location.href = `/game_page/${gameplay_id}/`
            }
            else if (data.status === 'initialized_game') {
                waitForOponent(gameplay_id)
            }
    }
    async function waitForOponent(gameplay_id){
            const interval = setInterval(async()=>{
                const response = await fetch('/check_status/', {method:'POST', headers:{'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}, body:JSON.stringify({gameplay_id:gameplay_id})});

                if (!response) {
                    console.error('Failed To Check Game Status!!!', response.status);
                    return;
                }
                const data = await response.json();
                if (data.is_ready){
                    clearInterval(interval);
                    window.location.href = `/game_page/${gameplay_id}/`
                }
                },1000);
            }



    joinGame.addEventListener('click', ()=>{
        console.log('TRIGGER')
    playGame();
    });
});