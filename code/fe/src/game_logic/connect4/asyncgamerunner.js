import { Match4Game, Match4Command } from "./match4game.js";

class AsyncGamerunnerMatch4 {
    constructor() {
        this.game = new Match4Game();
        this.p1 = 1
        this.p2 = 2
        this.curPlayer = this.p1;
        this.commandHisto = [];
        this.terminal = false
    }

    /**
     * Start a fresh new game
     * 
     * @returns {(number, number)} - returns the ids for player 1 and player 2
     */
    start() {
        this.game.setup();
        return (this.p1, this.p2)
    }

    /**
     * Apply a move to the game
     * @param {number} move - Column to place the token (1-based index)
     * @param {number} playerId - ID of the player making the move
     */
    applyMove(move, playerId) {
        if (playerId != this.curPlayer) { 
            console.error(" AsynGameRunner: playerId for the given value is bad!!!!")
            return;
        }
        let command = new Match4Command();
        command.column = move - 1; // Convert to 0-based index
        command.playerId = playerId;
        this.game.applyCommand(command);
        this.commandHisto.push(structuredClone(command));
        this.curPlayer = this.curPlayer === this.p1 ? this.p2 : this.p1;
        this.terminal = this.game.isTerminal()
    }

    getBoard() {
        return this.game._state.board
    }

    getTerminal() {
        return this.game._state
    }

    /**
     * Convert game state to a JSON-compatible object
     */
    toDict() {
        return {
            state: this.game.toDict(),
            moves: this.commandHisto.map(move => move.toDict())
        };
    }

    /**
     * Restore game state from a JSON object
     * @param {object} given - The object containing game state and moves
     */
    fromDict(given) {
        this.game = Match4Game.fromDict(given.state);
        this.commandHisto = given.moves.map(move => Match4Command.fromDict(move));
    }
}

// ✅ Export class for use in Node.js
export { AsyncGamerunnerMatch4 };
