import React, { useState, useEffect } from "react";
import axiosInstance from "../utils/axiosConfig";
import "./Connect4Board.css";

const ROWS = 8;
const COLS = 8;
const EMPTY = null;

function Connect4Board() {
  const [board, setBoard] = useState(Array(ROWS).fill(Array(COLS).fill(EMPTY)));
  const [currentPlayer, setCurrentPlayer] = useState("🔴");

  useEffect(() => {
    axiosInstance.get(`/get-board`)
      .then((response) => {
        const newBoard = response.data.board.map(row =>
          row.map(cell => (cell === 1 ? "🔴" : EMPTY))
        );
        setBoard(newBoard);
      })
      .catch((error) => {
        console.error("Error fetching the board:", error);
      });
  }, []);

  const handleColumnClick = (col) => {
    const newBoard = JSON.parse(JSON.stringify(board));

    for (let row = ROWS - 1; row >= 0; row--) {
      if (newBoard[row][col] === EMPTY) {
        newBoard[row][col] = currentPlayer;
        setBoard(newBoard);
        setCurrentPlayer(currentPlayer === "🔴" ? "🟡" : "🔴");
        break;
      }
    }
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
