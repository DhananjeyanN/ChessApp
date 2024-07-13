document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('Board');
    const setupBoard = document.getElementById('setupBoard');
    console.log('HELLLLLLLLLLOOOOOOOO')

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
    async function startGame() {
        console.log('GAME STARTED');
        const response = await fetch('/start_game/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        });
        if (!response.ok) {
            console.error('Failed to start the game', response.status);
            return;
        }
        const data = await response.json();
        console.log(data, 'REsPONSe');
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

    function handleDragStart(event) {
        event.dataTransfer.setData("text/plain", event.target.id);
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
        console.log(move_successful)

        if (!move_successful) {
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
    if (data.status === 'Success') {
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

    setupBoard.addEventListener('click', async () => {
        // Clear existing board to reinitialize
        board.innerHTML = '';
        await startGame();
        initializeBoard();
        console.log('bean');
    });

});
