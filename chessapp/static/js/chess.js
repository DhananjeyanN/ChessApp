document.addEventListener('DOMContentLoaded', () => {

    const board = document.getElementById('Board');
    const gameplay_id = document.getElementById('gameplay_id').value;
    const is_white = document.getElementById('is_white').value;
    var boardData = null;
    const pollInterval = 1000; // Poll every 3 seconds
    let lastGameState = null;

        function getColor(x) {
        if (x < 2) return 'white';
        else if (x > 5) return 'black';
        return null;
    }

    function getUrl(color, pieceType) {
        if (!pieceType) return '';
        return `/static/images/${color}-${pieceType.toLowerCase()}.png`;
    }
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
//    dd
    async function pollGameState() {
        const gamestate = await fetchGameState();
        if (gamestate && gamestate !== lastGameState) {
            lastGameState = gamestate;
            updateBoard(JSON.parse(JSON.parse(gamestate).board));
        } else if (!gamestate) {
            console.error('Game state not available!');
        }
    }

    function updateBoard(boardData) {
        board.innerHTML = ''; // Clear the current board
        console.log(boardData, 'Bean')
        let className = "square-white";
        // Rebuild the board based on the new state
        for (let i = 0; i < 8; i++) {
            for (let j = 0; j < 8; j++) {
                const square = document.createElement("div");
                className = (i + j) % 2 === 0 ? "square-white" : "square-green";
                square.classList.add('square', className);
                square.setAttribute("id", `square-${i}-${j}`);
                board.appendChild(square);
                let piece = boardData[i][j];
                if (piece && JSON.parse(piece)['piece']) {
                    piece = JSON.parse(piece);
                    piece = JSON.parse(piece.piece);
                    const color = piece.color;
                    const pieceType = piece.type;
                    const url = getUrl(color, pieceType);
                    let image = document.createElement('img');
                    image.classList.add('piece');
                    image.setAttribute('id', `${pieceType}-${color}-${i}-${j}`);
                    image.setAttribute('src', url);
                    image.setAttribute('draggable', 'true');
                    square.appendChild(image);
                }
            }
        }

        // Reattach event listeners if necessary
        attachDragListeners();
    }

    async function initializeBoard() {
        const gamestate = await fetchGameState();

        if (!gamestate) {
            console.error('GAMESTATE NOT AVAILABLE!!!');
            return;
        }
        boardData = JSON.parse(JSON.parse(gamestate).board);
        let className = "square-white";
        for (let i = 0; i < 8; i++) {
            for (let j = 0; j < 8; j++) {
                const square = document.createElement("div");
                className = (i + j) % 2 === 0 ? "square-white" : "square-green";
                square.classList.add('square', className);
                square.setAttribute("id", `square-${i}-${j}`);
                board.appendChild(square);
                let piece = boardData[i][j];
                if (piece && JSON.parse(piece)['piece']) {
                    piece = JSON.parse(piece);
                    piece = JSON.parse(piece.piece);
                    const color = piece.color;
                    const pieceType = piece.type;
                    const url = getUrl(color, pieceType);
                    let image = document.createElement('img');
                    image.classList.add('piece');
                    image.setAttribute('id', `${pieceType}-${color}-${i}-${j}`);
                    image.setAttribute('src', url);
                    image.setAttribute('draggable', 'true');
                    square.appendChild(image);
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
        event.preventDefault()
        let source = event.dataTransfer.getData('text/plain').split('-')
        let dest = event.target.id.split('-')
        let source1 = source
        source = source.slice(2,4).map(Number)
        if (dest[0] == 'square') {
        trueDest = source1.slice(0,2).join('-') + '-' + dest.slice(1,3).join('-')
        dest = dest.slice(1,3).map(Number)
        }
        else {
        trueDest = source1.slice(0,2).join('-') + '-' + dest.slice(2,4).join('-')
        dest = dest.slice(2,4).map(Number)
        }
        console.log(source, dest)

        const id = event.dataTransfer.getData('text/plain');
        const draggableElement = document.getElementById(id);
        let dropTarget = event.target;
        if(!dropTarget.classList.contains('square')) {
            dropTarget = dropTarget.closest('.square');
        }
        const move_successful = await movePiece(source, dest)
        console.log(move_successful, '24')

        if (!move_successful) {
            console.log('MOVE NOT SUCCESSFUL')
        }
        else {
        console.log('Draggable Element', draggableElement)
        draggableElement.id = trueDest
        if(dropTarget.hasChildNodes()) {
            dropTarget.innerHTML = '';
        }
        dropTarget.appendChild(draggableElement);
        }
    }

    function checkmateAlert(winner) {
    Swal.fire({
    title:'Checkmate!!!',
    text: `${winner} has won the game!!!`,
    icon: 'success',
    confirmButtonText:'Ok'
    });
}

function checkAlert(checkedKing) {
    Swal.fire({
    title:'Check',
    text: `${checkedKing} is-in-check`,
    icon: 'warning',
    confirmButtonText:'Ok'
    });
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
                console.log('DATTTTTTTA', data);
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

    // Start polling the server for game state updates
    setInterval(pollGameState, pollInterval);

    // Initialize the board when the page loads
    initializeBoard();
});