import React, { useState } from "react";
import Sidebar from "../components/sidebar/SideBar";
import Connect4Board from "../components/Connect4Board/Connect4Board";
import "./Main.css";

const Main = () => {
  const [player1, setPlayer1] = useState("Humen");
  const [player2, setPlayer2] = useState("Humen");
  const [playerTypes, setPlayerTypes] = useState({});

  const handlePlayer1Change = (event) => setPlayer1(event.target.value);
  const handlePlayer2Change = (event) => setPlayer2(event.target.value);

  const startGameWithPlayerTypes = (p1, p2) => {
    setPlayerTypes({ 1: p1, 2: p2 });
  };

  return (
    <div className="main-container">
      <Sidebar
        player1={player1}
        player2={player2}
        handlePlayer1Change={handlePlayer1Change}
        handlePlayer2Change={handlePlayer2Change}
        onStartGame={startGameWithPlayerTypes}
      />

      <div className="content-container">
        <h1>Connect 4 Game</h1>
        <h2>Player 1: {player1} | Player 2: {player2}</h2>
        <Connect4Board player1Type={playerTypes[1]} player2Type={playerTypes[2]} />
      </div>
    </div>
  );
};

export default Main;
