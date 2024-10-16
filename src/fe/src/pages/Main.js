import React, { useState } from "react";
import Sidebar from "../components/sidebar/SideBar";
import Connect4Board from "../components/Connect4Board/Connect4Board";
import "./Main.css";

const Main = () => {
  const [player1, setPlayer1] = useState("Humen");
  const [player2, setPlayer2] = useState("Humen");

  const handlePlayer1Change = (event) => setPlayer1(event.target.value);
  const handlePlayer2Change = (event) => setPlayer2(event.target.value);

  return (
    <div className="main-container">
      <Sidebar
        player1={player1}
        player2={player2}
        handlePlayer1Change={handlePlayer1Change}
        handlePlayer2Change={handlePlayer2Change}
      />

      <div className="content-container">
        <h1>Connect 4 Game</h1>
        <h2>Player 1: {player1} | Player 2: {player2}</h2>
        <Connect4Board player1Type={player1} player2Type={player2} />
      </div>
    </div>
  );
};

export default Main;
