
python pacman.py --frame_t 0 -p reflex_agent

pause
python pacman.py --frame_t 0 -p alpha_beta_agent -l trappedClassic -a depth=3 -q -n 10
pause

python pacman.py --frame_t 0 -p expecti_max_agent -l trappedClassic -a depth=3 -q -n 10
pause
python pacman.py --frame_t 0 -p reflex_agent -l testClassic

pause
python pacman.py --frame_t 0 -p reflex_agent -k 1

pause
python pacman.py --frame_t 0 -p reflex_agent -k 2
pause
python pacman.py --frame_t 0 -p reflex_agent -l openClassic -n 10 -q
pause


python pacman.py --frame_t 0 -p minimax_agent -l minimaxClassic -a depth=4
pause
python pacman.py --frame_t 0 -p minimax_agent -l trappedClassic -a depth=3
pause

python pacman.py --frame_t 0 -p alpha_beta_agent -a depth=3 -l smallClassic
pause

::python pacman.py --frame_t 0 -l smallClassic -p expecti_max_agent -q -n 30

::pause
