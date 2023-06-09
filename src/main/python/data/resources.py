# handles stuff related to the players resources

import struct
from typing import Type

from main.python.data.data import DataSource, ReadFromBytes

RESOURCE_GUIDS = {
    "yeast": "078548B93232C04085F892E084A74100",
    "starch": "72312204E287BC41815540A0CF881280",
    "barley": "22DAA757AD7A8049891B17EDCC2FE098",
    "bismor": "AF0DC4FE8361BB48B32C92CC97E21DE7",
    "enor": "488D05146F5F754BA3D4610D08C0603E",
    "malt": "41EA550C1D46C54BBE2E9CA5A7ACCB06",
    "umanite": "5F2BCF8347760A42A23B6EDC07C0941D",
    "jadiz": "22BC4F7D07D13E43BFCA81BD9C14B1AF",
    "croppa": "8AA7FB43293A0B49B8BE42FFE068A44C",
    "magnite": "AADED8766C227D408032AFD18D63561E",
    "error": "5828652C9A5DE845A9E2E1B8B463C516",
    "cores": "A10CB2853871FB499AC854A1CDE2202C",
    "data": "99FA526AD87748459498905A278693F6",
    "phazyonite": "67668AAE828FDB48A9111E1B912DBFA4",
}
RESOURCE_MARKER = (
    b"OwnedResources"  # marks the beginning of where resource values can be found
)

def __ResourceDataBuilder(marker) -> DataSource:
    return DataSource(
        marker,
        offset=16 # length of GUIDs in bytes
    )
    
class Resources(ReadFromBytes):
    @staticmethod
    def read(save_bytes:bytes) -> dict[str, int]:
        # extracts the resource counts from the save file
        start_pos = save_bytes.find(RESOURCE_MARKER)
        value_len = 4 # offset for the actual value
        
        resource_data_dict: dict[str, DataSource] = {k:__ResourceDataBuilder(v) for k,v in RESOURCE_GUIDS.items()}
        return {
            k:int(
                struct.unpack(
                    "f",
                    save_bytes[
                        v.get_position(save_bytes,start_pos) : v.get_position(save_bytes,start_pos) + value_len
                    ] # search for the value
                )[0] # extract and unpack the value
            ) # save resource count
            for k,v in resource_data_dict.items()
        }