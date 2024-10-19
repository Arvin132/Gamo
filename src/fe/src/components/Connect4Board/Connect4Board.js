import React, { useState, useEffect } from "react";
import axiosInstance from "../../utils/axiosConfig";
import "./Connect4Board.css";

const ROWS = 8;
const COLS = 8;
const EMPTY = null;

function Connect4Board({ player1Type, player2Type }) {
  const [board, setBoard] = useState(Array(ROWS).fill(Array(COLS).fill(EMPTY)));
  const [currentPlayer, setCurrentPlayer] = useState(1);
  const [terminal, setTerminal] = useState(false);
  const [Humen, setHumen] = useState('');

  useEffect(() => {
    axiosInstance.get("/connect4/agents")
      .then((response) => {
        setHumen(response.data["humen-agent"]);
        console.log("Humen Agent fetched:", response.data["humen-agent"]);
      })
      .catch((error) => console.error("Error fetching agents list:", error));
  }, []);

  useEffect(() => {
    console.log("Fetching Board State...");
    fetchBoardState();
  }, [currentPlayer]);

  const fetchBoardState = () => {
    axiosInstance.get("/connect4/state")
      .then((response) => {
        console.log("Board State Fetched:", response.data);
        const newBoard = response.data.state.board.map((row) =>
          row.map((cell) => (cell === 1 ? "🔴" : cell === 2 ? "🟡" : EMPTY))
        );
        setBoard(newBoard);
        setCurrentPlayer(response.data.state.current_player);
        setTerminal(response.data.state.terminal);
        if (!response.data.state.terminal) {
          handleTurn();
        }
      })
      .catch((error) => console.error("Error fetching the board:", error));
  };

  const handleTurn = () => {
    const currentPlayerType = currentPlayer === 1 ? player1Type : player2Type;
    console.log(`Current Player ${currentPlayer} Type:`, currentPlayerType);

    if (currentPlayerType === Humen) {
      console.log("Waiting for Human Move.");
    } else {
      console.log("Bot's Turn. Making a move...");
      setTimeout(() => handleAgentMove(), 1000);
    }
  };

  const handleColumnClick = (col) => {
    if (terminal) {
      alert("The game has ended! Start a new game.");
      return;
    }
    const currentPlayerType = currentPlayer === 1 ? player1Type : player2Type;
    if (currentPlayerType === Humen) {
      applyMove(col + 1);
    }
  };

  const applyMove = (column) => {
    axiosInstance.post("/connect4/apply-move", {
      column: column,
      "player-id": currentPlayer,
      "is-bot": false,
    })
      .then(() => fetchBoardState())
      .catch((error) =>
        console.error("Error applying move:", error.response?.data?.message || error.message)
      );
  };

  const handleAgentMove = () => {
    axiosInstance.post("/connect4/apply-move", {
      column: -1,
      "player-id": currentPlayer,
      "is-bot": true,
    })
      .then(() => fetchBoardState())
      .catch((error) =>
        console.error("Error with agent move:", error.response?.data?.message || error.message)
      );
  };

  return (
    <div className="board">
      {board.map((row, rowIndex) =>
        row.map((_, colIndex) => (
          <div className="cell" onClick={() => handleColumnClick(colIndex)} key={`${rowIndex}-${colIndex}`}>
            {board[rowIndex][colIndex]}
          </div>
        ))
      )}
    </div>
  );
}

export default Connect4Board;
