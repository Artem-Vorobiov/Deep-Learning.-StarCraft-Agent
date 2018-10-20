import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT, REFINERY, VESPENEGEYSER, MINERALFIELD, BARRACKS, FACTORY, \
STARPORT, BARRACKSREACTOR, BARRACKSTECHLAB, STARPORTREACTOR, STARPORTTECHLAB, FACTORYTECHLAB, FACTORYREACTOR, \
MARAUDER, MARINE, HELLION
from sc2.game_data import UpgradeData
from sc2 import position
from sc2.ids.ability_id import AbilityId
from sc2.game_info import Ramp

import math
import random
import time

import cv2
import numpy as np


MAX_WORKERS = 60
adjusted_time_set = set()
HEADLESS = True


class NN(sc2.BotAI):

    def __init__(self, title=1):
        self.tags = set()
        self.title = title


    async def on_step(self, iteration):
        #   Adjusted TimeChecking Function
        self.time = (self.state.game_loop/22.4) / 60
        adjusted_time = round(self.time, 1)
        if adjusted_time not in adjusted_time_set:
            adjusted_time_set.add(adjusted_time)
            print(adjusted_time)

        # what to do every step
        await self.distribute_workers()  
        await self.build_scv()           
        await self.build_supply_depot()
        await self.build_refinery()
        await self.expand()
        await self.build_barrack()
        await self.build_factory() 
        await self.improve_barracks()  
        await self.train_soldiers()    
        await self.attack_enemy_g()
        await self.train_hellion()
        await self.exploring()

        await self.intel()          #   NEW

    async def intel(self):
        # 1.  Make up array using Numpy. Paraments it is our map coordinates - 
        #     x: self.game_info.map_size[1],  t: self.game_info.map_size[0]

        # 2.  cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
        #     Make up circle. Loop through all units, pick up their positions(pos = unit.position). Draw circle: 
        #     (center) x: pos[0], y = pos[1]; (radius): unit.radius*8 

        # 3.  For enamy units the same.

        # 4.  Build progress bars dependences:  mineral_ratio, vespene_ratio, population_ratio, plausible_supply, worker_weight

        # 5.  Draw progress bars:
        #         cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) 

        # 6.  Flip horizontally:
        #         cv2.flip(src, flipCode[, dst])

        # 7.  Resize:
        #         cv2.resize(src, dsize[, dst[, fx[, fy[, interpolation]]]])

        # 8.  Closing...


        # 1.
        game_data = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)

        # 2. 
        for unit in self.units().ready:
            pos = unit.position
            cv2.circle(game_data, (int(pos[0]), int(pos[1])), int(unit.radius*8), (255, 255, 255), math.ceil(int(unit.radius*0.5)))

        # 3. 
        for unit in self.known_enemy_units:
            pos = unit.position
            cv2.circle(game_data, (int(pos[0]), int(pos[1])), int(unit.radius*8), (125, 125, 125), math.ceil(int(unit.radius*0.5)))

        # 4. 
        try:
            line_max = 50
            mineral_ratio = self.minerals / 1500
            if mineral_ratio > 1.0:
                mineral_ratio = 1.0

            vespene_ratio = self.vespene / 1500
            if vespene_ratio > 1.0:
                vespene_ratio = 1.0

            population_ratio = self.supply_left / self.supply_cap
            if population_ratio > 1.0:
                population_ratio = 1.0

            plausible_supply = self.supply_cap / 200.0

            worker_weight = len(self.units(SCV)) / (self.supply_cap-self.supply_left)
            if worker_weight > 1.0:
                worker_weight = 1.0


        # 5. 
            cv2.line(game_data, (0, 19), (int(line_max*worker_weight), 19), (250, 250, 200), 3)  # worker/supply ratio
            cv2.line(game_data, (0, 15), (int(line_max*plausible_supply), 15), (220, 200, 200), 3)  # plausible supply (supply/200.0)
            cv2.line(game_data, (0, 11), (int(line_max*population_ratio), 11), (150, 150, 150), 3)  # population ratio (supply_left/supply)
            cv2.line(game_data, (0, 7), (int(line_max*vespene_ratio), 7), (210, 200, 0), 3)  # gas / 1500
            cv2.line(game_data, (0, 3), (int(line_max*mineral_ratio), 3), (0, 255, 25), 3)  # minerals minerals/1500
        except Exception as e:
            print(str(e))

        # 6. 
        grayed = cv2.cvtColor(game_data, cv2.COLOR_BGR2GRAY)
        self.flipped = cv2.flip(grayed, 0)

        # 7. 
        resized = cv2.resize(self.flipped, dsize=None, fx=2, fy=2)

        # 8.
        cv2.imshow(str(self.title), resized)
        cv2.waitKey(1)



    def select_target(self):
        return self.enemy_start_locations[0].position


    async def attack_enemy_g(self):
        target = self.select_target()   #   <coroutine object NN.select_target at 0x105ae4258>

        if self.units(MARAUDER).amount >= 7 and self.units(MARINE).amount >= 10:
            for m in self.units(MARAUDER).idle:
                await self.do(m.attack(target))
            for mn in self.units(MARINE).idle:
                await self.do(mn.attack(target))
        elif self.known_enemy_units.exists:
            for m in self.units(MARAUDER).idle:
                # print('\n\t Inside known_enemy_units.exists', self.known_enemy_units)         #   True
                await self.do(m.attack(self.known_enemy_units.random.position))
                # print('\n\t RANDOM ENEMY POSITION', self.known_enemy_units.random.position)   #   (150.970458984375, 21.9423828125)
            for mn in self.units(MARINE).idle:
                await self.do(mn.attack(self.known_enemy_units.random.position))


    async def expand(self):
        if self.units(COMMANDCENTER).amount < 2:
            if self.can_afford(COMMANDCENTER) and not self.already_pending(COMMANDCENTER):
                # print('\n EXPANDING FIRST CONDITION ... ')
                await self.expand_now()
        elif self.units(COMMANDCENTER).amount < 3.5 and self.time >= 4:
            if self.can_afford(COMMANDCENTER) and not self.already_pending(COMMANDCENTER):
                # print('\n EXPANDING  second condition... ')
                await self.expand_now()

    async def build_factory(self):
        cc = self.units(COMMANDCENTER).first
        if self.units(BARRACKS).amount == 2:
            if self.can_afford(FACTORY) and not self.already_pending(FACTORY) \
            and self.units(FACTORY).amount < 1 and self.units(MARINE).amount >= 3:
                await self.build(FACTORY, near = cc.position.towards(self.main_base_ramp.top_center, 7))

    async def train_hellion(self):
        if self.units(FACTORY).ready and self.units(MARINE).amount >= 5:
            if self.can_afford(HELLION) and not self.already_pending(HELLION):
                for i in self.units(FACTORY).noqueue:
                    await self.do(i.train(HELLION))
                    print('\n Trainin HELLION', i)

############################################################################################
############################################################################################
############################################################################################
#                       Effective solution for exploring the map

#   self.do(h.attack(self.state.mineral_field.random.position))

    async def exploring(self):
        if self.units(HELLION).amount >=5:
            for h in self.units(HELLION).idle:
                await self.do(h.attack(self.state.mineral_field.random.position))
############################################################################################
############################################################################################
############################################################################################




    async def build_barrack(self):
        for cc in self.units(COMMANDCENTER).ready:
            if self.units(BARRACKS).amount < 2 and self.time > 1.6:
                if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
                    # print('\n\t\t\t\t We are in BUILD BARRACKS method')
                    await self.build(BARRACKS, near = cc.position.towards(self.game_info.map_center, 10))
    

    async def improve_barracks(self):   
        for BR in self.units(BARRACKS).ready:
            if not self.tags:
                await self.do(BR.build(BARRACKSTECHLAB))
                self.tags.add(BR.tag)


    async def train_soldiers(self):
        if self.units(BARRACKSTECHLAB).ready:
            for brlab in self.units(BARRACKS).noqueue:
                if brlab.tag in self.tags:
                    # print('\n Took one BARRACKS: {}'.format(brlab.tag))
                    if self.can_afford(MARAUDER):
                        if not self.already_pending(MARAUDER):
                            await self.do(brlab.train(MARAUDER))
                            # print('\n Training MARAUDER: {}'.format(brlab.tag))
                else:
                    if self.can_afford(MARINE):
                        if not self.already_pending(MARINE):
                            await self.do(brlab.train(MARINE))
                            # print('\n Training MARINE: {}'.format(brlab.tag))


    async def build_refinery(self):
        if self.units(SUPPLYDEPOT).exists:
            for cc in self.units(COMMANDCENTER):
                if self.can_afford(REFINERY) and not self.already_pending(REFINERY) and self.units(REFINERY).amount < 1:
                    try:
                        vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                        for vg in vgs:
                            if self.units(REFINERY).closer_than(1.0,vg).exists:
                                break
                            worker = self.select_build_worker(vg.position)
                            await self.do(worker.build(REFINERY, vg))
                    except Exception as e:
                        pass

                elif self.can_afford(REFINERY) and self.time > 1.7 and self.units(REFINERY).amount < 3 and not self.already_pending(REFINERY):
                    try:
                        vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                        for vg in vgs:
                            if self.units(REFINERY).closer_than(1.0,vg).exists:
                                break
                            worker = self.select_build_worker(vg.position)
                            await self.do(worker.build(REFINERY, vg))
                    except Exception as e:
                        pass

                elif self.can_afford(REFINERY) and self.time > 4 and self.units(REFINERY).amount < 4 and not self.already_pending(REFINERY):
                    try:
                        vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                        for vg in vgs:
                            if self.units(REFINERY).closer_than(1.0,vg).exists:
                                break
                            worker = self.select_build_worker(vg.position)
                            await self.do(worker.build(REFINERY, vg))
                    except Exception as e:
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
                await self.build(SUPPLYDEPOT, near = SD.first.position.towards(self.main_base_ramp.top_center, 4))






run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, NN()),
    Computer(Race.Terran, Difficulty.Medium)
], realtime=False)