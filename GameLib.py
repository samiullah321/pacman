try:
    import boinc
    _BOINC_ENABLED = True
except:
    _BOINC_ENABLED = False

class Game:

    # manages the control flow, requesting actions from agents.
    def __init__( self, agents, display, rules, s_index=0, mute_agent=False):
        self.agent_crash = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.s_index = s_index
        self.game_finish = False
        self.mute_agent = mute_agent
        self.move_history = []
        import io
        self.agent_out = [io.StringIO() for agent in agents]

    def get_progress(self): #Checking whether the game is over or not
        if self.game_finish:
            return 1.0
        else:
            return self.rules.get_progress(self)

    def _agentCrash( self, agent_index, quiet=False):
        "Helper method for handling agent crashes"
        if not quiet: traceback.print_exc()
        self.game_finish = True
        self.agent_crash = True
        self.rules.agent_crash(self, agent_index)

    ostd_out = None
    ostd_err = None

    def mute(self, agent_index):
        if not self.mute_agent: return
        global ostd_out, ostd_err
        import io
        ostd_out = sys.stdout
        ostd_err = sys.stderr
        sys.stdout = self.agent_out[agent_index]
        sys.stderr = self.agent_out[agent_index]

    def unmute(self):
        if not self.mute_agent: return
        global ostd_out, ostd_err
        # Revert stdout/stderr to originals
        sys.stdout = ostd_out
        sys.stderr = ostd_err


    def run( self ):
        """
        Main control loop for game play.
        """
        self.display.initialize(self.state.data)
        self.numMoves = 0

        ###self.display.initialize(self.state.makeObservation(1).data)
        # inform learning agents of the game start
        for i in range(len(self.agents)):
            agent = self.agents[i]
            if not agent:
                self.mute(i)
                # this is a null agent, meaning it failed to load
                # the other team wins
                print("Agent %d failed to load" % i, file=sys.stderr)
                self.unmute()
                self._agentCrash(i, quiet=True)
                return
            if ("registerInitialState" in dir(agent)):
                self.mute(i)
                agent.registerInitialState(self.state.deep_copy())
                ## TODO: could this exceed the total time
                self.unmute()

        agent_index = self.s_index
        numAgents = len( self.agents )

        while not self.game_finish:
            # Fetch the next agent
            agent = self.agents[agent_index]
            move_time = 0
            skip_action = False
            # Generate an observation of the state
            if 'observationFunction' in dir( agent ):
                self.mute(agent_index)
                observation = agent.observationFunction(self.state.deep_copy())
                self.unmute()
            else:
                observation = self.state.deep_copy()

            # Solicit an action
            action = None
            self.mute(agent_index)
            action = agent.get_move(observation)
            self.unmute()

            # Execute the action
            self.move_history.append( (agent_index, action) )
            self.state = self.state.produce_successor( agent_index, action )

            # Change the display
            self.display.update( self.state.data )
            ###idx = agent_index - agent_index % 2 + 1
            ###self.display.update( self.state.makeObservation(idx).data )

            # Allow for game specific conditions (winning, losing, etc.)
            self.rules.process(self.state, self)
            # Track progress
            if agent_index == numAgents + 1: self.numMoves += 1
            # Next agent
            agent_index = ( agent_index + 1 ) % numAgents

            if _BOINC_ENABLED:
                boinc.set_fraction_done(self.get_progress())

        # inform a learning agent of the game result
        for agent_index, agent in enumerate(self.agents):
            if "final" in dir( agent ) :
                try:
                    self.mute(agent_index)
                    agent.final( self.state )
                    self.unmute()
                except Exception as data:
                    if not False: raise
                    self._agentCrash(agent_index)
                    self.unmute()
                    return
        self.display.finish()
