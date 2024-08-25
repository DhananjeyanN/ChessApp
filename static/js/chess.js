document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('Board');
    const gameplay_id = gameplay_id;
    const is_white = is_white;
    const csrftoken = getCookie('csrftoken');
    let lastGameState = null;
    const pollInterval = 3000;

    console.log('Gameplay ID:', gameplay_id);  // Check this output in the console
    console.log('Is White:', is_white);

    async function fetchGameState() {
        try {
            const url = `/game_page/get_game_state/${gameplay_id}`;
            console.log('Fetching game state from URL:', url);
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Failed to get game state: ${response.status}`);
            }
            const data = await response.json();
            return data.game_state;
        } catch (error) {
            console.error('Failed to fetch game state:', error);
        }
    }

    async function pollGameState() {
        const gamestate = await fetchGameState();
        if (!gamestate) {
            console.error('Game state not available!');
            return;
        }

        if (gamestate !== lastGameState) {
            lastGameState = gamestate;
            updateBoard(JSON.parse(gamestate));
        }
    }

    function updateBoard(boardData) {
        board.innerHTML = '';
        for (let i = 0; i < 8; i++) {
            for (let j = 0; j < 8; j++) {
                const square = document.createElement('div');
                const className = (i + j) % 2 === 0 ? 'square-white' : 'square-green';
                square.classList.add('square', className);
                square.setAttribute('id', `square-${i}-${j}`);
                board.appendChild(square);

                const piece = boardData[i][j];
                if (piece && piece.piece) {
                    const img = document.createElement('img');
                    img.classList.add('piece');
                    img.setAttribute('id', `piece-${piece.piece.type}-${piece.piece.color}-${i}-${j}`);
                    img.setAttribute('src', `/static/images/${piece.piece.color}-${piece.piece.type}.png`);
                    img.setAttribute('draggable', 'true');
                    square.appendChild(img);
                }
            }
        }

        attachDragListeners();
    }

    function attachDragListeners() {
        const pieces = document.querySelectorAll('.piece');
        pieces.forEach(piece => {
            piece.addEventListener('dragstart', handleDragStart);
        });

        const squares = document.querySelectorAll('.square');
        squares.forEach(square => {
            square.addEventListener('dragover', handleDragOver);
            square.addEventListener('drop', handleDrop);
        });
    }

    function handleDragStart(event) {
        event.dataTransfer.setData('text/plain', event.target.id);
        console.log('Drag started');
    }

    function handleDragOver(event) {
        event.preventDefault();
    }

    async function handleDrop(event) {
        event.preventDefault();
        let source = event.dataTransfer.getData('text/plain').split('-').slice(2, 4).map(Number);
        let dest = event.target.id.split('-').slice(1, 3).map(Number);

        const id = event.dataTransfer.getData('text/plain');
        const draggableElement = document.getElementById(id);
        let dropTarget = event.target;

        if (!dropTarget.classList.contains('square')) {
            dropTarget = dropTarget.closest('.square');
        }

        const move_successful = await movePiece(source, dest);

        if (!move_successful) {
            console.log('Move not successful');
        } else {
            console.log('Move successful');
            draggableElement.id = `piece-${id.split('-')[1]}-${id.split('-')[2]}-${dest.join('-')}`;
            if (dropTarget.hasChildNodes()) {
                dropTarget.innerHTML = '';
            }
            dropTarget.appendChild(draggableElement);
        }
    }

    async function movePiece(source, dest) {
        try {
            const response = await fetch('/move/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                body: JSON.stringify({ source, dest, is_white })
            });

            const data = await response.json();
            if (data.status === 'success') {
                if (data.check) {
                    checkAlert(data.checked_king);
                }
                if (data.checkmate) {
                    checkmateAlert(data.winner);
                }
                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.error('Failed to move piece:', error);
            return false;
        }
    }

    setInterval(pollGameState, pollInterval);
    initializeBoard();
});