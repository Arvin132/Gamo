import React, { useEffect, useState } from "react";
import axiosInstance from "../../utils/axiosConfig";
import { Person, SmartToyOutlined } from "@mui/icons-material";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import "./SideBar.css";

const Sidebar = ({ player1, player2, handlePlayer1Change, handlePlayer2Change }) => {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    axiosInstance.get("/connect4/agents")
      .then((response) => {
        setAgents(response.data.agents);
      })
      .catch((error) => {
        console.error("Error fetching agents list:", error);
      });
  }, []);

  const getIcon = (player) => (player === "Humen" ? <Person /> : <SmartToyOutlined />);
  const handleStartGame = () => {
    axiosInstance.post("/connect4/start", {
        "player-1": player1,
        "player-2": player2,
      })
      .then((response) => {
        alert(response.data.message);
      })
      .catch((error) => {
        alert("Error starting game: " + error.response.data.message);
      });
  };

  return (
    <div className="sidebar">
      <div className="sidebar-item">
        {getIcon(player1)}
        <div className="dropdown">
          <label>Player 1</label>
          <select value={player1} onChange={handlePlayer1Change}>
            {agents.map((agent) => (
              <option key={agent} value={agent}>
                {agent}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="sidebar-item">
        {getIcon(player2)}
        <div className="dropdown">
          <label>Player 2</label>
          <select value={player2} onChange={handlePlayer2Change}>
            {agents.map((agent) => (
              <option key={agent} value={agent}>
                {agent}
              </option>
            ))}
          </select>
        </div>
      </div>

      <Stack spacing={2} direction="row">
        <Button variant="contained" onClick={handleStartGame}>
          Start
        </Button>
      </Stack>
    </div>
  );
};

export default Sidebar;
