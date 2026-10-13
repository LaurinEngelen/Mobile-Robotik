# MORO-Labor WS 2024

In diesen Übungen implementieren Sie grundlegende Funktionen, die für die Steuerung von Robotern erforderlich sind. Mit diesen Funktionen steuern Sie dann einen mobilen Roboter mit Greifarm. Dabei lernen Sie auch das Robot Operating System 2 (ROS2) kennen.
Programmiert wird in Python.

## Arbeitsweise

- Klonen Sie dieses Repo, um die darin enthaltenen Aufgaben zu bearbeiten.
- Erstellen Sie für jede neue Aufgabe einen Branch nach dem Schema `exercise<Nummer>` (z.B. für Aufgabe 1: `exercise1`).
- Sobald Sie die Aufgabe bearbeitet haben, stellen Sie einen Merge-Request gegen den Branch `main` in diesem Repo.
- Die Aufgabe gilt als bestanden, wenn die CI-Pipeline alle Tests erfolgreich ausgeführt hat und der Merge-Request akzeptiert wurde.

Sie können selbstverständlich weitere Sub-Branches zum Bearbeiten der Aufgaben erstellen. Lediglich der Merge-Request
mit Ihrer Abgabe muss von einem Branch mit Namen nach dem Schema `exercise<Nummer>` ausgehen.

## Implementierungshinweis

- Verwenden Sie für Funktionsaufrufe ausschließlich Parameter in SI-Einheiten.
Beispielsweise werden Entfernungen in Meter, Zeiten in Sekunden und Winkel in Radianten angegeben.
Sollten Sie Einheiten zwischenzeitlich nicht in SI-Einheiten verarbeiten, machen Sie dies
durch den Variablennamen kenntlich. Speichern Sie Winkel beispielsweise in Grad, können Sie
die zugehörige Variable beispielsweise `alpha_deg` nennen.

- Runden Sie Ergebnisse nur in den Tests, nicht in den Funktionen.

## Abgaben

Die Merge-Requests für die einzelnen Abgaben müssen bis zu folgenden Terminen gestellt sein:

- **Exercise 1** (2023-10-31)
- **Exercise 2** (2023-11-14)
- **Exercise 3** (2023-11-28)
- **Exercise 4** (2023-12-12)
- **Exercise 5** (2024-01-16)
