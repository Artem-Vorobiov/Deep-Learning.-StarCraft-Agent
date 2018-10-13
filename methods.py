import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT, REFINERY, VESPENEGEYSER, MINERALFIELD
from sc2 import position

MAX_WORKERS = 60

class MethodERSD(sc2.BotAI):

	async def expand(self):
	    if self.units(COMMANDCENTER).amount < 2:
	        if self.can_afford(COMMANDCENTER) and not self.already_pending(COMMANDCENTER):
	            print('\n EXPANDING FIRST CONDITION ... ')
	            await self.expand_now()
	    elif self.units(COMMANDCENTER).amount < 3.5 and self.time >= 4:
	        if self.can_afford(COMMANDCENTER) and not self.already_pending(COMMANDCENTER):
	            print('\n EXPANDING  second condition... ')
	            await self.expand_now()


	#   ЕСТЬ ПРОБЛЕМА - когда постороено 2 СС выскакивает ошибка касательно строительства REFINERY

	#   Specific Architecture for - finding spot and building Geyser
	async def build_refinery(self):
	    for cc in self.units(COMMANDCENTER):
	        print('\n Im inside REFINERY !!!')
	        if self.can_afford(REFINERY) and not self.already_pending(REFINERY) and self.units(REFINERY).amount < 1:
	            try:
	                print('\n\t\t\t FIRST CONDITION')
	                #   Found Geyser near CommandCenter
	                vgs = self.state.vespene_geyser.closer_than(20.0, cc)
	                    #   Iterate through Geyser near CC
	                for vg in vgs:
	                    #   Check If REFINERY already exists on Geyser Spot, If so break
	                    if self.units(REFINERY).closer_than(1.0,vg).exists:
	                        break
	                    #   If not exists, then select worker and use him for building Refinery
	                    worker = self.select_build_worker(vg.position)
	                    await self.do(worker.build(REFINERY, vg))
	            except Exception as e:
	                print(e)
	                pass

	        elif self.can_afford(REFINERY) and self.time > 1.45 and self.units(REFINERY).amount < 3 and not self.already_pending(REFINERY):
	            try:
	                print('\n\t\t\t SECOND CONDITION')
	                #   Found Geyser near CommandCenter
	                vgs = self.state.vespene_geyser.closer_than(20.0, cc)
	                    #   Iterate through Geyser near CC
	                for vg in vgs:
	                    #   Check If REFINERY already exists on Geyser Spot, If so break
	                    if self.units(REFINERY).closer_than(1.0,vg).exists:
	                        break
	                    #   If not exists, then select worker and use him for building Refinery
	                    worker = self.select_build_worker(vg.position)
	                    await self.do(worker.build(REFINERY, vg))
	            except Exception as e:
	                print(e)
	                pass

	        elif self.can_afford(REFINERY) and self.time > 4 and self.units(REFINERY).amount < 4 and not self.already_pending(REFINERY):
	            try:
	                print('\n\t\t\t THIRD CONDITION')
	                #   Found Geyser near CommandCenter
	                vgs = self.state.vespene_geyser.closer_than(20.0, cc)
	                    #   Iterate through Geyser near CC
	                for vg in vgs:
	                    #   Check If REFINERY already exists on Geyser Spot, If so break
	                    if self.units(REFINERY).closer_than(1.0,vg).exists:
	                        break
	                    #   If not exists, then select worker and use him for building Refinery
	                    worker = self.select_build_worker(vg.position)
	                    await self.do(worker.build(REFINERY, vg))
	            except Exception as e:
	                print(e)
	                pass


	async def build_scv(self):
	    if self.units(SCV).amount <= MAX_WORKERS:
	        for cc in self.units(COMMANDCENTER).ready.noqueue:
	            if self.can_afford(SCV) and not self.already_pending(SCV):
	                await self.do(cc.train(SCV))


	async def build_supply_depot(self):
	    SD = self.units(COMMANDCENTER)
	    if self.supply_used > 0.7*self.supply_cap:
	        if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
	            await self.build(SUPPLYDEPOT, near = SD.first.position.towards(self.game_info.map_center, 6))
