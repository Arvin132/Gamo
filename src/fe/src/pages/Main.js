// Main.js
import React, { useState } from "react";
import {
  Box,
  CssBaseline,
  Drawer,
  Toolbar,
  Typography,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  ListItemIcon,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import SmartToyOutlinedIcon from "@mui/icons-material/SmartToyOutlined";
import Connect4Board from "../components/Connect4Board";

const drawerWidth = 240;

const Main = () => {
  const [player1, setPlayer1] = useState("Human");
  const [player2, setPlayer2] = useState("Robot");

  const handlePlayer1Change = (event) => {
    setPlayer1(event.target.value);
  };

  const handlePlayer2Change = (event) => {
    setPlayer2(event.target.value);
  };

  return (
    <Box sx={{ display: "flex", height: "100vh", bgcolor: "#f0f0f5" }}>
      <CssBaseline />

      {/* Permanent Drawer */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: "auto" }}>
          <List>
            {/* Player 1 Dropdown */}
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <PersonIcon />
                </ListItemIcon>
                <FormControl fullWidth>
                  <InputLabel>Player 1</InputLabel>
                  <Select
                    value={player1}
                    onChange={handlePlayer1Change}
                    label="Player 1"
                  >
                    <MenuItem value="Human">Human</MenuItem>
                    <MenuItem value="Robot">Robot</MenuItem>
                  </Select>
                </FormControl>
              </ListItemButton>
            </ListItem>

            {/* Player 2 Dropdown */}
            <ListItem disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  <SmartToyOutlinedIcon />
                </ListItemIcon>
                <FormControl fullWidth>
                  <InputLabel>Player 2</InputLabel>
                  <Select
                    value={player2}
                    onChange={handlePlayer2Change}
                    label="Player 2"
                  >
                    <MenuItem value="Human">Human</MenuItem>
                    <MenuItem value="Robot">Robot</MenuItem>
                  </Select>
                </FormControl>
              </ListItemButton>
            </ListItem>
          </List>
          <Divider />
        </Box>
      </Drawer>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          bgcolor: "background.default",
          minHeight: "100vh",
        }}
      >
        <Toolbar />
        <Typography variant="h4" gutterBottom>
          Connect 4 Game
        </Typography>
        <Typography variant="h6" gutterBottom>
          Player 1: {player1} | Player 2: {player2}
        </Typography>
        <Connect4Board />
      </Box>
    </Box>
  );
};

export default Main;
