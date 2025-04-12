// src/ThemeToggle.js
import React from "react";

const ThemeToggle = ({ toggleTheme }) => {
  return (
    <button
      className="dark-mode-button"
      onClick={toggleTheme}
      aria-label="Toggle Dark/Light Mode"
    >
      🌙
    </button>
  );
};

export default ThemeToggle;
