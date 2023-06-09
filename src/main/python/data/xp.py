# handles stuff related to the players xp and promotions

import struct

from main.python.data.data import DataSource, ReadFromBytes

# xp_table[i] = XP needed for level i+1
XP_TABLE: list[int] = [
    0,
    3000,
    7000,
    12000,
    18000,
    25000,
    33000,
    42000,
    52000,
    63000,
    75000,
    88000,
    102000,
    117000,
    132500,
    148500,
    165000,
    182000,
    199500,
    217500,
    236000,
    255000,
    274500,
    294500,
    315000,
]

# ordered list of the promotion ranks (low -> high)
PROMO_RANKS: list[str] = [
    "None",
    "Bronze 1",
    "Bronze 2",
    "Bronze 3",
    "Silver 1",
    "Silver 2",
    "Silver 3",
    "Gold 1",
    "Gold 2",
    "Gold 3",
    "Platinum 1",
    "Platinum 2",
    "Platinum 3",
    "Diamond 1",
    "Diamond 2",
    "Diamond 3",
    "Legendary 1",
    "Legendary 2",
    "Legendary 3",
    "Legendary 3+",
]
MAX_BADGES: int = len(PROMO_RANKS) - 1

# ordered list of player rank titles (low -> high)
RANK_TITLES: list[str] = [
    "Greenbeard",
    "Rock Hauler",
    "Cave Runner",
    "Stone Breaker",
    "Pit Delver",
    "Rookie Miner",
    "Rookie Miner",
    "Authorized Miner",
    "Authorized Miner",
    "Senior Miner",
    "Senior Miner",
    "Professional Miner",
    "Professional Miner",
    "Veteran Miner",
    "Veteran Miner",
    "Expert Miner",
    "Expert Miner",
    "Elite Miner",
    "Elite Miner",
    "Elite Miner",
    "Supreme Miner",
    "Supreme Miner",
    "Supreme Miner",
    "Master Miner",
    "Master Miner",
    "Master Miner",
    "Epic Miner",
    "Epic Miner",
    "Epic Miner",
    "Epic Miner",
    "Legendary Miner",
    "Legendary Miner",
    "Legendary Miner",
    "Legendary Miner",
    "Legendary Miner",
    "Mythic Miner",
    "Mythic Miner",
    "Mythic Miner",
    "Mythic Miner",
    "Mythic Miner",
    "Stone Guard",
    "Stone Guard",
    "Stone Guard",
    "Stone Guard",
    "Stone Guard",
    "Honor Guard",
    "Honor Guard",
    "Honor Guard",
    "Honor Guard",
    "Honor Guard",
    "Iron Guard",
    "Iron Guard",
    "Iron Guard",
    "Iron Guard",
    "Iron Guard",
    "Giant Guard",
    "Giant Guard",
    "Giant Guard",
    "Giant Guard",
    "Giant Guard",
    "Night Carver",
    "Night Carver",
    "Night Carver",
    "Night Carver",
    "Night Carver",
    "Longbeard",
    "Longbeard",
    "Longbeard",
    "Longbeard",
    "Longbeard",
    "Gilded Master",
    "Gilded Master",
    "Gilded Master",
    "Gilded Master",
    "Gilded Master",
]

        
def __XpDataBuilder(marker) -> DataSource:
    return DataSource(marker,48)


def __PromoDataBuilder(XpData:DataSource) -> DataSource:
    return DataSource(XpData.marker, XpData.offset + 108)


class __XpAndPromoInfo:
    def __init__(self, marker) -> None:
        self.xp:DataSource = __XpDataBuilder(marker)
        self.promo:DataSource = __PromoDataBuilder(self.xp)

    def __update_pos(self,save_bytes)->None:
        self.xp_pos = self.xp.get_position(save_bytes)
        self.promo_pos = self.promo.get_position(save_bytes)
        
    def __update_value(self,save_bytes)->None:
        value_len = 4
        self.xp_value:int = int(struct.unpack("i", save_bytes[self.xp_pos : self.xp_pos + value_len])[0])
        self.promo_value:int = int(struct.unpack(
            "i",
            save_bytes[
                self.promo_pos: self.promo_pos + 4
            ],
        )[0])
        
    def update(self,save_bytes)->None:
        self.__update_pos(save_bytes)
        self.__update_value(save_bytes)


class XP(ReadFromBytes):
    __engineer: __XpAndPromoInfo   = __XpAndPromoInfo(b"\x85\xEF\x62\x6C\x65\xF1\x02\x4A\x8D\xFE\xB5\xD0\xF3\x90\x9D\x2E\x03\x00\x00\x00\x58\x50")
    __scout: __XpAndPromoInfo      = __XpAndPromoInfo(b"\x30\xD8\xEA\x17\xD8\xFB\xBA\x4C\x95\x30\x6D\xE9\x65\x5C\x2F\x8C\x03\x00\x00\x00\x58\x50")
    __driller: __XpAndPromoInfo    = __XpAndPromoInfo(b"\x9E\xDD\x56\xF1\xEE\xBC\xC5\x48\x8D\x5B\x5E\x5B\x80\xB6\x2D\xB4\x03\x00\x00\x00\x58\x50")
    __gunner: __XpAndPromoInfo     = __XpAndPromoInfo(b"\xAE\x56\xE1\x80\xFE\xC0\xC4\x4D\x96\xFA\x29\xC2\x83\x66\xB9\x7B\x03\x00\x00\x00\x58\x50")
    __data: dict[str, dict[str, int]]|None = None
    
    @staticmethod
    def read(self, save_bytes: bytes) -> None:
        XP.__engineer.update(save_bytes)
        XP.__scout.update(save_bytes)
        XP.__driller.update(save_bytes)
        XP.__gunner.update(save_bytes)
        
        XP.__data = {
            "driller":  {"xp": XP.__driller.xp_value,   "promo": XP.__driller.promo_value},
            "engineer": {"xp": XP.__engineer.xp_value,  "promo": XP.__engineer.promo_value},
            "gunner":   {"xp": XP.__gunner.xp_value,    "promo": XP.__gunner.promo_value},
            "scout":    {"xp": XP.__scout.xp_value,     "promo": XP.__scout.promo_value},
        }
    
    @staticmethod
    def data() -> None | dict[str, dict[str, int]]:
        return XP.__data
    
    @staticmethod
    def get_xp(dwarf:str) -> tuple[int,int,int] | None:
        """gets the total xp, level, and progress to the next level (rem)"""
        if XP.__data:
            if XP.__data.get(dwarf): # type: ignore
                total = XP.__data[dwarf]["xp"] # type: ignore
                level, rem = XP.xp_total_to_level(total)
            
            else:
                total = rem = level = -1 
        else:
            return None    
        return total, level, rem

    @staticmethod
    def update_xp(dwarf, total_xp=0)->bool:
        if XP.__data and XP.__data.get(dwarf): # type: ignore
            XP.__data[dwarf]["xp"] = total_xp
            return True
        else:
            return False
        
    @staticmethod
    def update_promos(driller_index,engineer_index,gunner_index,scout_index)->bool:
        if XP.__data:
            XP.__data["driller"]["promo"] = XP.__data["driller"]["promo"] if driller_index == MAX_BADGES else driller_index
            XP.__data["engineer"]["promo"] = XP.__data["engineer"]["promo"] if engineer_index == MAX_BADGES else engineer_index
            XP.__data["gunner"]["promo"] = XP.__data["gunner"]["promo"] if gunner_index == MAX_BADGES else gunner_index
            XP.__data["scout"]["promo"] = XP.__data["scout"]["promo"] if scout_index == MAX_BADGES else scout_index
            return True
        else: 
            return False
        
    @staticmethod
    def get_rank_title() -> str:
        default_str = "Classes - Rank 0 0/3, Lord of the Deep"
        #the original code had this in a try / except statement
        if XP.__data:
            dpromo:int = XP.__data["driller"]["promo"]
            epromo:int = XP.__data["engineer"]["promo"]
            gpromo:int = XP.__data["gunner"]["promo"]
            spromo:int = XP.__data["scout"]["promo"]
            
            dlvl:int = XP.get_xp("driller")[1] # type: ignore
            elvl:int = XP.get_xp("engineer")[1] # type: ignore
            glvl:int = XP.get_xp("gunner")[1] # type: ignore
            slvl:int = XP.get_xp("scout")[1] # type: ignore
            
            total_levels = (
                ((dpromo + epromo + gpromo + spromo) * 25)
                + dlvl + elvl + glvl + slvl
            )
            
            rank = total_levels // 3
            rem = total_levels % 3
            
            title = RANK_TITLES[rank] if rank in RANK_TITLES else "Lord of the Deep"
        
            return f"Classes - Rank {rank+1} {rem}/3, {title}"
        else:
            return default_str

    
    
    @staticmethod
    def xp_total_to_level(xp:int) -> tuple[int, int]:
        for i in XP_TABLE:
            if xp < i:
                level = XP_TABLE.index(i)
                remainder = xp - XP_TABLE[level - 1]
                return (level, remainder)
        return (25, 0)


