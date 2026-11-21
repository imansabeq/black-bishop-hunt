# Black Bishop Hunt ♟️ (BFS Pathfinding)

An interactive **Pygame** visualization of the **Breadth-First Search (BFS)** algorithm on an 8×8 chessboard. Place a Black Bishop and White pieces anywhere on the board, and watch the Bishop find the shortest legal diagonal path to the highest-priority reachable target.

---

## 🎥 Demo

https://github.com/user-attachments/assets/03aa453a-9667-45db-b3c0-eaedf1d66bac

---

## ✨ Features

- **Shortest path via BFS:** uses `collections.deque` to find the minimum number of diagonal moves to each reachable piece.
- **Smart target prioritization:** targets are sorted by:
  1. **Priority:** `Queen` > `Rook` > `Bishop` / `Knight` > `Pawn`
  2. **Piece value:** `9`, `5`, `3`, `1`
  3. **Path length:** the shortest path breaks ties.
- **Chess constraints:**
  - Respects diagonal movement and square-color constraints.
  - **King protection:** the White King is a strict barrier. It cannot be captured, stepped onto, or jumped over.
- **Visual path highlights:** the previous square and the planned path are shown in green, and the target piece in red.

## 🎮 Controls

| Input | Action |
|-------|--------|
| **1st click** | Place the **Black Bishop** on any square |
| Keys `1` – `6` | Select the White piece: `1` Pawn, `2` Knight, `3` Bishop, `4` Rook, `5` Queen, `6` King |
| **Next clicks** | Place White pieces on the board |
| `Space` | Start the hunt (calculates the BFS path and executes the move) |
| **Reset** button | Clear the board to test a new scenario |

## 🚀 How to Run

```bash
git clone https://github.com/imansabeq/black-bishop-hunt.git
cd black-bishop-hunt
pip install -r requirements.txt
python main.py
```

## 🧪 Testing & Edge-Case Validation

### King protection fix (before vs after)

<p align="center">
  <img width="420" alt="Before the King protection fix" src="https://github.com/user-attachments/assets/965a987d-d1be-482b-a9a4-a90a9366ed65" />
  <img width="420" alt="After the King protection fix" src="https://github.com/user-attachments/assets/db208ce7-5e1d-497f-9d5e-737adbfded9c" />
</p>

### Test scenarios

<p align="center">
  <img width="420" alt="Test scenario 1" src="https://github.com/user-attachments/assets/3cd447c7-7194-4db3-be45-30237f5b50c3" />
  <img width="420" alt="Test scenario 2" src="https://github.com/user-attachments/assets/4f3621d7-fc7b-439b-bec2-2e7e41e3d918" />
</p>
<p align="center">
  <img width="420" alt="Test scenario 3" src="https://github.com/user-attachments/assets/6a03c28b-dd02-424d-85c7-6d403549425f" />
  <img width="420" alt="Test scenario 4" src="https://github.com/user-attachments/assets/3a2d6bb2-a7dc-4a62-b574-fd578912198a" />
</p>

## 🛠️ Tech Stack

Python · Pygame · `collections.deque` (BFS)

## 👩‍💻 Author

**Iman**

- GitHub: [@imansabeq](https://github.com/imansabeq)
- LinkedIn: [linkedin.com/in/imansabeq](https://www.linkedin.com/in/imansabeq)
