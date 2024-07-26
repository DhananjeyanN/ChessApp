document.addEventListener('DOMContentLoaded', () => {
    let socket;
    const board = document.getElementById('Board');
    const setupBoard = document.getElementById('setupBoard');

    function startGame() {
    const response = fetch('/play_game/', {
    method:'POST', headers:{'Content-Type': 'application/json'}});
    const data = response.json();
    console.log(data);
    if (data.status === 'Success') {
        const gameId = data.gameplay_id;
        socket = new WebSocket(`ws://127.0.0.1:8000/ws/game/${gameId}/`);
        socket.onmessage = function (event){
            const data = JSON.parse(event.data);
            handleMove(data.source, data.dest);
        }
    }
    }
    function findPiece(x, y) {
        // Simplified for demonstration
        if (x === 1 || x === 6) return 'pawn';  // Pawns
        else if (x === 0 || x === 7) {
            if (y === 0 || y === 7) return 'rook';  // Rooks
            else if (y === 1 || y === 6) return 'knight';  // Knights
            else if (y === 2 || y === 5) return 'bishop';  // Bishops
            else if (y === 3) return 'queen';  // Queen
            else if (y === 4) return 'king';  // King
        }
        return null;
    }

    function getColor(x) {
        if (x < 2) return 'white';
        else if (x > 5) return 'black';
        return null;
    }

    function getUrl(color, pieceType) {
        if (!pieceType) return '';
        return `/static/images/${color}-${pieceType.toLowerCase()}.png`;
    }

    function initializeBoard() {
        let square_num = 0;
        let className = "square-white";
        for (let i = 0; i < 8; i++) {
            for (let j = 0; j < 8; j++) {
                const square = document.createElement("div");
                className = (i + j) % 2 === 0 ? "square-white" : "square-green";
                square.classList.add('square', className);
                square.setAttribute("id", `square-${i}-${j}`);
                board.appendChild(square);
                square_num++;

                const color = getColor(i);
                const pieceType = findPiece(i, j);
                let url = getUrl(color, pieceType);
//                url = "{% static "+"'"+url+"'"+" %}"
                console.log(url)
                if (pieceType) {
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

//    function makeMove(row, col){
//
//    }


    function handleDragStart(event) {
        event.dataTransfer.setData("text/plain", event.target.id);
    }

    function handleDragOver(event) {
        event.preventDefault();
    }

    function handleDrop(event) {
        console.log(event)
        console.log('EVENT')
        event.preventDefault();
        const id = event.dataTransfer.getData('text/plain');
        const draggableElement = document.getElementById(id);
        let dropTarget = event.target;
        if(!dropTarget.classList.contains('square')) {
            dropTarget = dropTarget.closest('.square');
        }
        if(dropTarget.hasChildNodes()) {
            dropTarget.innerHTML = '';
        }
        dropTarget.appendChild(draggableElement);
    }
    async function movePiece(source,dest) {
        const response = await fetch('/move/', {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken
            },
            body:JSON.stringify({source:source, dest:dest})
        });
        const data = await response.json()
        console.log(data.status)
        if (data.status === 'Success') {
            if (socket) {
                socket.send(JSON.stringify({'source':source,'dest':dest}));
            }
            return true;
        }
        else {
            return false;
        }
    }
    function handleMove(source, dest) {
        const draggableElement = document.getElementById(`piece-${source[0]}-${source[1]}`);
        const dropTarget = document.getElementById(`square-${dest[0]}-${dest[1]}`);
        draggableElement.id = `piece-${dest[0]}-${dest[1]}`;
        if (dropTarget.hasChildNodes()){
            dropTarget.innerHTML = '';
        }
        dropTarget.appendChild(draggableElement);
    }

    setupBoard.addEventListener('click', async () => {
        // Clear existing board to reinitialize
        board.innerHTML = '';
        await startGame();
        initializeBoard();
        console.log('bean');
    });

});
