# Look at challenge_4.py, rules.py

## STRATEGY
1. Left-hand rule from START.
2. Make a checkpoint when there is a three-turn combination and store it in array.
3. Checkpoint actions are reversed ("L" becomes "R", "S" still "S").
4. Use checkpoint actions when traveling back from END.

## PROBLEM
1. No solution for the nested T-juctions.
