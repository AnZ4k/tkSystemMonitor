from pysnmp.hlapi.v1arch.asyncio import *

import asyncio

async def _get_snmp(host: str, oid: str) -> list:
    with Slim(1) as slim:
        errorIndication, errorStatus, errorIndex, varBinds = await slim.get(
            'public',
            host,
            161,
            ObjectType(ObjectIdentity(oid)),
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
        else:
            return varBinds
        
        return []

def coleta_informacoes(addr: str) -> dict:
    clock_processador = int(asyncio.run(_get_snmp(addr, ".1.3.6.1.4.1.14988.1.1.3.14.0"))[0][1])
    temperatura_processador = int(asyncio.run(_get_snmp(addr, ".1.3.6.1.4.1.14988.1.1.3.100.1.3.17"))[0][1])
    pccpu_usage = {}
    core_usage = asyncio.run(_get_snmp(addr, ".1.3.6.1.2.1.25.3.3.1.2.1"))
    
    if core_usage:
        core_count = 0
        
        while core_usage != []:
            pccpu_usage[f"c{core_count}"] = int(core_usage[0][1])
            core_count += 1
            core_usage = asyncio.run(_get_snmp(addr, f".1.3.6.1.2.1.25.3.3.1.2.{core_count}"))
    
    counter = 0
    core_usage_sum = 0
    
    for _, core in pccpu_usage.items():
        counter += 1
        core_usage_sum += int(core)
    
    avg_core_usage = int(core_usage_sum / counter) 
    total_memory = int(asyncio.run(_get_snmp(addr, ".1.3.6.1.2.1.25.2.3.1.5.65536"))[0][1])
    used_memory = int(asyncio.run(_get_snmp(addr, ".1.3.6.1.2.1.25.2.3.1.6.65536"))[0][1])
    free_memory = total_memory - used_memory
    
    return {
        "cpu": {
            "clock": clock_processador,
            "temp": temperatura_processador,
            "usage": avg_core_usage,
            "pc_clock": [],
            "pc_temp": [],
            "pc_usage": pccpu_usage
        },
        "memory": {
            "total_size": total_memory,
            "used": used_memory,
            "free": free_memory,
            "frequency": 0
        }
    }    
        