from os.path import join, isfile

import stackexchange
from wowspy.wowspy import Wows

from core.data_class import Data
from core.file_system import fopen_generic, read_json, read_all_files, \
    write_json, freadlines
from core.wows_core.wg_core import get_all_ship_tier
from core.wows_core.wtr_core import coeff_all_region


def data_factory():
    """
    Creates an instance of Data 
    :rtype: Data
    """
    api_keys = read_json(fopen_generic(join('data', 'beta_api_keys.json')))
    wows_api = Wows(api_keys['WoWs'])

    write_json(fopen_generic(join('data', 'na_ships.json'), 'w'),
               wows_api.warships(wows_api.region.NA))

    kanna_files = read_all_files(join('data', 'kanna_is_cute_af'))
    lewds = freadlines(fopen_generic(join('data', 'lewd.txt')))
    lewds.append('( ͡° ͜ʖ ͡°)')
    so = stackexchange.Site(stackexchange.StackOverflow, api_keys[
        'StackExchange'], impose_throttling=True)
    help_message = read_json(fopen_generic(join('data', 'help.json')))
    shame_list = read_json(fopen_generic(join('data', 'shamelist.json')))
    na_ships = read_json(fopen_generic(join('data', 'na_ships.json')))['data']

    coefficients, expected = coeff_all_region()

    ship_dict = get_all_ship_tier(wows_api)

    prefix_dict = read_json(fopen_generic(join('data', 'prefix.json')))

    avatar = open(join('data', 'avatar.png'), 'rb').read() \
        if isfile(join('data', 'avatar.png')) else None

    data = Data(api_keys=api_keys, kanna_files=kanna_files, lewds=lewds, so=so,
                help_message=help_message, shame_list=shame_list,
                na_ships=na_ships, coefficients=coefficients, expected=expected,
                ship_dict=ship_dict, wows_api=wows_api, prefix_dict=prefix_dict,
                avatar=avatar)
    return data
