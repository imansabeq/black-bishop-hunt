# Black Bishop Hunt ♟️ (BFS Pathfinding)

An interactive **Pygame** visualization demonstrating the **Breadth-First Search (BFS)** algorithm on an 8×8 chessboard. Place a Black Bishop and White chess pieces anywhere on the board, and watch the Bishop find the shortest legal diagonal path to the highest-priority reachable target.

---

## ✨ Features
- **Shortest Path via BFS:** Uses `collections.deque` to find the minimum number of diagonal moves to each reachable piece.
- **Smart Target Prioritization:** Targets are sorted by:
  1. **Priority:** `Queen` > `Rook` > `Bishop` / `Knight` > `Pawn`
  2. **Piece Value:** (`9`, `5`, `3`, `1`)
  3. **Path Length:** Shortest path breaks ties.
- **Chess Constraints:**
  - Respects diagonal movement and square-color constraints.
  - **King Protection:** The White King acts as a strict barrier—it cannot be captured, stepped onto, or jumped over.
- **Visual Path Highlights:** Highlights the previous square and planned path in green, and the target piece in red.

---

## 🎮 Controls
- **1st Click:** Place the **Black Bishop** on any square.
- **Keys `1` – `6`:** Select White piece type:
  - `1`: Pawn | `2`: Knight | `3`: Bishop | `4`: Rook | `5`: Queen | `6`: King
- **Subsequent Clicks:** Place White pieces on the board.
- **`Space`:** Start the hunt (calculates BFS path and executes move).
- **`Reset` Button:** Clear the board to test a new scenario.

---

## 🚀 How to Run
```bash
git clone https://github.com/imansabeq/black-bishop-hunt.git
cd black-bishop-hunt
pip install -r requirements.txt
python main.py
```
## 🎥 Demo & Testing & Edge-Case Validation:
King Protection Constraint (Before vs After)
### Screen Recording

https://github.com/user-attachments/assets/03aa453a-9667-45db-b3c0-eaedf1d66bac

-----------------------------------------------

#### King Protection Fix (Before vs After)
<img width="420" alt="before" src="https://github.com/user-attachments/assets/965a987d-d1be-482b-a9a4-a90a9366ed65" />
<img width="420" alt="after" src="https://github.com/user-attachments/assets/db208ce7-5e1d-497f-9d5e-737adbfded9c" />

<img width="897" height="811" alt="Screenshot 2026-11-20 171015" src="https://github.com/user-attachments/assets/3cd447c7-7194-4db3-be45-30237f5b50c3" />
<img width="822" height="862" alt="Screenshot 2026-11-20 171824" src="https://github.com/user-attachments/assets/4f3621d7-fc7b-439b-bec2-2e7e41e3d918" />
<img width="875" height="913" alt="Screenshot 2026-11-20 171922" src="https://github.com/user-attachments/assets/6a03c28b-dd02-424d-85c7-6d403549425f" />
<img width="876" height="900" alt="Screenshot 2026-11-20 172250" src="https://github.com/user-attachments/assets/3a2d6bb2-a7dc-4a62-b574-fd578912198a" />





---

## 👩‍💻 Author
**Iman**
- GitHub: [@imansabeq](https://github.com/imansabeq)
- LinkedIn: www.linkedin.com/in/imansabeq
