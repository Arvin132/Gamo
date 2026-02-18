import structuredClone from '@ungap/structured-clone';

class Match4State {
    constructor() {
        this.board = Array.from({ length: 8 }, () => Array(8).fill(0));
        this.terminal = false;
        this.currentPlayer = 1;
        this.winnerPlayer = -10; // dummy values
    }

    equals(other) {
        return JSON.stringify(this.board) === JSON.stringify(other.board) &&
               this.terminal === other.terminal &&
               this.currentPlayer === other.currentPlayer &&
               this.winnerPlayer === other.winnerPlayer;
    }
}


class Match4Command {
    constructor(column = -10, playerId = 10) {
        this.column = column;
        this.playerId = playerId;
    }

    toDict() {
        return { column: this.column, playerId: this.playerId };
    }

    static fromDict(given) {
        return new Match4Command(given.column, given.playerId);
    }
}

class Match4Game {
    static tieValue = 3;
    static numCols = 8;
    static numRows = 8;

    constructor() {
        this.setup();
    }

    setup() {
        this._state = new Match4State();
    }

    getState() {
        return structuredClone(this._state);
    }

    applyCommand(command) {
        if (!(command instanceof Match4Command)) throw new TypeError("Expected a Match4Command instance");
        if (command.playerId !== this._state.currentPlayer) 
            throw new Error(`Expected command for player ${this._state.currentPlayer}, got ${command.playerId}`);
        if (!this.legalMove(command)) throw new Error("Illegal move!");
        

        let row = Match4Game.numRows - 1;
        while (this._state.board[row][command.column] !== 0) {
            row--;
            if (row < 0) {
                throw new Error(`Invalid row access: ${row}`);
            }
        }
        this._state.board[row][command.column] = command.playerId;
        this._state.currentPlayer = this._state.currentPlayer === 1 ? 2 : 1;
        this.checkForTerminal();
        return true;
    }

    checkForTerminal() {
        return Match4Game.checkForTerminalForState(this._state);
    }

    static checkForTerminalForState(state) {
        for (let i = 0; i < Match4Game.numCols; i++) {
            for (let j = 0; j < Match4Game.numRows; j++) {
                let winner = state.board[i][j];
                if (winner === 0) continue;
                for (let mov of [[0, 1], [1, 0], [-1, -1], [-1, 1]]) {
                    for (let m = 0; m < 4; m++) {
                        let pos = [i + mov[0] * m, j + mov[1] * m];
                        if (pos[0] >= Match4Game.numCols || pos[1] >= Match4Game.numRows || pos[0] < 0 || pos[1] < 0)
                            break;
                        if (state.board[pos[0]][pos[1]] !== winner)
                            break;
                        if (m === 3) {
                            state.winnerPlayer = winner;
                            state.terminal = true;
                            return winner;
                        }
                    }
                }
            }
        }

        for (let i = 0; i < Match4Game.numCols; i++) {
            if (state.board[0][i] === 0) break;
            if (i === 7) {
                state.terminal = true;
                state.winnerPlayer = Match4Game.tieValue;
                return Match4Game.tieValue;
            }
        }
        return 0;
    }

    legalMove(command) {
        return Match4Game.legalMoveState(command, this._state);
    }

    static legalMoveState(command, state) {
        try {
            return state.board[0][command.column] === 0;
        } catch {
            return false;
        }
    }

    isTerminal() {
        return this._state.terminal;
    }

    toDict() {
        return {
            board: this._state.board,
            terminal: this._state.terminal,
            currentPlayer: this._state.currentPlayer,
            winnerPlayer: this._state.winnerPlayer,
        };
    }

    static fromDict(given) {
        let game = new Match4Game();
        game._state.board = given.board;
        game._state.terminal = given.terminal;
        game._state.currentPlayer = given.currentPlayer;
        game._state.winnerPlayer = given.winnerPlayer;
        return game;
    }

    toJson() {
        return JSON.stringify(this.toDict());
    }

    
    fromJson(jsonStr) {
        let stateDict = JSON.parse(jsonStr);
        this._state.board = stateDict.board;
        this._state.terminal = stateDict.terminal;
        this._state.currentPlayer = stateDict.currentPlayer;
        this._state.winnerPlayer = stateDict.winnerPlayer;
    }
}

export { Match4Game, Match4State, Match4Command };