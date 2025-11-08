A simple Chess AI mini project built using Python and Minimax algorithm. 
The AI evaluates possible moves and plays against the user intelligently using game tree logic. 
Created as part of my AI practical mini project.

# ♟️ Chess AI using Minimax Algorithm
This mini project is a simple **Chess AI** built using **Python**.  
The AI uses the **Minimax Algorithm** to calculate the best possible move by simulating all potential moves ahead and selecting the most optimal one.  
It demonstrates how Artificial Intelligence can make strategic decisions using game theory concepts.
## 🎯 **Project Objective**

The main goal of this project is to design an AI that can play Chess intelligently against a human player by predicting future moves using the Minimax algorithm.  
It focuses on **decision-making, recursion, and game tree evaluation**.

## ⚙️ **Features**

- Two-player mode: Player vs AI  
- AI powered by Minimax algorithm  
- Move validation for legal chess moves  
- Simple and clean user interface using **Tkinter**  
- Clear turn indication (Player / AI)  
- Displays check and checkmate situations  

---
## 🧩 **Tech Stack**
- **Language:** Python  
- **Libraries Used:**  
  - `tkinter` → For GUI  
  - `pygame` (if used) → For board display and animations  
  - `math` and `random` → For calculations  
  - Custom logic for move generation and evaluation  
---
## 🧠 **Algorithm Used: Minimax**
The **Minimax algorithm** is a recursive algorithm used in decision-making and game theory.  
It simulates all possible moves of both the player and the AI and evaluates them using a scoring function.

**Basic Working:**
1. The algorithm generates a **game tree** of all possible future moves.  
2. Each move is assigned a score based on the AI’s advantage or disadvantage.  
3. The AI chooses the move with the **maximum value**, while assuming the opponent plays optimally to minimize it.  
4. This process repeats recursively until a depth limit or end state (checkmate/draw) is reached.

---

## 🚀 **How to Run the Project**
1. **Clone the Repository**
   git clone https://github.com/Niharika-sharma03/Chess-AI-Minimax.git
   
   cd Chess-AI-Minimax
