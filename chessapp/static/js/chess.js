document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('Board');

function getCookie(name) {
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

const csrftoken = getCookie('csrftoken');
    console.log(gameplay_id, 'GAME IDDDD')

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

    async function fetchGameState(){
    const response = await fetch(`get_game_state/${gameplay_id}`)

    if (!response) {
            console.error('Failed Get Game State!!!', response.status);
            return;
        }

    const data = await response.json()
        return data.game_state
    }




    async function initializeBoard() {
        const gamestate = await fetchGameState();
        console.log(gamestate,'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        if (!gamestate) {
            console.error('GAMESTATE NOT AVAILABLE!!!');
            return;
        }
        const boardData = JSON.parse(JSON.parse(gamestate).board)
        console.log( boardData, 'HELLO');

        let className = "square-white";
        for (let i = 0; i < 8; i++) {
            for (let j = 0; j < 8; j++) {
                const square = document.createElement("div");
                className = (i + j) % 2 === 0 ? "square-white" : "square-green";
                square.classList.add('square', className);
                square.setAttribute("id", `square-${i}-${j}`);
                board.appendChild(square);
                console.log(boardData[i][j], 'HHHHHHHHHHHHHHHHHHHHHHH')
                let piece = boardData[i][j];
                console.log(piece,'HJJHJHJHJHJ')
                if (piece && JSON.parse(piece)['piece']) {
                    piece = JSON.parse(piece);
                    piece = JSON.parse(piece.piece);
                    console.log(piece, 'PPPPPPPPPPPPPPPPPPPP')
                    const color = piece.color;
                    const pieceType = piece.type;
                    console.log(pieceType, 'PIECETYPE')
                    const url = getUrl(color, pieceType);
                    console.log(url, color, 'LLLLLLLLLLLLLLLLLLLLLLLL')
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
        event.dataTransfer.setData("text/plain", event.target.id);
        console.log('DRAG STARTED')
    }

    function handleDragOver(event) {
        event.preventDefault();
    }

    async function handleDrop(event) {
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

        event.preventDefault();
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

    async function movePiece(source, dest) {
    console.log(JSON.stringify({source:source, dest:dest}), 'SOURCE')
    const response = await fetch('/move/', {method:'POST', headers:{'Content-Type':'application/json', 'X-CSRFToken': csrftoken}, body:JSON.stringify({source:source, dest:dest})});
    const data = await response.json();
    console.log(data.status)
    if (data.status === 'success') {
        if (data.check) {
        console.log('INCHECK', data)
        checkAlert(data.checked_king);
        }
        if (data.checkmate) {
        console.log('INCHECKMATE', data)
        checkmateAlert(data.winner);
        }
    return true;
    }
    else {
    return false;
    }
    }
    // async function set_board() {
    //     board.innerHTML = '';
    //     initializeBoard();
    //     console.log('bean');
    // }
    initializeBoard();
});
