import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import COMMANDCENTER, SCV, SUPPLYDEPOT, COLOSSUS, SUPPLYDEPOTLOWERED


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
                ###############                     ###############
                ###############     game_state.py   ###############


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
        # print(self.state.common.food_cap)       #   Units Cap = 15
        # print(self.state.common.food_used)      #   Now I Have = 13 (1 is training in CC) 
        # print(self.state.common.food_workers)   #   Currently without CC = 2
        # print(self.state.common.food_army)      #   My army = 0


                ###############     INFORMATION     ###############
                ###############                     ###############
                ###############     game_data.py    ###############
                ###############  GameData(object)   ###############

# GameData(object) - includes: UpgradeData(object), AbilityData(object), UnitTypeData(object)

###############     UpgradeData(object)      ###############

    #### Exploring game_data.py Class UpgradeData --> trying to extract usefull data
        # print('\n\t\t   RESEARCH_ABILITY ')
        # print(type(self._game_data.upgrades))           #   class "Dict"
        # for www in (self._game_data.upgrades).items():  #   Iterate throught dict
        #     print('\n\n',www)                           #   (292, <sc2.game_data.UpgradeData object at 0x1060b3940>)

        # for xxx in (self._game_data.upgrades).values(): #   Iterate throught values()
        #     print('\n\n',xxx)                           #   <sc2.game_data.UpgradeData object at 0x1060c5898>

    #### Iterating through methods insidde class UpgradeData(object) and class AbilityData(object)
        # for xxx in (self._game_data.upgrades).values():
        #     if xxx.research_ability != None:
        #         print('\n inside Values() Type', xxx.name)      #   CarrierLaunchSpeedUpgrade (first iteration) - and so on - GlialReconstitution, TunnelingClaws .... DiggingClaws(last) 
        #         print('\n Inside values()', type(xxx.name))     #   <class 'str'> (first iteration) 

        #         print('\n inside Values() Type', xxx.research_ability)      #   AbilityData(name=ResearchInterceptorLaunchSpeedUpgrade)
        #         print('\n Inside values()', type(xxx.research_ability))     #   <class 'sc2.game_data.AbilityData'>
        #         print('\n inside Values() Type', xxx.research_ability.is_free_morph)        #   False
        #         print('\n inside Values() Type', type(xxx.research_ability.is_free_morph))  #   <class 'bool'>

        #         print('\n inside Values() Type', xxx.cost)              #   Cost(150, 150)
        #         print('\n Inside values()', type(xxx.cost))             #   <class 'sc2.game_data.Cost'>


###############     AbilityData(object)      ###############

#         print(self._game_data.abilities)                  #   Giant Dict, pull out all data from ability_id.py
# #   {1: AbilityData(name=Smart), 2: AbilityData(name=Taunt), .....  3771: AbilityData(name=OverlordTransportLoad), 3773: AbilityData(name=OverlordTransportUnload)}  
#         print(type(self._game_data.abilities))            #   <class 'dict'>
#         # for ab in self._game_data.abilities.items():
#         #     print('\n\t {}'.format(ab))                   #     (1, AbilityData(name=Smart)) ; (2, AbilityData(name=Taunt))
#         for abVal in self._game_data.abilities.values():
#             # print('\n\t {}'.format(abVal.name))
#             print('\n\t {}'.format(abVal.id))               #   AbilityId.SMART
#             print('\n\t {}'.format(type(abVal.id)))         #   <enum 'AbilityId'>
#             print('\n\t {}'.format(abVal.cost))             #   Cost(0, 0)
#             print('\n\t {}'.format(type(abVal.cost)))       #   <class 'sc2.game_data.Cost'>
#             print('\n\t {}'.format(abVal.id_exists))        #   <function AbilityData.id_exists at 0x105498488>
#             print('\n\t {}'.format(type(abVal.id_exists)))  #   <class 'function'>



###############     UnitTypeData(object)      ###############

#### Iterating through methods insidde class UnitTypeData(object)

#         print('\n UNIT', self._game_data.units)     
# #   {1: <sc2.game_data.UnitTypeData object at 0x106076e80>, ..... 1925: <sc2.game_data.UnitTypeData object at 0x1060a07f0>}
#         print('\n', type(self._game_data.units))    #   <class 'dict'>

#         for un in self._game_data.units.values():
#             try:
#                 print('\n\tID {}'.format(un.id))            #   UnitTypeId.COLOSSUS
#                 print('\n\tID {}'.format(type(un.id)))      #   <enum 'UnitTypeId'>

#                 print('\n\tNAME {}'.format(un.name))        #   Colossus
#                 print('\n\tNAME {}'.format(type(un.name)))  #   <class 'str'>   

#                 print('\n\tCREATION_ABILITY {}'.format(un.creation_ability))        #   AbilityData(name=Colossus)
#                 print('\n\tCREATION_ABILITY {}'.format(type(un.creation_ability)))  #   <class 'sc2.game_data.AbilityData'>

#                 print('\n\tATTRIBUTES {}'.format(un.attributes))                    #   [2, 4, 7]
#                 print('\n\tATTRIBUTES {}'.format(type(un.attributes)))              #   <class 'google.protobuf.internal.containers.RepeatedScalarFieldContainer'>

#                 print('\n\t HAS ATTRIBUTES {}'.format(un.has_attribute))            #   <bound method UnitTypeData.has_attribute of <sc2.game_data.UnitTypeData object at 0x10607ce80>>
#                 print('\n\t HAS ATTRIBUTES {}'.format(type(un.has_attribute)))      #   <class 'method'>

#                 print('\n\tHAS MINERALS {}'.format(un.has_minerals))                #   False
#                 print('\n\tHAS MINERALS {}'.format(type(un.has_minerals)))          #   <class 'bool'>

#                 print('\n\tHAS VESPENE {}'.format(un.has_vespene))                  #   False
#                 print('\n\tHAS VESPENE {}'.format(type(un.has_vespene)))            #   <class 'bool'>

#                 print('\n\tCOST {}'.format(un.cost))                                #   Cost(300, 200)
#                 print('\n\tCOST {}'.format(type(un.cost)))                          #   <class 'sc2.game_data.Cost'>
#             except:
#                 pass 



                ###############     INFORMATION     ###############
                ###############                     ###############
                ###############     game_state.py   ###############

###############     class Units(list):      ###############
    #   Here we're working with 'sc2.units.Units'
        u = self.units(SUPPLYDEPOT)
        ulow = self.units(SUPPLYDEPOTLOWERED)

        # print('\n\t BARRACK - {}'.format(u))        #   [Unit(name='SupplyDepot', tag=4354211841)]
        # print('\n\t BARRACK - {}'.format(type(u)))  #

        # print('\n', self.units)                     #  [Unit(name='SCV', tag=4347658241),  ...  Unit(name='CommandCenter', tag=4346347521)]
        # print('\n', type(self.units))               #   <class 'sc2.units.Units'>

    #   Here we're working with 'sc2.units.Unit'
        for unn in self.units:
            if unn.name == 'SupplyDepot':
        #         print('\n\t Units - {}'.format(unn))                          #   Unit(name='SupplyDepot', tag=4353687553)
        #         print('\n\t Units - {}'.format(type(unn)))                    #   <class 'sc2.unit.Unit'>

        #         print('\n\t TYPE ID - {}'.format(unn.type_id))                #   UnitTypeId.SUPPLYDEPOT
        #         print('\n\t TYPE ID - {}'.format(type(unn.type_id)))          #   <enum 'UnitTypeId'>

        #         print('\n\t TYPE DATA - {}'.format(unn._type_data))           #   <sc2.game_data.UnitTypeData object at 0x1060b32b0>
        #         print('\n\t TYPE DATA - {}'.format(type(unn._type_data)))     #   <class 'sc2.game_data.UnitTypeData'>

        #         print('\n\t IS SNAPSHOT - {}'.format(unn.is_snapshot))        #   False
        #         print('\n\t IS SNAPSHOT - {}'.format(type(unn.is_snapshot)))  #   <class 'bool'>

        #         print('\n\t IS VISIBLE - {}'.format(unn.is_visible))          #   True
        #         print('\n\t IS VISIBLE - {}'.format(type(unn.is_visible)))    #   <class 'bool'>

        #         print('\n\t ALLIANCE - {}'.format(unn.alliance))              #   1
        #         print('\n\t ALLIANCE - {}'.format(type(unn.alliance)))        #   <class 'int'>

        #         print('\n\t IS_MINE - {}'.format(unn.is_mine))                #   True
        #         print('\n\t IS_MINE - {}'.format(type(unn.is_mine)))          #   <class 'bool'>

        #         print('\n\t IS_ENEMY - {}'.format(unn.is_enemy))              #   False
        #         print('\n\t IS_ENEMY - {}'.format(type(unn.is_enemy)))        #   <class 'bool'>

        #         print('\n\t TAG - {}'.format(unn.tag))                        #   4353687553
        #         print('\n\t TAG - {}'.format(type(unn.tag)))                  #   <class 'int'>

        #         print('\n\t Owner - {}'.format(unn.owner_id))                 #   1
        #         print('\n\t Owner - {}'.format(type(unn.owner_id)))           #   <class 'int'>

        #         print('\n\t Position - {}'.format(unn.position))              #   (156.0, 21.0)
        #         print('\n\t Position - {}'.format(type(unn.position)))        #   <class 'sc2.position.Point2'>

        #         print('\n\t Position 3D - {}'.format(unn.position3d))         #   (156.0, 21.0, 11.984375)
        #         print('\n\t Position 3D - {}'.format(type(unn.position3d)))   #   <class 'sc2.position.Point3'>

        #         print('\n\t Distance to Center - {}'.format(unn.distance_to(self.game_info.map_center)))         #   75.7429864739964
        #         print('\n\t Distance to Center - {}'.format(type(unn.distance_to(self.game_info.map_center))))   #   <class 'float'>

        #         print('\n\t Facing - {}'.format(unn.facing))                  #   3.925297260284424
        #         print('\n\t Facing - {}'.format(type(unn.facing)))            #   <class 'float'>

        #         print('\n\t Radius - {}'.format(unn.radius))                  #   1.25
        #         print('\n\t Radius - {}'.format(type(unn.radius)))            #   <class 'float'>

        #         print('\n\t DETECT RANGE - {}'.format(unn.detect_range))      #   0
        #         print('\n\t DETECT RANGE - {}'.format(type(unn.detect_range)))#   <class 'float'>

        #         print('\n\t RADAR_RANGE - {}'.format(unn.radar_range))        #   0
        #         print('\n\t RADAR_RANGE - {}'.format(type(unn.radar_range)))  #   <class 'float'>

        #         print('\n\t BUILD PROGRESS - {}'.format(unn.build_progress))        #   1
        #         print('\n\t BUILD PROGRESS - {}'.format(type(unn.build_progress)))  #   <class 'float'>

        #         print('\n\t IS READY - {}'.format(unn.is_ready))              #   True
        #         print('\n\t IS READY - {}'.format(type(unn.is_ready)))        #   <class 'bool'>

        #         print('\n\t CLOAK - {}'.format(unn.cloak))                    #   3
        #         print('\n\t CLOAK - {}'.format(type(unn.cloak)))              #   <class 'int'>

        #         print('\n\t IS BLIP - {}'.format(unn.is_blip))                #   false
        #         print('\n\t IS BLIP - {}'.format(type(unn.is_blip)))          #   <class 'bool'>

        #         print('\n\t IS POWERED - {}'.format(unn.is_powered))          #   false
        #         print('\n\t IS POWERED - {}'.format(type(unn.is_powered)))    #   <class 'bool'>

                print('\n\t IS BURROWED - {}'.format(unn.is_burrowed))        #   false
                print('\n\t IS BURROWED - {}'.format(type(unn.is_burrowed)))  #   <class 'bool'>

        #         print('\n\t IS FLYING - {}'.format(unn.is_flying))            #   False
        #         print('\n\t IS FLYING - {}'.format(type(unn.is_flying)))      #   <class 'bool'>

        #         print('\n\t IS STRUCTURE - {}'.format(unn.is_structure))      #   True
        #         print('\n\t IS STRUCTURE - {}'.format(type(unn.is_structure)))#   <class 'bool'>

        #         print('\n\t IS MINERAL FIELD - {}'.format(unn.is_mineral_field))        #   False
        #         print('\n\t IS MINERAL FIELD - {}'.format(type(unn.is_mineral_field)))  #   <class 'bool'>

        #         print('\n\n\t\t\t\t NEXT')

        #         print('\n\t HEALTH - {}'.format(unn.health))                #   40.866943359375
        #         print('\n\t HEALTH - {}'.format(type(unn.health)))          #   <class 'float'>

        #         print('\n\t HEALTH MAX - {}'.format(unn.health_max))        #   400.0
        #         print('\n\t HEALTH MAX - {}'.format(type(unn.health_max)))  #   <class 'float'>

        #         print('\n\t SHIELD - {}'.format(unn.shield))                #   0
        #         print('\n\t SHIELD - {}'.format(type(unn.shield)))          #   <class 'float'>

        #         print('\n\t SHIELD MAX - {}'.format(unn.shield_max))        #   0
        #         print('\n\t SHIELD MAX - {}'.format(type(unn.shield_max)))  #   <class 'float'>

        #         print('\n\t ENERGY - {}'.format(unn.energy))                #   0
        #         print('\n\t ENERGY - {}'.format(type(unn.energy)))          #   <class 'float'>

        #         print('\n\t MINERAL CONTENTS - {}'.format(unn.mineral_contents))        #   0
        #         print('\n\t MINERAL CONTENTS - {}'.format(type(unn.mineral_contents)))  #   <class 'int'>

        #         print('\n\t IS SELECTED - {}'.format(unn.is_selected))        #   False
        #         print('\n\t IS SELECTED - {}'.format(type(unn.is_selected)))  #   <class 'bool'>

        #         print('\n\t ORDERS - {}'.format(unn.orders))                #   []   If it's SCV = 
        #         #[UnitOrder(AbilityData(name=SupplyDepot), x: 44.0, y: 120.0, 0.0)]
        #         print('\n\t ORDERS - {}'.format(type(unn.orders)))          #   <class 'list'>

        #         print('\n\t IS ADD ON TAG - {}'.format(unn.add_on_tag))        #   0
        #         print('\n\t IS ADD ON TAG - {}'.format(type(unn.add_on_tag)))  #   <class 'int'>

        #         print('\n\t HAS ADD ON - {}'.format(unn.has_add_on))        #   False
        #         print('\n\t HAS ADD ON - {}'.format(type(unn.has_add_on)))  #   <class 'bool'>

        #         print('\n\t ASSIGHNED HARVESTERS - {}'.format(unn.assigned_harvesters))        #   0
        #         print('\n\t ASSIGHNED HARVESTERS - {}'.format(type(unn.assigned_harvesters)))  #   <class 'int'>

        #         print('\n\t IDEAL HARVESTERS - {}'.format(unn.ideal_harvesters))        #   0
        #         print('\n\t IDEAL HARVESTERS - {}'.format(type(unn.ideal_harvesters)))  #   <class 'int'>

#   Did't check - train; build; has_buff; warp_in; attack; gather; return_resource; move; hold_position; stop; 


                print('\n\n\t\t\t\t #############################################')
                #       SUPPLYDEPOTLOWERED





run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, NN()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)