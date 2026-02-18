import { Match4Game, Match4Command } from './match4game.js';
import readlineSync from "readline-sync";

class GamerunnerMatch4 {
    constructor() {
        this.game = new Match4Game();
        this.p1 = 1;
        this.p2 = 2;
        this.curPlayer = this.p1;
        this.commandHisto = [];
        this.terminal = false
    }

    run(verbose = false) {
        this.game.setup();
        this.curPlayer = this.p1;
        if (verbose) this.printState();
        
        while (true) {
            
            console.log(`Human Player ${this.curPlayer}: Input the column you want to put the token`);
            let column = parseInt(readlineSync.question("Enter column: "), 10);
            let command = new Match4Command(column, this.curPlayer);
            while (!this.game.legalMove(command)) {
                console.log("Please input a valid move");
                let column = parseInt(prompt("Enter column:"));
                command = new Match4Command(column, this.curPlayer);
            }

            this.game.applyCommand(command);
            this.commandHisto.push(structuredClone(command));
            this.curPlayer = this.curPlayer === this.p1 ? this.p2 : this.p1;
            if (verbose) this.printState();
            
            if (this.game.isTerminal()) {
                this.terminal = true
                console.log("Game Finished");
                if (this.game._state.winnerPlayer === Match4Game.tieValue) {
                    console.log("Tie !!");
                } else {
                    console.log(`Winner: Player ${this.game._state.winnerPlayer}`);
                }
                break;
            }
        }
    }

    printState() {
        const state = this.game.getState();
        state.board.forEach(row => {
            console.log(row.map(cell => {
                if (cell === 0) return "_";
                if (cell === 1) return "O";
                if (cell === 2) return "X";
                throw new Error("Unknown value for the cell in match4game");
            }).join(" "));
        });
        console.log();
    }
}


export { GamerunnerMatch4 };
