document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('Board');
    const game_id = gameplay_id;
    console.log(gameplay_id)
    console.log(game_id)
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/chess/${game_id}/`);
    console.log(`WebSocket URL: ws://${window.location.host}/ws/chess/${game_id}/`);

    socket.onmessage = function(e) {
        console.log('MESSAGE')
        const data = JSON.parse(e.data);
        const source = data['source'];
        const dest = data['dest'];

        // Update the board
        const piece = document.getElementById(`piece-${source.join('-')}`);
        if (piece) {
            piece.id = `piece-${dest.join('-')}`;
            const targetSquare = document.getElementById(`square-${dest.join('-')}`);
            const sourceSquare = document.getElementById(`square-${source.join('-')}`);
            if (targetSquare) {
                if (targetSquare.hasChildNodes()) {
                    targetSquare.innerHTML = '';
                }
                targetSquare.appendChild(piece);
                sourceSquare.innerHTML = '';
            }
        }
    };

    socket.onclose = function(e) {
        console.error('Socket closed unexpectedly');
    };

    // Function to handle piece movement
    async function handleDrop(event) {
        event.preventDefault();
        let source = event.dataTransfer.getData('text/plain').split('-').slice(1, 3).map(Number);
        let dest = event.target.id.split('-').slice(1, 3).map(Number);

        if (dest.length !== 2) {
            dest = event.target.closest('.square').id.split('-').slice(1, 3).map(Number);
        }

        const piece = document.getElementById(`piece-${source.join('-')}`);
        const targetSquare = document.getElementById(`square-${dest.join('-')}`);

        if (piece && targetSquare) {
            targetSquare.innerHTML = '';
            targetSquare.appendChild(piece);
            piece.id = `piece-${dest.join('-')}`;
            const sourceSquare = document.getElementById(`square-${source.join('-')}`);
            sourceSquare.innerHTML = '';

            // Send move to WebSocket server
            socket.send(JSON.stringify({
                'source': source,
                'dest': dest
            }));
        }
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
        event.dataTransfer.setData("text/plain", event.target.id);
    }

    function handleDragOver(event) {
        event.preventDefault();
    }

    async function initializeBoard() {

        console.log(game_id)
        const response = await fetch(`get_game_state/${game_id}`);
        if (!response.ok) {
            console.error('Failed to get game state!', response.status);
            return;
        }

        const data = await response.json();
        const boardData = JSON.parse(JSON.parse(data.game_state).board);
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

    initializeBoard();
});