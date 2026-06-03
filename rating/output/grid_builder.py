# output/grid_builder.py

def build_quote_grid(ctx):
    grid = []

    for v in ctx.vehicles:
        vidx = v.vehicle_index
        rates = ctx.vehicle_rate_parts.get(vidx, {})

        grid.append({
            "vehicleIndex": vidx,
            "liability": rates.get("liability"),
            "medpay": rates.get("medpay"),
            "pip": rates.get("pip"),
            "collision": rates.get("collision"),
            "comprehensive": rates.get("comprehensive"),
            "um": ctx.policy_rate_parts.get("um"),
            "uim": ctx.policy_rate_parts.get("uim"),
        })

    return grid