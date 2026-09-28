# Project 1 Report: Intelligent Search Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Selected Region:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information 
- **Name:** John Paradela
- **UID (netID):** jpara3
- **UIN:** 660826798

---

## Section 1: Selected City Region
- **Selected Region:** Southern California: Los Angeles and Orange County

---

## Section 2: Map Graph Configuration
- **Total Cities Configured:** 20
- **Total Connection Edges:** 27
- **Graph Fully Connected:** Yes

---

## Section 3: Local Verification & Search Algorithms
*Check the algorithms you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Breadth-First Search (BFS)
- [x] Depth-First Search (DFS)
- [x] Uniform Cost Search (UCS)
- [x] Iterative Deepening Search (IDS)
- [x] Greedy Best-First Search (Greedy)
- [x] A* Search (A*)

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://project01-ai-search-qhkl.onrender.com/    
- **Video Presentation Link:** https://drive.google.com/file/d/1EjB-U6oeSugeWYrCJ4MzYlZkHvD4lDuU/view?usp=sharing

---

## Section 5: Discussion
- **Which search algorithm is best for this route finding problem?**
A* was the best choice in my Los Angeles to Irvine test. It found a 49.4 mile route, matching Uniform Cost Search (UCS), while expanding 13 nodes instead of 20. A* uses both the distance traveled and an estimate of the remaining distance to guide its search.
- **Search Efficiency (Nodes expanded/time taken comparison):**
Greedy Search expanded the fewest nodes of 5, but it had a route cost of 49.53 miles. A* expanded 13 and found a 49.4 mile route. Similarly, DFS also expanded 13, but its route cost was 66.09 miles. BFS and UCS each expanded 20; their route costs were 49.53 and 49.4 miles. IDS expanded 79 nodes because it repeated the search at increasing depth limits, and also had a route cost of 49.53.
- **Link the idea of search algorithm to today Generative AI.**
Both search algorithms and generative AI evaluate possible next steps to reach a result. My application explores connected cities and uses path costs and a distance estimate to choose a route. A generative AI system may evaluate possible words, past data, or tool actions when producing an answer. The options and getting data methods may be different, but both involve choosing alternatives as the process continues.

