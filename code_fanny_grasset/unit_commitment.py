from math import trunc
from typing import Dict, List, Tuple
import payload_classes

POWERPLANT_TYPE_COST_CORR = {
    "gasfired": "gas(euro/MWh)",
    "turbojet": "kerosine(euro/MWh)",
}

def get_cost_MWh_and_effective_p(
    payload: payload_classes.Payload,
    powerplant_type_cost_corr: dict = POWERPLANT_TYPE_COST_CORR
) -> payload_classes.Payload:
    for i in range(len(payload.powerplants)):
        pp = payload.powerplants[i]
        pp.effective_pmin = trunc(10 * pp.efficiency * pp.pmin) / 10
        pp.effective_pmax = trunc(10 * pp.efficiency * pp.pmax) / 10
        if pp.type == payload_classes.EnergyType.windturbine:
            pp.effective_pmin = trunc(10 * pp.effective_pmin *
                                payload.fuels["wind(%)"] / 100) / 10
            pp.effective_pmax = trunc(10 * pp.effective_pmax *
                                payload.fuels["wind(%)"] / 100) / 10
            pp.cost_1MWh = 0
        else:
            pp.cost_1MWh = (payload.fuels[powerplant_type_cost_corr[pp.type]] /
                pp.efficiency)
    return payload

def get_merit_order(
    payload: payload_classes.Payload
) -> List[Tuple[payload_classes.Powerplant, float]]:
    order = [(pp, pp.cost_1MWh) for pp in payload.powerplants]
    order = sorted(order, key=lambda x: x[1])
    return order

def get_cheapest_energy_mix(
    payload: payload_classes.Payload,
    order: List[Tuple[payload_classes.Powerplant, float]]
) -> dict:
    load = payload.load
    result = {o[0].name: 0 for o in order}
    rest = load
    i = 0
    while rest != 0 and i < len(order):
        pp = order[i][0]
        if pp.effective_pmin <= rest:
            power = min(rest, pp.effective_pmax)
            result[pp.name] += power
            rest = round(rest - power, 1)

        i += 1
    return result

def main(payload: payload_classes.Payload) -> Dict:

    payload = get_cost_MWh_and_effective_p(payload)
    merit_order = get_merit_order(payload)
    mix = get_cheapest_energy_mix(payload, merit_order)

    return  mix

