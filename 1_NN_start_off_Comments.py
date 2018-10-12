import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT


class NN(sc2.BotAI):
    async def on_step(self, iteration):
        self.time = (self.state.game_loop/22.4) / 60
        print('Time:',self.time)

        # what to do every step
        await self.distribute_workers()  # in sc2/bot_ai.py
        await self.build_scv()			 # Build our worker who will mine minerals
        await self.game_state_args()

    async def build_scv(self):
    	for cc in self.units(COMMANDCENTER).ready.noqueue:
    		# print('\n \t We are in loop {}'.format(cc))
    		if self.can_afford(SCV) and not self.already_pending(SCV):
    			await self.do(cc.train(SCV))
    			# print('Passed conditions and train - {}'.format(self.do(cc.train(SCV))))

                ###############     INFORMATION     ###############
    #   I'm exploring game_state.py file

    async def game_state_args(self):
        # print(self.state.units)         #   All - minerals, geyser, commandcenter, scv ... e.t
        # print(self.state.common)        #   <sc2.game_state.Common object at 0x105bf66d8>
        # print(self.state.game_loop)     #   Game loops: 1,2,3,4 .....

#               For info:
# class Common(object):
#     ATTRIBUTES = [
#         "player_id",
#         "minerals", "vespene",
#         "food_cap", "food_used",
#         "food_army", "food_workers",
#         "idle_worker_count", "army_count",
#         "warp_gate_count", "larva_count"
#     ]
    #   Very begining of the game, first secs
        print(self.state.common.food_cap)       #   Units Cap = 15
        print(self.state.common.food_used)      #   Now I Have = 13 (1 is training in CC) 
        print(self.state.common.food_workers)   #   Currently without CC = 2
        print(self.state.common.food_army)      #   My army = 0


                ###############                     ###############


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, NN()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)