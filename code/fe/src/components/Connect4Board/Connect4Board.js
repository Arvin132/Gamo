import React, { useState, useEffect } from "react";
import axiosInstance from "../../utils/axiosConfig";
import "./Connect4Board.css";

const ROWS = 8;
const COLS = 8;
const EMPTY = null;

function Connect4Board({ player1Type, player2Type }) {
  const [board, setBoard] = useState(Array(ROWS).fill(Array(COLS).fill(EMPTY)));
  const [currentPlayer, setCurrentPlayer] = useState(1); // 1 = 🔴, 2 = 🟡
  const [terminal, setTerminal] = useState(false); // Track if the game has ended
  const [Humen, setHuman] = useState('');

  useEffect(() => {
    axiosInstance.get("/connect4/agents")
      .then((response) => {
        setHuman(response.data["humen-agent"]);
      })
      .catch((error) => {
        console.error("Error fetching agents list:", error);
      });
  }, []);


  useEffect(() => {
    fetchBoardState();
    if (terminal) {
      alert("The game has ended! Start a new game.");
      return;
    }
  }, [currentPlayer]);

  const fetchBoardState = () => {
    axiosInstance.get(`/connect4/state`)
      .then((response) => {
        const newBoard = response.data.state.board.map((row) =>
          row.map((cell) => (cell === 1 ? "🔴" : cell === 2 ? "🟡" : EMPTY))
        );
        setBoard(newBoard);
        setCurrentPlayer(response.data.state.current_player);
        setTerminal(response.data.state.terminal);
      })
      .catch((error) => console.error("Error fetching the board:", error));
  };

  const handleColumnClick = (col) => {
    const currentPlayerType = currentPlayer === 1 ? player1Type : player2Type;

    if (currentPlayerType === Humen) {
      applyMove(col + 1);
    }
    else {
      setTimeout(() => handleAgentMove(), 1000);
    }
  };

  const applyMove = (column) => {
    const playerId = currentPlayer;

    axiosInstance.post("/connect4/apply-move", {
        column: column,
        "player-id": playerId,
        "is-bot": false,
      })
      .then(() => {
        fetchBoardState();
        const nextPlayerType = currentPlayer === 1 ? player2Type : player1Type;
        if (nextPlayerType !== Humen) {
          setTimeout(() => handleAgentMove(), 1000);
        }
      })
      .catch((error) => alert("Error applying move: " + error.response.data.message));
  };

  const handleAgentMove = () => {
    const playerId = currentPlayer;

    axiosInstance.post("/connect4/apply-move", {
        column: 1, // Backend determines bot's move
        "player-id": playerId,
        "is-bot": true,
      })
      .then(() => {
        fetchBoardState(); // Update board state after bot move

        const nextPlayerType = currentPlayer === 1 ? player2Type : player1Type;
        if (nextPlayerType !== Humen) {
          setTimeout(() => handleAgentMove(), 1000); // Continue bot moves if needed
        }
      })
      .catch((error) => alert("Error with agent move: " + error.response.data.message));
  };

  const renderCell = (row, col) => (
    <div className="cell" onClick={() => handleColumnClick(col)} key={`${row}-${col}`}>
      {board[row][col]}
    </div>
  );

  return (
    <div className="board">
      {board.map((row, rowIndex) =>
        row.map((_, colIndex) => renderCell(rowIndex, colIndex))
      )}
    </div>
  );
}

export default Connect4Board;
