
python pacman.py --frameTime 0 -p ReflexAgent

pause
python pacman.py --frameTime 0 -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
pause

python pacman.py --frameTime 0 -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
pause
python pacman.py --frameTime 0 -p ReflexAgent -l testClassic

pause
python pacman.py --frameTime 0 -p ReflexAgent -k 1

pause
python pacman.py --frameTime 0 -p ReflexAgent -k 2
pause
python pacman.py --frameTime 0 -p ReflexAgent -l openClassic -n 10 -q
pause


python pacman.py --frameTime 0 -p MinimaxAgent -l minimaxClassic -a depth=4
pause
python pacman.py --frameTime 0 -p MinimaxAgent -l trappedClassic -a depth=3
pause

python pacman.py --frameTime 0 -p AlphaBetaAgent -a depth=3 -l smallClassic
pause

::python pacman.py --frameTime 0 -l smallClassic -p ExpectimaxAgent -q -n 30

pause
