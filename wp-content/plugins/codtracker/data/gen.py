import json, re, sys

OUT = sys.argv[1]

# Sources
GR_LVL = "https://gamerant.com/cod-mw4-dmz-xp-level-rewards-unlocks/"
MR = "https://metaradar.gg/modernwarfare4/dmz/missions"
MW4W = "https://www.mw4wiki.com/dmz/"
GF = "https://www.gamerfuzion.com/modern-warfare-4-dmz-guides/"
CM = "https://codmunity.gg/dmz/guide"
CQ = "https://conquestcapped.com/guides/call-of-duty/mw4-dmz/"
CODW = "https://cod-mw4.wiki/"
GR_ORD = "https://gamerant.com/mw4-dmz-orders-how-to-complete-all-rewards/"
DG = "https://dmzguides.xyz/orders/"
GF_P21 = "https://www.gamerfuzion.com/modern-warfare-4-dmz-orders-page-21-hard-carry-stalking-the-stalker-deathstalker-sam-site-solo/"
CQB = "https://conquestcapped.com/guides/call-of-duty/mw4-dmz-bosses/"
GR_BOSS = "https://gamerant.com/call-of-duty-cod-modern-warfare-4-mw4-dmz-boss-locations-lieutenants-commanders/"
SG = "https://showgamer.com/en/guides/7057-modern-warfare-4-dmz-vse-komnaty-leytenantov-klyuchi-i-oruzhie"
ATH = "https://allthings.how/modern-warfare-4-dmz-key-locations-which-door-each-key-opens/"
CC_TR = "https://codcentral.net/blog/mw4-dmz-traits/"
CC_CAMO = "https://codcentral.net/blog/mw4-dmz-camo-challenges/"
CM_PROG = "https://codmunity.gg/dmz/progression"
GF_S1 = "https://www.gamerfuzion.com/modern-warfare-4-dmz-season-1-x01-black-site-deep-vault-new-bosses-november-6/"
DMZHUB_X01 = "https://dmzhub.gg/guides/x01-dmz-map-season-1-guide"
ATH_STASH = "https://allthings.how/how-to-increase-stash-space-and-bank-limit-in-mw4-dmz-upgrade-costs/"
CQ_FOB = "https://conquestcapped.com/guides/call-of-duty/mw4-dmz-fob/"
POWERPYX = "https://www.powerpyx.com/call-of-duty-modern-warfare-4-2026-trophy-guide-roadmap/"
CODW_ACH = "https://cod-mw4.wiki/guide/cod-mw4-achievements"
DMZT_PT = "https://www.dmztracker.gg/guides/prestige-traits/"
GF_TRAITS = "https://www.gamerfuzion.com/modern-warfare-4-dmz-best-traits-solo-squads-possum-prestige-pro-traits/"
DMZMAP_DO = "https://dmzmap.com/guides/dynamic-ops"
MW4BUZZ_SO = "https://mw4.buzz/guides/mw4-dmz-side-ops/"
GR_3DP = "https://gamerant.com/mw4-dmz-all-3d-printer-recipes-locations-ingredients/"
GPM_3DP = "https://gamingpromax.com/modern-warfare-4-dmz-all-3d-printer-recipes/"
CM_CRAFT = "https://codmunity.gg/dmz/crafting"
GF_3DP = "https://www.gamerfuzion.com/modern-warfare-4-dmz-3d-printer-crafting-recipes-costs-resources-ingredients/"
MR_CRAFT = "https://metaradar.gg/modernwarfare4/dmz/crafting"
GG_X01P = "https://games.gg/call-of-duty-modern-warfare-4/guides/how-to-print-legendary-materials-in-x01/"
CQ_WM = "https://conquestcapped.com/guides/call-of-duty/mw4-dmz-weapon-manuals/"
GG_WM = "https://games.gg/call-of-duty-modern-warfare-4/guides/dmz-weapon-manuals-locations/"

categories = []
items = []


def cat(slug, name, parent=None, description=""):
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug), slug
    categories.append({"slug": slug, "name": name, "parent": parent,
                       "description": description,
                       "order": sum(1 for c in categories if c["parent"] == parent) + 1})


def item(category, title, description="", requirement="", reward="", location="",
         confirmed=False, sources=(), goal=None):
    row = {"title": title, "category": category, "description": description,
           "requirement": requirement, "reward": reward, "location": location,
           "confirmed": bool(confirmed), "sources": list(sources),
           "order": sum(1 for i in items if i["category"] == category) + 1}
    if goal is not None:
        row["goal"] = goal
    items.append(row)


# ---------------------------------------------------------------- Story missions
cat("story-missions", "Story Missions", None,
    "Operations chosen at the Deploy station. Each reportedly pays 25,000 DMZ Cash plus an item/unlock. Official trailer showed six mission markers.")
item("story-missions", "Operation Silent Ledger",
     "Breach the casino vault and secure the printing plates.",
     "Required for Orders Counterfeit 2/2 (Page 6).",
     "25,000 DMZ Cash, Gold Bar, Polaris Dagor A1 (infil/vehicle), Counting Room Vault key",
     "Heavenly Luck Casino, Cheongun Village", True, [MR, MW4W, GF, CM, CQ, ATH])
item("story-missions", "Operation Shopping Hacks",
     "Hack Lieutenant Jang-ui's encampment/network, break into the K9 lab, loot the vault, exfil by balloon.",
     "Required for Orders Underground 2/2 (Page 9).",
     "25,000 DMZ Cash, Night Vision Goggles, Coin Mining Den key. Field Depot key also reported as a guaranteed reward by one source.",
     "NuriGO Mall", True, [MR, MW4W, GF, CM, CQ, ATH])
item("story-missions", "Operation Critical Extraction",
     "Find General Kang and push his bed to the exfil chopper alive.",
     "Required for Orders Human Intel 2/2 (Page 3).",
     "25,000 DMZ Cash, Defibrillator (recipe per metaradar; item per conquestcapped), Mirae Electrical Room key",
     "Mirae General Hospital", True, [MR, GF, CM, CQ, ATH])
item("story-missions", "Operation Iron Citadel",
     "Get the access card and armory code, destroy three jets, capture the SAM site (objectives from metaradar, reported).",
     "Reportedly unlocks after Silent Ledger, Shopping Hacks and Critical Extraction. Required for Orders Hornet's Nest 2/2 (Page 17).",
     "LTV infil unlock, 25,000 DMZ Cash, Bunker Access key, ~12,500 XP (reported)",
     "Chang-san Air Base", True, [MR, MW4W, GF, CM, CQ])
item("story-missions", "Operation Grid Assault",
     "Assemble a kill code and broadcast it from a radio tower (objectives reported).",
     "Required for Orders The Grid 2/2 (Page 13).",
     "Helicopter infil unlock, 25,000 DMZ Cash, Armory key (reported)",
     "The Grid, DBN Headquarters, Hotel Lucera", True, [MR, MW4W, GF, CM, CQ])
item("story-missions", "Operation Fallen Ember",
     "Recover fuel rods and a warhead, escape by boat (objectives reported). Described as the last story mission.",
     "Required for Orders Page 21.",
     "Cargo Plane infil (reported), Reactor key, 25,000 DMZ Cash, ~12,500 XP (reported)",
     "Haneul Nuclear Reactor", True, [MR, CM, GR_ORD, DG])

# ---------------------------------------------------------------- DMZ Orders
cat("dmz-orders", "DMZ Orders", None,
    "Order pages taken from the FOB DMZ Orders laptop. Each page pays 20,000 DMZ Cash plus gear. Page numbering may vary by account (one player reported Hornet's Nest as pages 22-23). Completing all Orders reportedly unlocks a secret Ghost cutscene (Game Rant).")

orders = [
    ("orders-page-1", "Page 1: Getting Started", "Medkit, 2-Plate Armor Vest", True, [
        ("Gear Up", "Equip a weapon, backpack, armor vest and medkit from your Stash.", ""),
        ("Crack Shot", "Knock down 3 targets at the FOB Firing Range.", "FOB Firing Range"),
        ("First Op", "Deploy into DMZ in Dynamic Ops.", ""),
    ]),
    ("orders-human-intel-1", "Page 2: Human Intel 1/2", "Flash Grenade recipe, Basic Triage Kit", True, [
        ("Hunter", "Climb a Lieutenant Hunt Tower and use the terminal to locate the nearest Lieutenant.", ""),
        ("Triage Protocol", "Visit a Clinic, loot a Bandage, loot 30 Chemicals.", "Clinic"),
        ("No One Left", "Clear a Compound and loot the Medical Extraction Intel.", "Compound"),
    ]),
    ("orders-human-intel-2", "Page 3: Human Intel 2/2", "UAV x3, Operator Rescue Beacon, Weapon Insurance Contract", True, [
        ("Blindness", "Print 4 Flash Grenades and kill 8 enemies affected by them.", ""),
        ("Payment Due", "Collect a Dynamic Op Phone (Free Roam) and earn 11,500 DMZ Cash from Dynamic Ops.", ""),
        ("Operation Critical Extraction", "Complete the story mission (counts if already done).", "Mirae General Hospital"),
    ]),
    ("orders-page-4", "Page 4: Printing & Dynamic Ops", "Medium Backpack, Ammo Box", True, [
        ("Operation Rewards", "Collect a Dynamic Op Phone in Cheongun Village, complete a Dynamic Op, loot its crate.", "Cheongun Village"),
        ("Preparation", "Print a Medium Backpack and a 2-Plate Armor Vest.", "FOB 3D Printer"),
        ("Work Quietly", "Gunsmith a suppressor onto a weapon, print a Throwing Knife, kill 8 enemies in a row without taking damage.", ""),
    ]),
    ("orders-counterfeit-1", "Page 5: Counterfeit 1/2", "Recon Drone recipe, Explosives Equipment Kit", True, [
        ("Hostile Force", "Enter a Police Station, search 3 containers, eliminate 5 soldiers inside.", "Police Station (e.g. NuriGO Mall, Wolves Stadium)"),
        ("Robbery", "Open a Safe and extract with 5,000+ backpack/loadout value.", ""),
        ("Execute Intel", "Hack a UAV Tower in Deadtown, kill 5 NK soldiers it pings, loot the Counterfeit Cash they drop.", "Deadtown"),
    ]),
    ("orders-counterfeit-2", "Page 6: Counterfeit 2/2", "Operator Rescue Beacon, Weapon Insurance Contract", True, [
        ("Suit Breach", "Kill 15 enemies wearing Hazmat Suits.", ""),
        ("Eyes Everywhere", "Print a Recon Drone and mark 10 enemies in the Heavenly Luck Casino with it.", "Heavenly Luck Casino"),
        ("Operation Silent Ledger", "Complete the story mission.", "Heavenly Luck Casino"),
    ]),
    ("orders-page-7", "Page 7: Radiation & Medical", "UAV, Armor Box", True, [
        ("Recognition", "Kill 15 enemies with an unsuppressed weapon in a High Threat Level location.", ""),
        ("Radiation Station", "Enter a Fire Station, loot 3 Gas Masks or Radiation Pill Bottles, search 5 containers while in radiation.", "Fire Station"),
        ("Healer", "Print a Medkit.", "FOB 3D Printer"),
    ]),
    ("orders-underground-1", "Page 8: Underground 1/2", "DDOS recipe, Decoy Grenade recipe, Night Vision Goggles recipe", True, [
        ("Eye in the Sky", "Capture a SAM Site, shoot down a cargo-carrying chopper, loot its crate.", "SAM Site"),
        ("Watch for Bumps", "Steal an enemy vehicle, refuel and repair at a Gas Station, run over 7 enemies.", "Gas Station"),
        ("Triangulation", "Place transmitters on 2 Radio Towers and on La Grande Vie.", "Songdo Wharf (La Grande Vie)"),
    ]),
    ("orders-underground-2", "Page 9: Underground 2/2", "Basic Restock Kit, Operator Rescue Beacon, Weapon Insurance Contract", True, [
        ("Dead Battery", "Print a DDOS Field Upgrade and disable 3 enemy vehicles or drones with it.", ""),
        ("Death From Above", "Trick a drone with a Decoy Grenade, destroy 3 drones, loot a Drone Motherboard.", ""),
        ("Operation Shopping Hacks", "Complete the story mission.", "NuriGO Mall"),
    ]),
    ("orders-page-10", "Page 10: Supply & Salvage", "Large Backpack, Basic Triage Kit", True, [
        ("Crashed Crate", "Retrieve 3 Lost Supply Drops and complete a Loot Radio Tower Side Op (one source says near D8).", ""),
        ("Surprise Me", "Complete 5 Dynamic Ops and a Story Mission via Random Mission Deploy.", ""),
        ("Healer (Page 10)", "Print or extract 3 Reactive Metals, extract with 30 Metals, print an Armor Box. (Game Rant lists only the Reactive Metals step.)", ""),
    ]),
    ("orders-page-11", "Page 11: Boss Board & Gunsmith", "Defibrillator, Inflatable Decoy, C4 recipe", True, [
        ("Information Power", "Buy Lieutenant intel on the FOB Boss Board and kill that Lieutenant.", "FOB Boss Board"),
        ("Arms Deal", "Buy a gun from the Gunsmith and Gunsmith a weapon with 3+ attachments.", "FOB Gunsmith"),
        ("Friendly Face", "Use the ping wheel to request a Truce. Name reported as 'Friendly Force' (Game Rant) or 'Friendly Face' (dmzguides).", ""),
    ]),
    ("orders-the-grid-1", "Page 12: The Grid 1/2", "3-Plate Armor Vest recipe, Triage Kit (sources disagree on the vest)", True, [
        ("I'm Over Here", "Distract a drone with an Inflatable Decoy; destroy 8 Combat Drones and 3 Heavy Combat Drones.", ""),
        ("Worth Every Penny", "Buy a DMZ Vendor weapon; get 50 kills with a Rare or better weapon.", ""),
        ("No Time", "Complete any Dynamic Op in under 8 minutes.", ""),
    ]),
    ("orders-the-grid-2", "Page 13: The Grid 2/2", "Recon Equipment Kit, Operator Rescue Beacon, Weapon Insurance Contract", True, [
        ("Opulent", "Complete 6 Side Ops in one deployment.", ""),
        ("Civil Service", "Enter NuriGO Mall, locate City Hall, extract with Financial Ledger Fragments (2nd floor).", "NuriGO Mall / City Hall"),
        ("Operation Grid Assault", "Complete the story mission.", "The Grid"),
    ]),
    ("orders-page-14", "Page 14: Lethals & Safes", "Structural Alloy x2, Stock Rod x2", True, [
        ("Lethal Tools", "Print 6 Lethal Equipment and kill 13 enemies with it.", ""),
        ("Committed", "Exfil after radiation has begun spreading (25+ minutes).", ""),
        ("Nothing Is Secure", "Open 4 Safes and extract with $20,000 backpack/loadout value.", ""),
    ]),
    ("orders-page-15", "Page 15: Vehicles & Stealth", "CPU x2, Nylon Cloth x2, Inflatable Decoy", True, [
        ("Fire Insurance", "Print 5 Thermite and stick 5 (occupied) enemy vehicles.", ""),
        ("Quiet", "Loot 10 containers in The Grid without taking damage.", "The Grid"),
        ("Mechanic", "Repair a Radar Truck and kill 19 enemies it pings.", ""),
    ]),
    ("orders-hornets-nest-1", "Page 16: Hornet's Nest 1/2", "Large Backpack recipe, Weapon Restock Kit", True, [
        ("Goliath", "Hit the Colossus with Thermite or a Drill Charge, and with a Shock Stick.", ""),
        ("Click, Boom", "Print 5 C4; kill 12 armored enemies with C4; kill 5 enemies with a single C4.", ""),
        ("Navigate With Care", "Buy the Polaris Dagor A1 infil, clear a North Korean Convoy, extract its Chemical Components.", ""),
    ]),
    ("orders-hornets-nest-2", "Page 17: Hornet's Nest 2/2", "Helmeted Armor Kit (one source: Armor Survival Kit), Operator Rescue Beacon, Weapon Insurance Contract", True, [
        ("Jail Break", "Kill 15 enemies in the 14th Political Prison, destroy a Reinforcement Helicopter, kill 10 enemies in the Citadel.", "14th Political Prison"),
        ("Keep Out", "Kill 3 Lieutenants, loot a Lieutenant's Key, loot the Lieutenant's gun in their room.", ""),
        ("Operation Iron Citadel", "Complete the story mission.", "Chang-san Air Base"),
    ]),
    ("orders-page-18", "Page 18: Armor, K9s & Keys", "Nitro Compounds x2, SERE Kit", True, [
        ("How Bulletproof?", "Kill 30 enemies, 15 armored enemies and 5 Lieutenants.", ""),
        ("Abandoned", "Enter the NuriGO Mall Underground, kill 10 K9s, extract 3 Pristine K9 Battery Cores.", "NuriGO Mall Underground"),
        ("Locksmith", "Loot 5 keys and unlock 3 locked spaces.", ""),
    ]),
    ("orders-page-19", "Page 19: Avionics & Ops", "Binding Catalyst x2, Explosives Equipment Kit", True, [
        ("Avionics", "Print or extract 5 Electronic Sensors, extract 1 Structural Alloy, print a UAV.", ""),
        ("Philanthropist", "Complete the Weekly Random Mission Deploy challenge (three random Story Missions).", ""),
        ("Multi-Talented", "Capture 6 SAM Sites, open 12 Supply Drops, clear 4 Compounds.", ""),
    ]),
    ("orders-page-20", "Page 20: Vaults & Tanks", "Reported: 20,000 DMZ Cash, 3-Plate Armor Vest, Bomb Glider (Game Rant lists no reward)", True, [
        ("Ears Everywhere", "Hack the DBN TV Building broadcast system at Cheonwang Peak Array and loot the Encrypted Voice Logs.", "Cheonwang Peak Array"),
        ("The Vault", "Restore power at the Hanex Branch Bank with a Car Battery, find the Access Card and 3 password notes, open the vault.", "Hanex Branch Bank"),
        ("Massive Damage", "Disable the Tank's reactive armor with DDOS (3 uses reported), hit it with a rocket, destroy it.", "The Grid"),
    ]),
    ("orders-page-21", "Page 21: Backpacks & Deathstalkers", "Reported: Triage Kit or Basic Triage Kit, Operator Rescue Beacon, Weapon Insurance Contract (Game Rant lists no reward)", True, [
        ("Hard Carry", "Print or extract 2 Nylon Laminate, extract Structural Alloy, print a Large Backpack. Structural Alloy count reported as 2 (Game Rant) or 5 (dmzguides).", ""),
        ("Stalking the Stalker", "Destroy Deathstalkers: with a SAM Site (1 per Game Rant, 3 per dmzguides), with a launcher, and (per dmzguides/gamerfuzion) disable one with DDOS. Task count disputed (2 vs 3).", "The Grid"),
        ("Operation Fallen Ember", "Complete the story mission.", "Haneul Nuclear Reactor"),
    ]),
    ("orders-page-22", "Page 22: Lockers & Radiation", "Reported: High-Tenacity Fibers x2, Trap Equipment Kit or Explosives Kit (sources disagree; Game Rant lists no reward)", True, [
        ("DRC", "Loot a DRC Weapons Locker (requires an Ultra DRC key).", ""),
        ("Unstoppable", "Kill 10 Commanders and 15 Lieutenants; extract 5 Lieutenant Dog Tags.", ""),
        ("Astronaut", "Loot containers in radiation (21 per dmzguides) without radiation damage at Haneul Nuclear Reactor; extract on the final exfil (3 times per dmzguides/metaradar).", "Haneul Nuclear Reactor"),
    ]),
    ("orders-page-23", "Page 23: Side Jobs", "Printed Circuit Board x2, Recon Equipment Kit", True, [
        ("Rule of Three", "Print or extract 2 Ballistic Fabric, extract 5 Nylon Cloth, print a 3-Plate Carrier.", ""),
        ("Temp Job", "Complete 40 Side Ops.", ""),
        ("No Time (Page 23)", "Complete 4 Dynamic Ops in one deployment.", ""),
    ]),
    ("orders-page-24", "Page 24: Loot, Snipers & Cash", "Gold Bar x2, Advanced SERE Kit (final Hajin page)", True, [
        ("High Quality Loot", "Extract 2 Weapon Manuals, 4 Recipes and an Ultra-rarity weapon.", ""),
        ("You Won't See Me", "Build a sniper rifle with 5+ attachments and get 100 kills with it.", ""),
        ("Upper Class", "Earn 250,000 DMZ Cash from Story Missions and Dynamic Ops.", ""),
    ]),
    ("orders-x01-1", "X01 Page 1: X01 1/5", "Reported (single source): Medium Scavenger Backpack, Encodable Blank Keycard x2", False, [
        ("Fresh Start", "Infil into X01.", "X01"),
        ("Sight Seeing", "Search 5 unopened containers in the Main Warehouse and 5 in the Control Room.", "X01"),
        ("First Win", "Extract from X01.", "X01"),
    ]),
    ("orders-x01-2", "X01 Page 2: X01 2/5", "Reported: Consumable Box recipe, Medical Box recipe", False, [
        ("Explorer", "Find the hidden stash in Production Assembly; search 5 unopened containers in the Tech Lab.", "X01"),
        ("Crafting Material", "Visit the X01 3D Printer and any Keycard Encoder Station.", "X01"),
        ("Video Footage", "Find Ri's video footage in the surveillance room at the Admin Offices.", "X01 Admin Offices"),
    ]),
    ("orders-x01-3", "X01 Page 3: X01 3/5", "Reported: Specter Fabric Sample, Hazmat Box recipe", False, [
        ("Streaming Service Ep. 1", "Intercept Ri's video feed in the Control Room; kill 10 enemies there.", "X01 Control Room"),
        ("Streaming Service Ep. 2", "Intercept the feed in the Medical Wing; loot 10 healing items there.", "X01 Medical Wing"),
        ("Streaming Service Ep. 3", "Extract Ri's video log in the Data Center; kill 3 Robot Dogs in X01.", "X01 Data Center"),
    ]),
    ("orders-x01-4", "X01 Page 4: X01 4/5", "Reported: 3-Plate Ballistic Gel Vest, SR-16 Bio Agent Sample, Staff Emergency Exfil Keycard recipe", False, [
        ("Racing the Hour", "Override the bioweapon release in the Bio Lab canister chamber.", "X01 Bio Lab"),
        ("The Vault (X01)", "Kill The Captain and take the X01 Vault Access Keycard from his body.", "X01"),
        ("Complete Defusal", "Enter the Deep Vault, neutralize the bioweapon in the core room, kill Blix.", "X01 Deep Vault"),
    ]),
    ("orders-x01-5", "X01 Page 5: X01 5/5", "Reported: Argonaut Armor, Large Scavenger Backpack, Parachute", False, [
        ("Door Opener", "Destroy the Wheelson in the Logistics Tunnel; cut power at the Power Generators.", "X01 Logistics Tunnel"),
        ("Water Wading", "With power cut, enter the flooded barracks under the Supply Depot; collect the Super User Data Access Keycard and extract.", "X01 Supply Depot"),
        ("Source Code", "Download the malicious AI source code in the Data Center dark room and extract in the same match.", "X01 Data Center"),
    ]),
]
for slug, name, reward, conf, objs in orders:
    is_x01 = slug.startswith("orders-x01")
    late = name.split(":")[0] in ("Page 20", "Page 21", "Page 22", "Page 23", "Page 24")
    cat(slug, name, "dmz-orders", "Page reward: 20,000 DMZ Cash + " + reward + ".")
    for t, d, loc in objs:
        if is_x01:
            srcs = [DG, GF]
        elif late:
            srcs = [GR_ORD, DG] + ([GF_P21] if slug == "orders-page-21" else [])
        else:
            srcs = [GR_ORD, DG, MR]
            if slug.startswith("orders-counterfeit-1"):
                srcs += [MW4W, CM]
            if slug == "orders-human-intel-1":
                srcs += [CM, GF]
        item(slug, t, d, "Order on " + name, "", loc, conf, srcs)

# ---------------------------------------------------------------- Dynamic Ops
cat("dynamic-ops", "Dynamic Ops", None,
    "Multi-step operations chosen before infil or started from a Dynamic Op Phone. Payouts pre-Oct 30 were ~3,000-10,000 Cash; deploy menu now promises 10,000-20,000. No official full list; community-compiled.")
dyn = [
    ("Signal Breaker", "Collect bomb parts, craft the bomb (Namjin Riverside reported), plant on 3 radar trucks.", "~6,000 XP, 10,000 DMZ Cash", "North Korean Wilderness, Deadtown, Imjin Farmland", True),
    ("Dead Man's Cache", "Find a cache, unlock the HVT's keypad, get a bomb, plant it, kill the HVT.", "Payout reported as ~5,100 XP / 9,900 Cash (metaradar) or 4,575 XP / 7,500 Cash (other guide)", "South Korean shoreline, Songdo Wharf", True),
    ("Special Delivery", "Gather bomb parts, craft, capture a UAV Tower, plant on a launcher, defend.", "~5,000 XP, 7,500 DMZ Cash; unlocks Mojave .357", "Songdo Wharf, Construction Zone, South Island", True),
    ("Ghost Shipment", "Eliminate a target, take orders, capture a SAM site, wait for a helicopter to go down.", "~5,000 XP", "Deadtown, Mirae General Hospital", True),
    ("Viral Reckoning", "Kill the HVT carrying a radio, rescue a scientist (keypad door), defend the LZ, plant a bomb on the bioweapon (or leave by helicopter for partial reward).", "~4,950 XP, 7,500 DMZ Cash", "14th Political Prison or South Korean border", True),
    ("Toxic Intercept", "Decrypt a drive, hijack a fuel tanker, deliver it.", "~4,500 XP", "South Korean border, Oamsik Turtle Island, NuriGO Mall", True),
    ("Broken Resupply", "Hack a comms server, loot a bomb, open a safe for a code, plant the bomb. Repeat completions in one deployment raise the supply drop tier (Common > Uncommon > Rare).", "~3,000 XP, 5,000 DMZ Cash, Supply Drop; unlocks ISO Nightshade", "Cheongun Village, Compound Charlie; seen near Imjin Suburb (D6)", True),
    ("Chemical Denial", "Collect 3 chemical components, craft at a workbench, deposit in a metal case.", "~3,300 XP", "Jayon Warehouses, Hanrim Village", True),
    ("Domino Protocol", "Chain of eliminations ending with a Lieutenant. Details not reported.", "", "", True),
    ("Sky Heist", "Take intel, approach a High-threat SAM site; gives your squad a private helicopter. Later steps not reported.", "", "Imjin Farmland, Compound Alpha", True),
    ("Ignition Point", "Reach the target area. Later steps not reported.", "", "North Fork of the Hajin River", True),
    ("Hunt Operator", "PvP op: hunt a full squad of real players in a high-threat zone before a countdown ends. Also called 'Hunt Operators'.", "DMZ XP, DMZ Cash, Supply Drop", "", True),
]
for t, d, r, loc, c in dyn:
    item("dynamic-ops", t, d, "Select before infil or pick up a Dynamic Op Phone", r, loc, c, [MR, DMZMAP_DO] + ([MW4W] if t in ("Broken Resupply", "Hunt Operator") else []) + ([CM, GF] if t in ("Dead Man's Cache", "Chemical Denial") else []) + ([CQ] if t == "Sky Heist" else []))

# ---------------------------------------------------------------- Side Ops
cat("side-ops", "Side Ops", None,
    "Low-intensity map activities. Since the Oct 30 update a Side Op reportedly pays 2,000 DMZ Cash.")
for t, d in [
    ("UAV Tower", "Hack/activate a UAV tower to ping nearby enemies."),
    ("Lieutenant Hunt Tower", "Climb the tower and use the terminal to locate the nearest Lieutenant."),
    ("SAM Site", "Capture a SAM site; can shoot down cargo choppers and Deathstalkers."),
    ("Lost Supply Drop", "Find and loot a lost supply crate."),
    ("Truck Repair", "Repair a truck (e.g. Radar Truck, which pings enemies)."),
    ("Radio Tower (Loot)", "Climb a radio tower and loot it."),
    ("Dynamic Op Phone", "Collect a Dynamic Op Phone to start a Dynamic Op in free roam."),
    ("Crack Safe", "Reported side op: crack a safe."),
]:
    item("side-ops", t, d, "", "2,000 DMZ Cash (post Oct 30, reported)", "", t != "Crack Safe", [MR, CM, MW4BUZZ_SO])

# ---------------------------------------------------------------- Bosses
cat("bosses", "Bosses & Boss Board", None,
    "Lieutenants and Commanders. Boss Board at the FOB unlocks after the 2nd DMZ Order; intel costs 25,000 DMZ Cash, lasts one deployment, guarantees the Lieutenant spawns. Some intel requires finishing a DMZ Orders chapter. Boss count reported as 10 bosses (gamerfuzion), 13 (conquestcapped) or 18 since Season 1.")
cat("bosses-lieutenants", "Lieutenants (Hajin)", "bosses", "Each pays a 10,000 DMZ Cash first-kill bounty and drops Dog Tags (~25,000 Cash per tag reported).")
cat("bosses-commanders", "Commanders", "bosses", "No purchasable intel, no dog tags; first kill reportedly ~50,000 DMZ Cash (conquestcapped) and rare 3D Printer ingredients.")
cat("bosses-x01", "X01 Bosses (Season 1)", "bosses", "Season 1 (Nov 6) X01 Black Site bosses.")
cat("bosses-boss-board", "Boss Board Challenges", "bosses", "")
lts = [
    ("Gorani", "Sniper Lieutenant. Location reported as Mujin Pass (Game Rant) or the forest between Cheonwang Peak Array and Mirae General Hospital / Hanrim Village (others).", "MAR-9 Marksman Rifle (unique 'Incisor'), Dog Tags, Gorani's Scout Overlook key", "Mujin Pass / South Korean Wilderness"),
    ("The Chemist", "Inside the radiation zone. Weapon reported as Kastov 762 (conquestcapped, showgamer 'Chemical Reaction') vs Oris 8.6 Legendary Blueprint (Game Rant).", "Kastov 762 or Oris 8.6 blueprint (conflict), Dog Tags, The Chemist's Secure Armory key", "Haneul Nuclear Reactor"),
    ("Jin-Tae", "Intel reportedly requires the Counterfeit Orders chapter.", "ISO Nightshade Legendary Blueprint 'High Roller's Fortune', Dog Tags, Jin-Tae's Private Lounge key", "Heavenly Luck Casino, Cheongun Village"),
    ("The Doctor", "Tied to Operation Critical Extraction.", "Patriot XMR Legendary Blueprint ('Doctor's Salvo'), Dog Tags, The Doctor's Command Office key", "Mirae General Hospital"),
    ("Bale", "Location reported as Re-Education Center (Deadtown) or Chang-san Air Base bunker / Tank Depot.", "Type 73 LMG ('Dreadnought'), Dog Tags (Bale's Dog Tag listed Legendary), Supreme Leader's Bunker Access Card", "Re-Education Center or Chang-san Air Base"),
    ("Iskra", "", "Warlord shotgun (rarely 'Widow Maker' blueprint), Dog Tags, Iskra's Control Room key", "Cheonwang Peak Array"),
    ("Scavenger", "No fixed spawn: reported as spawning near dead players (Game Rant) or driving an LTV around Hajin (conquestcapped). Use Lieutenant Hunt Towers. Showgamer calls him Krueger.", "Oris 8.6 Marksman Rifle ('Revenant'), Dog Tags; no key room", "Roaming"),
    ("Roze", "Location reported as DBN tower roof / DBN Headquarters, or Netshin Tech Complex floor 14 (key room). Sometimes spelled 'Rose'.", "Astaroth .57 Legendary Blueprint ('The Kraken'), Dog Tags, Roze's Highrise Armory key", "The Grid (DBN Headquarters)"),
    ("Jang-Ui", "Linked to Operation Shopping Hacks. Location reported as Netshin Tech Complex upper floors.", "Hyeon Burst AR ('Paektu'), Dog Tags, Jang-ui's Converted Power Room key", "Netshin Tech Complex / NuriGO Mall"),
    ("The Warden", "Patrols the Citadel.", "X-58 NYX SMG Legendary Blueprint ('Incarcerator'), Dog Tags; room 'Kang's Arms Incinerator' (access method not reported)", "The Citadel, 14th Political Prison"),
]
for t, d, r, loc in lts:
    item("bosses-lieutenants", t, d, "Find via Lieutenant Hunt Tower or buy intel (25,000) at the Boss Board", r, loc, True, [CQB, GR_BOSS, SG, CQ])
for t, d, r, loc in [
    ("Colossus", "Minigun-wielding heavy. Roams; reported spawns include The Grid, Wolves Stadium, SAM sites, Cheonwang Peak Array, Chang-San Air Base Armory, Cheongun Village, Songdo Wharf.", "Military Composites (Legendary ingredient), Experimental Compounds", "Roaming"),
    ("Deathstalker", "Autonomous drone helicopter. Most often over downtown Hajin / NuriGO Mall / DBN HQ.", "Prototype RF Module (Legendary ingredient), Experimental Compounds", "Hajin City"),
    ("North Korean Battle Tank", "Patrols roads, often The Grid. DDOS disables reactive armor. Threat-briefing event.", "Nano-Structured Alloy, Experimental Compounds", "Roads / The Grid"),
]:
    item("bosses-commanders", t, d, "Commanders appear on the map when close", r, loc, True, [CQB, GR_BOSS, CQ, CM])
for t, d, r, loc, c in [
    ("The Captain", "Commander. Juggernaut with elite guard, top floor / Main Warehouse / Logistics Tunnel. Threat Briefing: collect sections of The Captain's helmet and extract.", "Deep Vault Access Key / X01 Vault Access Keycard, Experimental Compounds", "X01", True),
    ("Wheelson", "Commander. Patrols lower levels / Logistics Tunnel; appears ~5 minutes in.", "Power Regulator, Remote Module (opens an emergency exfil gate)", "X01 Logistics Tunnel", True),
    ("Knuckle (Tae-Hyun)", "Lieutenant in the dark Data Center server room (night vision advised). Name reported as Tae-Hyun (Game Rant) and Knuckle (other guides).", "Rezi 12 Legendary Blueprint, Dog Tags, random Deep Vault key", "X01 Data Center", True),
    ("The Wrench (Chol-Min)", "Lieutenant hiding among tanks in the Motor Pool.", "Type 73 Legendary Blueprint, Dog Tags, random Deep Vault key", "X01 Motor Pool", True),
    ("Blix", "Lieutenant found only in the Deep Vault (not every match reported). Requires Deep Vault access.", "Rezi 12 Legendary Blueprint, Dog Tags", "X01 Deep Vault", True),
]:
    item("bosses-x01", t, d, "Season 1 X01 deployment", r, loc, c, [GR_BOSS, DMZHUB_X01, GF_S1])
for t, d in [
    ("Kill every Lieutenant once", "Boss Board challenge."),
    ("Extract each Lieutenant's Dog Tags 2 times", "Boss Board challenge tier."),
    ("Extract each Lieutenant's Dog Tags 5 times", "Boss Board challenge tier."),
]:
    item("bosses-boss-board", t, d, "", "", "FOB Boss Board", False, [CQ])

# ---------------------------------------------------------------- Level rewards
cat("level-rewards", "DMZ Level Rewards", None,
    "DMZ player level 1-70. Game Rant says DMZ has 77 levels but lists only 2-70; codmunity covers 1-70 only.")
lv = {
    1: ("3D Printer station; recipes: 1-Plate Armor Vest, Bandage, Small Backpack, Medkit (codmunity). Game Rant lists nothing at Level 1 and puts all of this at Level 2.", False),
    2: ("Recipes: 2-Plate Armor Vest, Medium Backpack (codmunity). Game Rant: 3D Printer station + 1-Plate Vest, Bandage, Small Backpack, Medkit, 2-Plate Vest, Medium Backpack recipes. Conquestcapped/codmunity guide say 3D Printer unlocks at Level 2.", False),
    3: ("Sedative Inhaler recipe", True),
    4: ("Reece operator skin; 3D Printer Tacticals upgrade; Smoke Grenade and Concussion Grenade recipes", True),
    5: ("Vendor station", True),
    6: ("Rigid Synthetics x2; Basic Armor Kit", True),
    7: ("3D Printer Lethals upgrade; Frag Grenade and Throwing Knife recipes", True),
    8: ("Restock Kit", True),
    9: ("Coffey operator skin; Snapshot Grenade recipe", True),
    10: ("Gunsmith station", True),
    11: ("Reactive Metals x2; Basic Triage Kit", True),
    12: ("3D Printer Field Upgrades; Ammo Box and Spotter Scope recipes", True),
    13: ("UAV (fire support)", True),
    14: ("Armor Box recipe", True),
    15: ("Simone operator skin; +1 Operator Slot", True),
    16: ("Explosives Equipment Kit", True),
    17: ("Shock Stick recipe", True),
    18: ("Vendor Upgrade", True),
    19: ("Hector operator skin; Recon Equipment Kit", True),
    20: ("Dog Tag Case station", True),
    21: ("Basic Armor Kit", True),
    22: ("+18 item stash slots", True),
    23: ("Sticky Grenade recipe", True),
    24: ("Restock Kit", True),
    25: ("+5% Gunsmith discount", True),
    26: ("Gas Mask recipe", True),
    27: ("Triage Kit", True),
    28: ("3D Printer Fire Support upgrade; Care Package recipe (Care Package recipe listed by codmunity only)", True),
    29: ("Detonators x2", True),
    30: ("+10% bounty payout", True),
    31: ("UAV recipe", True),
    32: ("Vendor Upgrade", True),
    33: ("Electronics x2", True),
    34: ("Large Backpack", True),
    35: ("+6 weapon stash slots", True),
    36: ("Molotov Cocktail recipe", True),
    37: ("3-Plate Armor Vest", True),
    38: ("Control Unit x2", True),
    39: ("Biomaterials x2", True),
    40: ("+25% bounty payout (Game Rant). Codmunity: unnamed station upgrade.", False),
    41: ("Thermite recipe", True),
    42: ("Trap Equipment Kit", True),
    43: ("Structural Alloy x2", True),
    44: ("CPU x2", True),
    45: ("+18 item stash slots", True),
    46: ("Recon Equipment Kit", True),
    47: ("Nitro Compounds (x2 per codmunity)", True),
    48: ("Self-Revive Kit (recipe per codmunity)", True),
    49: ("Binding Catalyst x2", True),
    50: ("+50% bounty payout", True),
    51: ("Stock Rod x2", True),
    52: ("Inflatable Decoy recipe", True),
    53: ("High-Tenacity Fibers x2", True),
    54: ("Ballistic Gel Armor Kit (Game Rant). Codmunity: unnamed consumable.", False),
    55: ("Disposable Parachute recipe", True),
    56: ("Printed Circuit Board x2", True),
    57: ("Nylon Cloth x2", True),
    58: ("Care Package (fire support)", True),
    59: ("Combat Drone (fire support)", True),
    60: ("+6 weapon stash slots", True),
    61: ("Medium Weapon Backpack", True),
    62: ("Door Breacher Charge", True),
    63: ("2-Plate Helmet Armor Vest", True),
    64: ("Revive Pistol (field upgrade)", True),
    65: ("UAV (fire support)", True),
    66: ("Crossfire (fire support)", True),
    67: ("Defibrillator", True),
    68: ("Durable Gas Mask", True),
    69: ("Parachute", True),
    70: ("+18 item stash slots; +100% bounty payout; Advanced SERE Kit", True),
}
for n in sorted(lv):
    r, c = lv[n]
    item("level-rewards", f"DMZ Level {n}", "Reach DMZ level %d." % n, "Earn DMZ XP (exfils, Story Missions, Dynamic Ops, Side Ops, kills, revives)", r, "", c, [GR_LVL, CM_PROG])

# ---------------------------------------------------------------- Prestige
cat("prestige", "Operator Prestige", None,
    "Prestige an Operator after spending all 18 trait points with the Operator not MIA. Up to 3 permanent Prestige (Pro) Traits, assigned randomly.")
cat("prestige-rewards", "Prestige Rewards", "prestige", "")
cat("prestige-traits", "Prestige (Pro) Traits", "prestige", "12 Pro traits, each upgrading a row 6/9 Major Trait. Assigned randomly; up to 3 permanent.")
item("prestige-rewards", "First Prestige", "Rare tier rewards.", "18 trait points spent, Operator not MIA", "200,000 DMZ Cash; 2 Rare weapons (3 attachment slots); Rare plate carrier and backpack; 4 Rare ingredients", "", True, [CM, CQ])
item("prestige-rewards", "Second Prestige", "Epic tier rewards.", "Prestige again", "300,000 DMZ Cash; 2 weapons with 4 attachment slots; Epic gear and ingredients", "", True, [CM, CQ])
item("prestige-rewards", "Third+ Prestige", "Legendary tier rewards (repeats).", "Prestige again", "500,000 DMZ Cash; Legendary items; 2 weapons with 4 attachment slots", "", True, [CM, CQ])
for t, d in [
    ("Possum Pro", "Self Revive into Last Stand once per match; removes the Tourniquet health penalty."),
    ("Quick Fix Pro", "Health regen starts immediately after killing an enemy Operator or hostile."),
    ("Viper Sense Pro", "Hidden from thermal optics and AI targeting; alerts when an enemy Operator aims at you (alert part reported by some sources only; codmunity calls it 'High Alert')."),
    ("Adaptive Restock Pro", "Hostiles drop rarer additional items."),
    ("Overwatch Pro", "UAV towers never expire and have increased range."),
    ("Field Crafting Pro", "Craft from Common printer resources in-match at 50% lower cost."),
    ("UAV Upgrade Pro", "Increased UAV range/duration, Advanced UAVs, expanded minimap."),
    ("Thermal Padding Pro", "Hides occupied vehicles from UAV detection."),
    ("Free Revive Pro", "Auto-repairs first Wound; can use a Tourniquet while Wounded."),
    ("Numb The Pain Pro", "Longer Painkiller and Smelling Salts effects on revives."),
    ("Die Hard Pro", "Auto-call exfil in Last Stand, infinite bleed-out, faster Last Stand movement. Sources disagree on which effect is the Pro addition."),
    ("Impact Smokes Pro", "Larger, longer-lasting smoke when downed."),
]:
    item("prestige-traits", t, d, "Random on Operator Prestige", "", "", True, [CC_TR, DMZT_PT, CM])

# ---------------------------------------------------------------- Infils
cat("infils", "Infil Methods", None, "Infil choices at deploy and their costs.")
for t, req, r, c in [
    ("Ground (On Foot)", "Available from start", "Free", True),
    ("Polaris Dagor A1", "Reward from Operation Silent Ledger (vehicle); purchasable infil", "5,000 DMZ Cash per infil", True),
    ("LTV", "Complete Operation Iron Citadel", "25,000 DMZ Cash per infil", True),
    ("Helicopter", "Complete Operation Grid Assault", "50,000 DMZ Cash per infil", True),
    ("Cargo Plane", "Reportedly Operation Fallen Ember (metaradar); lets you choose your exact drop point", "100,000 DMZ Cash per infil", True),
]:
    item("infils", t, "", req, r, "", c, [MR, CM, CQ, GF])
cat("exfils", "Exfil Methods", None, "Ways to extract.")
for t in ["Twin Heli Exfil", "Final Exfil (fixed time, carries gas masks)", "Fulton Balloon", "Flare", "Sky Heist Helicopter", "Personal Exfil (buy station)"]:
    item("exfils", t, "", "", "", "", False, [CQ] + ([MW4W] if "Personal" in t else []))

# ---------------------------------------------------------------- FOB
cat("fob", "FOB", None, "Forward Operating Base stations and 3D Printer upgrades.")
cat("fob-stations", "FOB Stations", "fob", "")
cat("fob-upgrades", "FOB / 3D Printer Upgrades", "fob", "Costs vary between guides; check the in-game Upgrades tab.")
for t, req in [
    ("Operators", "Available at start"), ("DMZ Orders", "Available at start"), ("Stash and Loadout", "Available at start"),
    ("Firing Range", "Available at start"), ("Survival Kits", "Available at start"), ("Bounty Leaderboard", "Available at start"),
    ("DMZ Progression", "Available at start"), ("Deploy", "Available at start"), ("Events", "Available at start"),
    ("3D Printer", "DMZ Level 2 (codmunity progression page says Level 1)"), ("Boss Board", "After completing the 2nd DMZ Order"),
    ("Vendor", "DMZ Level 5"), ("Gunsmith", "DMZ Level 10"), ("Dog Tag Case", "DMZ Level 20"),
]:
    item("fob-stations", t, "", req, "", "FOB", True, [CM, CQ])
for t, d, r, c, s in [
    ("Bank Upgrade I", "Bank cap to $250,000 (base $100,000).", "Cost: 20,000 Cash", True, [ATH_STASH, CQ_FOB]),
    ("Bank Upgrade II", "Bank cap to $500,000.", "Cost: 50,000 Cash", False, [ATH_STASH]),
    ("Bank Upgrade III", "Top tier reaches $1,000,000 cap (codmunity mentions a next $2M tier).", "Cost: 100,000 Cash + 5 Infantry Invasion Plans (reported)", False, [ATH_STASH, CM, CQ]),
    ("Stash Item Upgrade I", "+18 item stash slots.", "Cost: $10,000 (one source adds materials)", True, [ATH_STASH, CQ_FOB]),
    ("Weapon Stash Upgrade I", "+6 weapon stash slots; requires Item Stash I.", "", False, [ATH_STASH]),
    ("Dog Tag Case Upgrade I", "+20 Dog Tag Case storage.", "Cost reported as 10,000 Cash + 10 Rigid Synthetics + 10 Biomaterials, or 20,000 Cash + 5 Military Composites", False, [ATH_STASH, CQ_FOB]),
    ("Epic Ingredient Printing", "Print higher-rarity ingredients.", "Cost: 100,000 Cash, 10 Binding Catalyst, 10 Printed Circuit Board, 5 Military Composites", False, [ATH_STASH]),
    ("MIA Recovery Discount", "Discounts on MIA recovery.", "", False, [CM, ATH_STASH]),
    ("Gunsmith Discount", "Gunsmith discounts (Level 25 grants +5%).", "", False, [CM, GR_LVL]),
    ("Gunsmith 5th Attachment Slot", "Fifth attachment slot (Apex slot free at full weapon level per conquestcapped).", "About $50,000", False, [CM, CQ]),
    ("Vendor Upgrades", "More Vendor options; also granted at DMZ Levels 18 and 32.", "", True, [CM, GR_LVL, CM_PROG]),
    ("3D Printer: Tacticals", "Unlocks tactical printing (DMZ Level 4).", "", True, [GR_LVL, CM_PROG]),
    ("3D Printer: Lethals", "Unlocks lethal printing (DMZ Level 7).", "", True, [GR_LVL, CM_PROG]),
    ("3D Printer: Field Upgrades", "Unlocks field upgrade printing (DMZ Level 12).", "", True, [GR_LVL, CM_PROG]),
    ("3D Printer: Fire Support", "Unlocks fire support printing (DMZ Level 28).", "", True, [GR_LVL, CM_PROG]),
]:
    item("fob-upgrades", t, d, r, "", "FOB 3D Printer", c, s)

# ---------------------------------------------------------------- Crafting recipes
cat("crafting", "Crafting Recipes", None,
    "3D Printer recipes (FOB printer unlocks at DMZ Level 2; codmunity progression says Level 1). Printer tabs: Upgrades, Consumables, Plate Carriers, Backpacks, Tacticals, Lethals, Field Upgrades, Fire Support, Gear, Ingredients (gamerfuzion, Game Rant). Upgrades-tab items are tracked under FOB / 3D Printer Upgrades. "
    "Recipes unlock by DMZ Level, DMZ Orders, Story Missions, or by looting a 'Recipe' in Hajin ('Found in Hajin') and extracting it: the recipe is consumed at exfil, added to the printer permanently, and pays 5,000 DMZ Cash, duplicates included (gamerfuzion, metaradar, gamingpromax). Recipes are lost if you die with them. "
    "Costs use four resources (Synthetics, Electronics, Chemicals, Metals; loot breaks down automatically) plus named Ingredients. All FOB printing happens from stash between deployments; the only in-match printer reported is the X01 Production Assembly printer. The Field Crafting trait reportedly allows crafting from Common resources while deployed (no recipe list documented). "
    "Recipe count conflicts: metaradar 94, Game Rant 'over 107'.")
cat("crafting-consumables", "Consumables", "crafting", "")
cat("crafting-plate-carriers", "Plate Carriers", "crafting", "")
cat("crafting-backpacks", "Backpacks", "crafting", "")
cat("crafting-tacticals", "Tacticals", "crafting", "Tab unlocked by the 3D Printer Tacticals upgrade at DMZ Level 4.")
cat("crafting-lethals", "Lethals", "crafting", "Tab unlocked by the 3D Printer Lethals upgrade at DMZ Level 7.")
cat("crafting-field-upgrades", "Field Upgrades", "crafting", "Tab unlocked by the 3D Printer Field Upgrades upgrade at DMZ Level 12. Metaradar counts 15 recipes; Game Rant lists 16.")
cat("crafting-fire-support", "Fire Support", "crafting", "Tab unlocked by the 3D Printer Fire Support upgrade at DMZ Level 28.")
cat("crafting-gear", "Gear", "crafting", "")
cat("crafting-ingredients", "Ingredients", "crafting", "Printable ingredients. Uncommon tier needs the Uncommon Ingredient Printing upgrade; Epic tier needs Epic Ingredient Printing. Metaradar counts 6 Uncommon + 9 Epic; Game Rant and gamingpromax list 6 + 8.")
cat("crafting-x01-printer", "X01 Printer (In-Match)", "crafting", "Printer in Production Assembly, western mezzanine office on the Data Center floor (E5), X01 Black Site. Bring inputs in your backpack, print in-match, extract with the output (games.gg). Opening it completes the X01 Orders 'Crafting Material' task.")
cat("crafting-other", "Other Reported Recipes", "crafting", "Recipes named as rewards but missing from the recipe lists checked; costs unknown.")

FOUND = "Found in Hajin: loot the Recipe and extract with it"
STARTER = "Starter recipe: Game Rant lists it as default; gamerfuzion says DMZ Level 2 (when the printer unlocks); codmunity progression says Level 1"
STARTER2 = "Starter recipe: Game Rant lists it as default; gamerfuzion and codmunity progression say DMZ Level 2"
ORD = "DMZ Orders (Game Rant)"
BOTH = [GR_3DP, GPM_3DP]
recipes = [
    # tab, name, cost, unlock, note, sources, confirmed
    ("consumables", "Bandage", "15 Synthetics, 15 Chemicals", STARTER, "", BOTH + [CM_CRAFT, GF_3DP], True),
    ("consumables", "Medkit", "30 Chemicals, 1 Binding Catalyst, 5 Biomaterials", STARTER, "", BOTH + [CM_CRAFT, GF_3DP], True),
    ("consumables", "Pain Killers", "15 Electronics, 15 Chemicals", FOUND, "", BOTH + [CM_CRAFT], True),
    ("consumables", "Sedative Inhaler", "15 Synthetics, 15 Chemicals", "DMZ Level 3", "", BOTH + [CM_CRAFT, GR_LVL], True),
    ("consumables", "Energy Drink", "10 Chemicals, 10 Metals", FOUND, "", BOTH + [CM_CRAFT], True),
    ("consumables", "Radiation Blockers", "30 Chemicals, 3 Biomaterials", FOUND, "Codmunity lists 15 Electronics, 15 Chemicals.", BOTH + [CM_CRAFT], True),
    ("consumables", "Smelling Salts", "30 Chemicals, 3 Detonators", FOUND, "", BOTH, True),
    ("consumables", "Self-Revive Kit", "1 Stabilized Reagents, 5 Biomaterials, 3 Binding Catalyst", "DMZ Level 48 (Game Rant; codmunity progression lists a Self-Revive Kit recipe at 48)", "Binding Catalyst count conflicts: gamingpromax/codmunity 3, Game Rant 5. Codmunity omits the Stabilized Reagents.", BOTH + [CM_CRAFT, CM_PROG], True),
    ("consumables", "Door Breacher Charge", "1 Experimental Compounds, 5 Stock Rod, 3 Volatile Explosives", FOUND, "Codmunity lists only 1 Stock Rod. Level 62 also grants a Door Breacher Charge item (level rewards).", BOTH + [CM_CRAFT], True),
    ("plate-carriers", "1-Plate Armor Vest", "25 Synthetics, 25 Metals", STARTER, "", BOTH + [CM_CRAFT, GF_3DP], True),
    ("plate-carriers", "2-Plate Armor Vest", "50 Synthetics, 5 Reactive Metals", STARTER2, "Game Rant lists 25 Synthetics; gamingpromax, codmunity and gamerfuzion say 50.", BOTH + [CM_CRAFT, GF_3DP], True),
    ("plate-carriers", "2-Plate Ballistic Gel Vest", "50 Synthetics, 3 Binding Catalyst, 10 Reactive Metals", FOUND, "", BOTH, True),
    ("plate-carriers", "2-Plate Helmet Armor Vest", "50 Synthetics, 3 Structural Alloy, 10 Reactive Metals", FOUND, "", BOTH, True),
    ("plate-carriers", "3-Plate Armor Vest", "2 Ballistic Fabric, 5 Nylon Cloth, 10 Reactive Metals", ORD + "; reported as the Page 12 (The Grid 1/2) reward, sources disagree", "", BOTH, True),
    ("plate-carriers", "3-Plate Ballistic Gel Vest", "2 Experimental Compounds, 4 Stabilized Reagents, 10 Biomaterials", FOUND, "", BOTH, True),
    ("plate-carriers", "3-Plate Helmet Armor Vest", "2 Nano-Structured Alloy, 4 Alloyed Plating, 10 Reactive Metals", FOUND, "", BOTH, True),
    ("plate-carriers", "Tempered Armor Vest", "2 Military Composites, 4 Ballistic Fabric, 10 Rigid Synthetics", FOUND, "", BOTH + [CM_CRAFT], True),
    ("backpacks", "Small Backpack", "25 Synthetics, 25 Metals", STARTER, "", BOTH + [CM_CRAFT, GF_3DP], True),
    ("backpacks", "Medium Backpack", "50 Synthetics, 5 Rigid Synthetics", STARTER2, "", BOTH + [CM_CRAFT, GF_3DP], True),
    ("backpacks", "Large Backpack", "2 Nylon Laminate, 5 Structural Alloy, 10 Rigid Synthetics", ORD + "; Page 16 (Hornet's Nest 1/2) rewards the recipe", "", BOTH, True),
    ("backpacks", "Medium Scavenger Backpack", "50 Metals, 3 Nylon Cloth, 10 Rigid Synthetics", FOUND, "", BOTH, True),
    ("backpacks", "Medium Weapon Backpack", "50 Synthetics, 3 High-Tenacity Fibers, 10 Rigid Synthetics", FOUND, "", BOTH, True),
    ("backpacks", "Small Secure Backpack", "50 Metals, 3 Structural Alloy, 10 Rigid Synthetics", FOUND, "", BOTH + [CM_CRAFT], True),
    ("backpacks", "Large Scavenger Backpack", "2 Nylon Laminate, 5 High-Tenacity Fibers, 10 Rigid Synthetics", FOUND, "Game Rant lists 3 Nylon Laminate; gamingpromax 2.", BOTH, False),
    ("backpacks", "Medium Secure Backpack", "2 Alloyed Plating, 5 Nylon Cloth, 10 Reactive Metals", FOUND, "", BOTH, True),
    ("backpacks", "Large Secure Backpack", "2 Prototype RF Module, 4 Alloyed Plating, 10 Rigid Synthetics", FOUND, "", BOTH, True),
    ("backpacks", "Secure Scavenger Backpack", "2 Military Composites, 4 Nylon Laminate, 10 Reactive Metals", FOUND, "", BOTH + [CM_CRAFT], True),
    ("tacticals", "Concussion Grenade", "10 Synthetics, 10 Chemicals", "DMZ Level 4", "", BOTH + [GR_LVL], True),
    ("tacticals", "Smoke Grenade", "10 Synthetics, 10 Chemicals", "DMZ Level 4", "", BOTH + [GR_LVL], True),
    ("tacticals", "Snapshot Grenade", "10 Synthetics, 10 Chemicals", "DMZ Level 9", "", BOTH + [GR_LVL], True),
    ("tacticals", "Shock Stick", "10 Synthetics, 10 Chemicals", "DMZ Level 17", "", BOTH + [GR_LVL], True),
    ("tacticals", "Screamer Mine", "10 Synthetics, 10 Chemicals", FOUND, "", BOTH, True),
    ("tacticals", "Flash Grenade", "10 Synthetics, 10 Chemicals", ORD + "; Page 2 (Human Intel 1/2) rewards the recipe", "", BOTH, True),
    ("tacticals", "Decoy Grenade", "10 Synthetics, 10 Chemicals", ORD + "; Page 8 (Underground 1/2) rewards the recipe", "", BOTH, True),
    ("tacticals", "Stim", "15 Synthetics, 15 Chemicals", FOUND, "", BOTH, True),
    ("tacticals", "Heartbeat Sensor", "25 Synthetics, 25 Chemicals", FOUND, "", BOTH, True),
    ("tacticals", "Spotter Scope", "50 Synthetics, 5 Electronic Sensors", "DMZ Level 12", "", BOTH + [GR_LVL], True),
    ("lethals", "Frag Grenade", "10 Chemicals, 10 Metals", "DMZ Level 7", "", BOTH + [GR_LVL], True),
    ("lethals", "Throwing Knife", "25 Chemicals, 25 Metals", "DMZ Level 7", "", BOTH + [GR_LVL], True),
    ("lethals", "Semtex", "10 Chemicals, 10 Metals", "DMZ Level 23 (Game Rant recipe list; level-reward lists call it 'Sticky Grenade')", "", BOTH + [GR_LVL], True),
    ("lethals", "Molotov Cocktail", "10 Chemicals, 10 Metals", "DMZ Level 36", "", BOTH + [GR_LVL], True),
    ("lethals", "Thermite", "10 Chemicals, 10 Metals", "DMZ Level 41", "", BOTH + [GR_LVL], True),
    ("lethals", "C4", "10 Chemicals, 10 Metals", ORD + "; Page 11 (Boss Board & Gunsmith) rewards the recipe", "", BOTH, True),
    ("lethals", "Zip Gun", "10 Chemicals, 10 Metals", FOUND, "", BOTH, True),
    ("lethals", "Claymore", "10 Chemicals, 10 Metals", FOUND, "", BOTH, True),
    ("lethals", "Proximity Mine", "10 Chemicals, 10 Metals", FOUND, "", BOTH, True),
    ("lethals", "Drill Charge", "15 Chemicals, 15 Metals", FOUND, "", BOTH, True),
    ("lethals", "Trip Wire", "15 Chemicals, 15 Metals", FOUND, "", BOTH, True),
    ("field-upgrades", "Ammo Box", "15 Synthetics, 15 Metals", "DMZ Level 12", "", BOTH + [GR_LVL], True),
    ("field-upgrades", "Armor Box", "30 Metals, 3 Reactive Metals", "DMZ Level 14", "Codmunity lists only 1 Reactive Metals.", BOTH + [CM_CRAFT, GR_LVL], True),
    ("field-upgrades", "Revive Pistol", "2 Power Regulators, 3 Binding Catalyst, 5 Detonators", "DMZ Level 25 (Game Rant recipe list)", "Game Rant lists 2 Binding Catalyst; gamingpromax and codmunity 3. Level-reward lists put a Revive Pistol at Level 64 and give Level 25 as a Gunsmith discount, so the Level 25 unlock is unverified.", BOTH + [CM_CRAFT], True),
    ("field-upgrades", "Inflatable Decoy", "15 Synthetics, 15 Electronics", "DMZ Level 52", "", BOTH + [GR_LVL], True),
    ("field-upgrades", "Defibrillator", "30 Electronics, 3 Control Units", "Complete Operation Critical Extraction (Game Rant, metaradar)", "", BOTH + [MR], True),
    ("field-upgrades", "DDOS", "30 Electronics, 3 Detonators", ORD + "; Page 8 (Underground 1/2) rewards the recipe", "Gamingpromax lists 30 Detonators (likely typo); Game Rant 3.", BOTH, False),
    ("field-upgrades", "Recon Drone", "30 Metals, 3 Electronic Sensors", ORD + "; Page 5 (Counterfeit 1/2) rewards the recipe", "", BOTH, True),
    ("field-upgrades", "Trophy System", "15 Electronics, 3 Control Units", FOUND, "", BOTH, True),
    ("field-upgrades", "Portable Radar", "15 Synthetics, 15 Electronics", FOUND, "", BOTH, True),
    ("field-upgrades", "Razor Wire Trap", "15 Electronics, 15 Metals", FOUND, "", BOTH, True),
    ("field-upgrades", "Rebreather", "15 Synthetics, 15 Chemicals", FOUND, "", BOTH, True),
    ("field-upgrades", "Riot Shield", "15 Synthetics, 15 Metals", FOUND, "", BOTH, True),
    ("field-upgrades", "Seeker Drone", "15 Synthetics, 15 Electronics", FOUND, "", BOTH, True),
    ("field-upgrades", "Smoke Wall", "15 Electronics, 15 Chemicals", FOUND, "", BOTH, True),
    ("field-upgrades", "SAM Airburst Turret", "30 Metals, 3 Detonators", FOUND, "", BOTH, True),
    ("field-upgrades", "Fulton Drop Marker", "1 Prototype RF Module, 3 Comms Modules, 5 Control Units", FOUND, "", BOTH, True),
    ("fire-support", "Care Package", "20 Electronics, 2 Control Units, 2 Rigid Synthetics", "DMZ Level 28 (Game Rant recipe list, codmunity progression)", "", BOTH + [CM_PROG], True),
    ("fire-support", "UAV", "30 Electronics, 2 Structural Alloy, 5 Electronic Sensors", "DMZ Level 31", "", BOTH + [GR_LVL], True),
    ("fire-support", "Bombing Run", "30 Chemicals, 2 Nitro Compounds, 5 Control Units", FOUND, "", BOTH, True),
    ("fire-support", "Combat Drone", "30 Electronics, 2 CPU, 5 Control Units", FOUND, "", BOTH, True),
    ("fire-support", "Bomb Glider", "30 Chemicals, 2 Stock Rod, 5 Control Units", FOUND, "Codmunity lists only 1 Stock Rod.", BOTH + [CM_CRAFT], True),
    ("fire-support", "Artillery Beacon", "2 Volatile Explosives, 3 Nitro Compounds, 5 Detonators", FOUND, "", BOTH, True),
    ("fire-support", "Advanced UAV", "2 Comms Modules, 3 Nitro Compounds, 5 Electronic Sensors", FOUND, "", BOTH, True),
    ("fire-support", "Impact Warhead", "2 Turned Components, 3 Nitro Compounds, 5 Detonators", FOUND, "", BOTH, True),
    ("fire-support", "Railgun Sentry", "2 Power Regulators, 3 Nitro Compounds, 5 Control Units", FOUND, "", BOTH, True),
    ("fire-support", "Crossfire", "2 Prototype RF Modules, 3 Volatile Explosives, 5 Electronic Sensors", FOUND, "", BOTH, True),
    ("gear", "Gas Mask", "30 Chemicals, 3 Rigid Synthetics", "DMZ Level 26", "", BOTH + [GR_LVL], True),
    ("gear", "Disposable Parachute", "30 Chemicals, 3 Rigid Synthetics", "DMZ Level 55", "Codmunity lists only 1 Rigid Synthetics.", BOTH + [CM_CRAFT, GR_LVL], True),
    ("gear", "Weak Night Vision Goggles", "25 Metals, 5 Control Units", ORD + "; Page 8 (Underground 1/2) rewards a 'Night Vision Goggles recipe', tier not specified", "", BOTH, True),
    ("gear", "Night Vision Goggles", "50 Metals, 3 Printed Circuit Boards, 10 Control Units", ORD + "; Page 8 (Underground 1/2) rewards a 'Night Vision Goggles recipe', tier not specified", "", BOTH, True),
    ("gear", "Durable Gas Mask", "30 Chemicals, 1 High-Tenacity Fibers, 5 Biomaterials", FOUND, "", BOTH, True),
    ("gear", "Elite Night Vision Goggles", "2 Power Regulators, 3 CPU, 5 Electronic Sensors", FOUND, "", BOTH, True),
    ("gear", "Parachute", "2 Turned Components, 5 Nylon Cloth, 10 Rigid Synthetics", FOUND, "", BOTH, True),
]
UNC = "Uncommon Ingredient Printing upgrade (FOB; reported cost 50,000 DMZ Cash, 20 Biomaterials, 10 High-Tenacity Fibers, 5 Comms Modules)"
EPI = "Epic Ingredient Printing upgrade (FOB; 100,000 DMZ Cash, 10 Binding Catalyst, 10 Printed Circuit Boards, 5 Military Composites)"
for n, c in [("Biomaterials", "20 Synthetics, 20 Chemicals"), ("Control Unit", "20 Electronics, 20 Metals"),
             ("Detonators", "20 Electronics, 20 Chemicals"), ("Electronic Sensors", "20 Synthetics, 20 Electronics"),
             ("Reactive Metals", "20 Chemicals, 20 Metals"), ("Rigid Synthetics", "20 Synthetics, 20 Metals")]:
    recipes.append(("ingredients", n, c, UNC, "", BOTH, True))
for n, c in [("Alloyed Plating", "100 Metals, 3 Structural Alloy"), ("Ballistic Fabric", "100 Synthetics, 3 High-Tenacity Fibers"),
             ("Comms Module", "100 Electronics, 3 CPU"), ("Nylon Laminate", "100 Synthetics, 3 Nylon Cloth"),
             ("Power Regulator", "100 Electronics, 3 Printed Circuit Boards"), ("Stabilized Reagents", "100 Chemicals, 3 Binding Catalyst"),
             ("Turned Components", "100 Metals, 3 Stock Rod"), ("Volatile Explosives", "100 Chemicals, 3 Nitro Compounds")]:
    recipes.append(("ingredients", n, c, EPI, "", BOTH, True))
for tab, n, cost, unlock, note, src, conf in recipes:
    item("crafting-" + tab, n, ("Cost: " + cost + "." + (" " + note if note else "")), unlock, "", "FOB 3D Printer", conf, src)
X01P = "X01 Production Assembly printer (Data Center, E5)"
for n, cost, req in [
    ("Experimental Compounds", "2 Volatile Explosives, 5 Binding Catalyst", "Available at the X01 printer"),
    ("Military Composites", "2 Nylon Laminate, 5 Nylon Cloth", "Available at the X01 printer"),
    ("Nano-Structured Alloy", "2 Turned Components, 5 Structural Alloy", "Available at the X01 printer"),
    ("Prototype RF Module", "2 Power Regulator, 5 CPU", "Available at the X01 printer"),
    ("Staff Emergency Exfil Keycard", "2 CPU, 4 Printed Circuit Board, 8 Control Unit", "Available at the X01 printer; a recipe for it is also reported as an X01 Orders Page 4 reward"),
    ("Encodable Blank Keycard", "6 Printed Circuit Board, 8 Control Unit", "Available at the X01 printer"),
]:
    item("crafting-x01-printer", n, "Cost: " + cost + ". Printed in-match; output quantity not stated. Legendary materials are not printable at the FOB printer.", req, "", X01P, False, [GG_X01P])
for n, req in [("Consumable Box", "Reported X01 Orders Page 2 reward"), ("Medical Box", "Reported X01 Orders Page 2 reward"),
               ("Hazmat Box", "Reported X01 Orders Page 3 reward")]:
    item("crafting-other", n, "Cost not documented; not in the Game Rant or gamingpromax recipe lists.", req, "", "", False, [DG])

# ---------------------------------------------------------------- Keys
cat("keys", "Keys & Locked Rooms", None, "Keys show a grid hint on their item card. Key door count reported as 19 by one guide, 14 by another.")
cat("keys-lieutenant", "Lieutenant Key Rooms", "keys", "Keys dropped by Lieutenants.")
cat("keys-general", "Other Keys", "keys", "")
for t, loc, loot, src in [
    ("Gorani's Scout Overlook", "Top of the Rice Mill, Imjin Farmland (D8)", "Incisor (MAR-9)", [SG, GF, CQB]),
    ("The Chemist's Secure Armory", "Bunker opposite the boathouse, Haneul Nuclear Reactor (I4)", "Chemical Reaction (Kastov 762)", [SG, MW4W, CQB]),
    ("Jin-Tae's Private Lounge", "Heavenly Luck Casino penthouse/roof (F4); power the parking-garage generator then take the elevator", "Highroller's Fortune (ISO Nightshade)", [SG, GF, CQB]),
    ("The Doctor's Command Office", "Mirae General Hospital floor 7, near offices 701-712 (F5)", "Doctor's Salvo (Patriot XMR)", [SG, GF, CQB, ATH]),
    ("Iskra's Control Room", "Cheonwang Peak Array transmitter/broadcast building top floor (grid F6 or F7 reported)", "Widow Maker (Warlord)", [SG, GF, CQB, MW4W]),
    ("Roze's Highrise Armory", "Netshin Tech Complex floor 14 east side, The Grid (G6)", "The Kraken (Astaroth .57)", [SG, GF, CQB, MW4W]),
    ("Jang-ui's Converted Power Room", "NuriGO Mall lowest floor near K9 course (H6)", "Paektu (Hyeon Burst)", [SG, GF, CQB]),
    ("Supreme Leader's Bunker (Bale)", "Beneath Admin Complex No. 2, Chang-san Air Base; access card not a key", "Dreadnought (Type 73)", [SG, ATH]),
    ("Kang's Arms Incinerator (Warden)", "Central 14th Political Prison; access method not reported", "Incarcerator (X-58 NYX)", [SG]),
]:
    item("keys-lieutenant", t, "Unique weapon not guaranteed; loot randomized.", "Kill the Lieutenant and take the key/card", loot, loc, len(src) >= 2, src)
for t, loc, how, d, src in [
    ("Counting Room Vault", "Heavenly Luck Casino main floor, Cheongun Village", "Operation Silent Ledger reward; Industrial Locker at Rice Mill; Military Locker in Haksan School Armory", "Epic rarity (allthings).", [MW4W, ATH, MR]),
    ("Vault Armory", "Heavenly Luck Casino underground parking, Cheongun Village", "", "", [MW4W, ATH]),
    ("Mirae Electrical Room", "Mirae General Hospital B2 parking (F5)", "Operation Critical Extraction reward", "Rare rarity.", [ATH, MR]),
    ("Coin Mining Den", "NuriGO West (G6), '3' stairwell landing", "Operation Shopping Hacks reward", "", [ATH, MR]),
    ("Haksan School Armory", "School NE of the Re-Education Center, Deadtown", "", "", [MW4W, ATH]),
    ("Re-Education Center Annex", "Re-Education Center ground floor, Deadtown", "", "", [MW4W, ATH]),
    ("Underground Propaganda Store Room", "Re-Education Center underground", "", "", [ATH]),
    ("Air Base DRC Weapons Locker", "Secure armory, Chang-san Air Base bunker", "", "Ultra rarity reported.", [MW4W]),
    ("Reactor DRC Locker", "Reactor 02 irradiated pool, Haneul Nuclear Reactor", "", "Rarity reported as Ultra or Legendary.", [MW4W]),
    ("Bank Branch Vault Access", "South Korean bank branches (currency storage)", "", "", [MW4W]),
    ("Imjin Mill Foreman's Office", "Rice mill first floor, Imjin Farmland", "", "", [MW4W]),
    ("The Citadel South Wing", "14th Political Prison", "", "", [MW4W]),
    ("Train Depot Storageroom", "Basement storeroom near the fire department, Cheongun Village", "", "", [MW4W]),
    ("Mechanic's Shack", "South of the clinic, Cheongun Village", "", "Rare rarity.", [ATH]),
    ("Police Station Armory", "Pyeonghwa Village police station basement", "", "", [ATH, CQ]),
    ("Militia Arms Depot", "Gangbyeon Apartment B lower floor, Hajin River Heights", "Duffel bag in The Citadel East Wing", "Rare. Gamerfuzion mentions a 'Gangbyeon Apartment B Key'.", [ATH, GF]),
    ("Field Depot", "Hangar, Chang-san Air Base", "Reported as Operation Shopping Hacks reward (one source)", "", [ATH]),
    ("Executive Arms Auction", "DBN Headquarters office floor", "", "", [ATH]),
    ("Rice Mill Bunker", "Rice Mill, Imjin Farmland", "", "", [ATH]),
    ("Commandant Office", "Admin Complex No. 2", "", "", [ATH]),
    ("Shop Records Room", "Wolves Stadium (F7)", "", "", [ATH]),
    ("Gun Store Weapons Locker", "Gun stores in western Cheongun Village and northern Songdo Wharf", "", "Rare; one key opens one locker.", [ATH]),
    ("Hazard Storehouse", "Haneul Nuclear Reactor storage shed", "", "", [ATH]),
    ("Mirae Chemical Lab", "Mirae General Hospital", "Key spawns in 7th floor offices", "", [CM]),
    ("Fire Station Key", "Fire stations", "Usually on a lower floor; single-use", "", [CM]),
    ("Deep Vault Access Key", "X01 Deep Vault", "Dropped by The Captain; X01 Lieutenants drop random Deep Vault keys", "", [GR_BOSS, DG]),
]:
    item("keys-general", t, d, how, "", loc, len(src) >= 2, src)

# ---------------------------------------------------------------- Weapons & camos
cat("weapons", "Weapons & Weapon Manuals", None,
    "Gunsmith sells launch weapons (count reported as 32, 33, or 35 incl. later additions). Weapon Manuals are loot items: extracting a weapon's manual consumes it at exfil and permanently unlocks that weapon for purchase at the Gunsmith (games.gg, conquestcapped, gfinity); each extracted manual pays 5,000 DMZ Cash, duplicates included (conquestcapped). Extracting 3 manuals for the same weapon unlocks its War Spoils camo (games.gg, conquestcapped, codmunity). Conquestcapped words it as 'three manuals for the equipped weapon' and notes player reports of some manuals not counting, so check challenge progress after each run. Manuals are lost if you die with them. Per-weapon ladder: Military 1-8, 3 Special, Gold, Platinum, Harmonic Break, Divergence.")
weapons = {
    "Assault Rifle": [("HAN 86", "Smoke, Stormwave, Red"), ("M4", "Myriad, Night Ops, Green"), ("Hyeon Burst", "Ponderosa, Red Rain, Kitty Kaos"),
                      ("Kastov 762", "Samnim, Raster Aux, Yellow"), ("Patriot XMR", "Dune Sea, Scorch, Disperse"), ("Oden", "Dark Moss, Shale, Hot Rod"),
                      ("Axion", "Splinter Rock, Sunset Tropic, Cyan"), ("Cronen Squall", "Oni, Urban Smoke, Optical Reverb"), ("Cronen Osprey", "In the Weeds, Dark Ichor, Chained")],
    "SMG": [("ISO Nightshade", "Asphalt, Black Topo, Brown"), ("VEL 46", "Jungle Shadow, Ghast, Gunmetal"), ("WZ.55 Striga", "Stellation, Rattlesnake, Dark Tan"),
            ("PPSH-41", "Blackwell, Iron, Currents"), ("X-58 NYX", "Sniper Veil, Carbonated, Lime"), ("CSG-35", "Polyhedron, Rind, Black Grip")],
    "Shotgun": [("REZI 12", "Struck Oil, Brushstroke, White Pine (list truncated)"), ("Warlord", "")],
    "LMG": [("FINN LMG", ""), ("Type 73", ""), ("APOC-338", "")],
    "Marksman Rifle": [("MAR-9", ""), ("ORIS 8.6", ""), ("Mosin-Nagant", "")],
    "Sniper Rifle": [("Astaroth .57", ""), ("KG-7 Vulcan", ""), ("Signal 50", "")],
    "Pistol": [("Sang 9mm", ""), ("Krait P68", ""), (".50 GS", ""), ("Mojave .357", "")],
    "Launcher": [("PILA", ""), ("RPG-8", ""), ("JOKR", ""), ("PM-40 Anvil", "")],
    "Melee": [("FSS Carbon Edge 1095", "")],
}
corroborated = {"M4", "Patriot XMR", "Hyeon Burst", "Kastov 762", "ISO Nightshade", "X-58 NYX", "REZI 12", "Warlord", "Type 73", "MAR-9", "ORIS 8.6", "Astaroth .57", "Mojave .357", "Signal 50"}
for cls, ws in weapons.items():
    for w, sp in ws:
        notes = {"Mojave .357": " Unlocked via Special Delivery Dynamic Op (metaradar).",
                 "ISO Nightshade": " Unlocked via Broken Resupply Dynamic Op (metaradar).",
                 "Cronen Squall": " Vendor weapon, unlocks at level 55 (codmunity spells 'Cronin Squall').",
                 "Signal 50": " Free via a Code Blurple blueprint (gamerfuzion)."}.get(w, "")
        item("weapons", w, cls + "." + notes + ((" Special camos: " + sp + ".") if sp else ""),
             "Extract 3 of this weapon's Weapon Manuals. The first extraction unlocks it for purchase at the Gunsmith.",
             "Gunsmith unlock (1st manual); War Spoils camo (3rd manual); 5,000 DMZ Cash per manual", "", w in corroborated,
             [CC_CAMO] + ([GR_BOSS, CQB] if w in corroborated else []) + [GG_WM, CQ_WM, CM], goal=3)

cat("camos", "DMZ Camos", None, "DMZ camo ladder and mode mastery camos. Harmonic Break requires 33 Platinum camos.")
for t, d, c in [
    ("Military Camos 1-8", "Per weapon; weapon level or unlock count requirements vary by weapon.", False),
    ("Special Camos (3 per weapon)", "Weapon-specific challenges.", False),
    ("Gold", "Complete the 3 weapon-specific camos, then 100 enemy kills in one DMZ match.", False),
    ("Platinum", "Complete 8 Gold camos on ARs (5 on SMGs) then 100 headshots (75 kills from behind on SMGs).", False),
    ("Harmonic Break", "Complete 33 Platinum camos, then 50 double kills (ARs; varies by class).", True),
    ("Divergence", "Awarded for completing 33 Harmonic Break camos; grants access to DMZ Mastery.", True),
    ("Chiral", "DMZ Mastery 1: 2,500 kills on Tier 3+ enemies. One source (gamingpromax) swaps Chiral/Helio numbers (25,000).", True),
    ("Ripple Tide", "After Chiral: extract two Lieutenant dog tags in one deployment, 50 times.", True),
    ("Helio", "After Ripple Tide: 25,000 kills with Legendary weapons on a max-level Operator (one source says 2,500).", True),
    ("Pyroclast / Terminus / Scatter / Cascade (Prestige camos)", "Prestige camos; Terminus at weapon-specific Prestige Master levels (44-73 seen), Scatter 150, Cascade 250. Not confirmed DMZ-specific.", False),
]:
    item("camos", t, d, "", "", "", c, [CC_CAMO] + ([CQ] if c else []))

# ---------------------------------------------------------------- Traits
cat("traits", "Operator Traits", None, "Three trees (Warfighter, Scout, Survivalist); each has 6 Major (rows 3/6/9, pick one of each pair) and 16 random Minor traits; 9 points per tree, 18 total.")
cat("traits-warfighter", "Warfighter (Major)", "traits", "")
cat("traits-scout", "Scout (Major)", "traits", "")
cat("traits-survivalist", "Survivalist (Major)", "traits", "")
cat("traits-minor", "Minor Traits", "traits", "Random minor traits; tree assignment not documented.")
for slug, lst in [
    ("traits-warfighter", [("Equipment Professional", "Row 3: slowly refills Lethals/Tacticals."), ("Combat Resistance", "Row 3: reduced explosive/tactical damage."),
                           ("Viper Sense", "Row 6: hidden from thermal optics and AI targeting."), ("Quick Fix", "Row 6: faster health regen after kills."),
                           ("Possum", "Row 9: one Self Revive into Last Stand per match; nerfed Oct 28/Season 1 (not usable with killers nearby or within 4 min)."),
                           ("Adaptive Restock", "Row 9: hostiles drop an additional item.")]),
    ("traits-scout", [("Hostile Looter", "Row 3: hostiles sometimes drop Uncommon (rarely Rare) printer ingredients."), ("Container Looter", "Row 3: chance of extra container loot."),
                      ("Field Crafting", "Row 6: craft from Common printer resources while deployed."), ("UAV Upgrade", "Row 6: better UAVs, Advanced UAVs."),
                      ("Overwatch", "Row 9: UAV towers you activate never expire."), ("Thermal Padding", "Row 9: hidden from UAVs; downgrades Advanced UAVs.")]),
    ("traits-survivalist", [("Faster Revive", "Row 3."), ("Consumable Duration", "Row 3."), ("Impact Smokes", "Row 6: smoke when downed."),
                            ("Free Revive", "Row 6: auto-repair first Wound."), ("Numb The Pain", "Row 9: Painkiller/Smelling Salts on revive."),
                            ("Die Hard", "Row 9: auto-call exfil in Last Stand; infinite bleed-out.")]),
]:
    for t, d in lst:
        item(slug, t, d, "Spend trait points", "", "", True, [CC_TR, CM])
minor = ["Plate Speed", "Plate Pouch", "Plate Organization", "Cash Ops", "Objective Oriented", "Expedited Extraction", "Resupply", "Quick Regen",
         "Auto Fill", "Combat Scanner", "Operator Tracker", "Mini Tracker", "Investor", "Combat Scavenger", "Resource Pockets", "Resource Management",
         "Stealthy", "Lucky", "Metabolism", "Consumable Stacker", "Killing Spree", "Final Intel", "Fast Learner", "Faster Learner", "Pack Rat",
         "Resource Hoarder", "Key Cash", "LT Hunter", "Bounty Hunter", "Air Superiority", "Rampage", "Adrenaline Burst", "Rescuer", "Strong Arm",
         "Free Prep", "Ammo Scavenger", "Ammo Reserves", "Hostile Ammo", "Popcorn Lethals", "Popcorn Tacticals", "Bounty Intel", "Quick Knife",
         "Rad Blocker", "Fuel Economy", "Mechanic", "Deep Breath"]
in_cm = {"Adrenaline Burst", "Investor", "Killing Spree", "LT Hunter", "Air Superiority", "Metabolism", "Stealthy", "Resource Pockets", "Final Intel"}
for t in minor:
    item("traits-minor", t, "", "Random minor trait slot", "", "", t in in_cm, [CC_TR] + ([CM] if t in in_cm else []))

# ---------------------------------------------------------------- Collectibles
cat("collectibles", "Collectibles & Intel Items", None, "Notable lootable/extractable items tied to objectives and progression.")
for t, d, loc, src in [
    ("Gold Bar", "Ultra valuable; reported in 5 bank vaults; Silent Ledger reward.", "Bank vaults, Heavenly Luck Casino", [CM, GF, MR]),
    ("Counterfeit Cash", "Dropped by NK soldiers pinged via Deadtown UAV tower (Execute Intel).", "Deadtown", [CM, GR_ORD, DG]),
    ("Printing Plates", "Secured in Operation Silent Ledger.", "Heavenly Luck Casino", [MR, GF]),
    ("Medical Extraction Intel", "Looted after clearing a Compound (No One Left).", "Compounds", [GR_ORD, DG]),
    ("Drone Motherboard", "Loot from destroyed drones (Death From Above).", "", [GR_ORD, DG]),
    ("Financial Ledger Fragments", "City Hall 2nd floor (Civil Service).", "NuriGO Mall City Hall", [GR_ORD, DG, GF]),
    ("Chemical Components (Convoy)", "From a cleared NK convoy (Navigate With Care).", "", [GR_ORD, DG, MR]),
    ("Pristine K9 Battery Cores", "From K9s in NuriGO Mall Underground (Abandoned).", "NuriGO Mall Underground", [GR_ORD, DG, GF]),
    ("Encrypted Voice Logs", "DBN TV Building broadcast hack (Ears Everywhere).", "Cheonwang Peak Array", [GR_ORD, DG, GF]),
    ("Lieutenant Dog Tags", "Dropped by Lieutenants; redeem for cash or store in Dog Tag Case; used for Ripple Tide camo and Boss Board challenges.", "", [CQ, CQB, CM]),
    ("Irradiated Containers", "Rarest loot from chemical lockers; opened at decontamination points (Reactor 02 decontamination).", "Haneul Nuclear Reactor", [CM, GF]),
    ("Encrypted Drive", "Valuable/intel item.", "", [CM]),
    ("Regional Combat Notes", "Intel document.", "", [CM]),
    ("Infantry Invasion Plans", "Reportedly needed for Bank Upgrade III.", "", [ATH_STASH]),
    ("The Captain's Helmet Sections", "Collect and extract during The Captain Threat Briefing (X01).", "X01", [DMZHUB_X01]),
    ("Ri's Video Footage / Logs", "X01 Orders storyline items.", "X01", [DG]),
    ("Super User Data Access Keycard", "Flooded barracks under X01 Supply Depot.", "X01", [DG]),
    ("Military Composites", "Legendary ingredient from Colossus.", "", [CQB, GR_BOSS]),
    ("Prototype RF Module", "Legendary ingredient from Deathstalker.", "", [CQB, GR_BOSS]),
    ("Nano-Structured Alloy", "Ingredient from the Tank.", "", [CQB, GR_BOSS]),
]:
    item("collectibles", t, d, "", "", loc, len(src) >= 2, src)

# ---------------------------------------------------------------- Cosmetics
cat("cosmetics", "Blueprints & Cosmetics", None, "DMZ-earned cosmetics. No MW4 DMZ calling card/emblem list was found in any source.")
for t, req, src, c in [
    ("Reece (Operator Skin)", "DMZ Level 4", [GR_LVL, CM_PROG], True),
    ("Coffey (Operator Skin)", "DMZ Level 9", [GR_LVL, CM_PROG], True),
    ("Simone (Operator Skin)", "DMZ Level 15", [GR_LVL, CM_PROG], True),
    ("Hector (Operator Skin)", "DMZ Level 19", [GR_LVL, CM_PROG], True),
    ("Vitriol (Legendary Operator Skin)", "Wager Match event (free)", [GF], False),
    ("High Roller's Fortune (ISO Nightshade Legendary Blueprint)", "Jin-Tae drop", [CQB, GR_BOSS, SG], True),
    ("Doctor's Salvo (Patriot XMR Legendary Blueprint)", "The Doctor drop / Command Office", [GR_BOSS, SG, GF], True),
    ("The Kraken (Astaroth .57 Legendary Blueprint)", "Roze drop / Highrise Armory", [GR_BOSS, SG], True),
    ("Incarcerator (X-58 NYX Legendary Blueprint)", "The Warden drop / Kang's Arms Incinerator", [GR_BOSS, SG], True),
    ("Widow Maker (Warlord Blueprint)", "Iskra drop (rare) / Control Room", [CQB, SG], True),
    ("Incisor (MAR-9)", "Gorani's Scout Overlook", [SG], False),
    ("Chemical Reaction (Kastov 762)", "The Chemist's Secure Armory (Game Rant instead lists an Oris 8.6 blueprint from The Chemist)", [SG], False),
    ("Paektu (Hyeon Burst)", "Jang-ui's Converted Power Room", [SG], False),
    ("Dreadnought (Type 73)", "Supreme Leader's Bunker (Bale)", [SG], False),
    ("Revenant (Oris 8.6)", "Scavenger drop", [SG], False),
    ("Rezi 12 Legendary Blueprint", "Knuckle/Tae-Hyun or Blix (X01)", [GR_BOSS], False),
    ("Type 73 Legendary Blueprint (X01)", "The Wrench / Chol-Min (X01)", [GR_BOSS], False),
    ("Secret Ghost Cutscene", "Complete all DMZ Orders", [GR_ORD], False),
]:
    item("cosmetics", t, "", req, "", "", c, src)

# ---------------------------------------------------------------- Achievements
cat("achievements", "Achievements & Trophies", None,
    "No DMZ-tied achievements found: sources report MW4's list (16-18 entries) as campaign-only.")
item("achievements", "No DMZ achievements/trophies", "Sources state the MW4 trophy list is campaign-only; nothing is tied to DMZ.", "", "", "", True, [POWERPYX, CODW_ACH, CM])

# ---------------------------------------------------------------- Validate & write
slugs = [c["slug"] for c in categories]
assert len(slugs) == len(set(slugs))
seen = set()
for c in categories:
    assert c["parent"] is None or c["parent"] in seen, c
    seen.add(c["slug"])
for i in items:
    assert i["category"] in seen, i
data = {"generated": "2026-11-17", "categories": categories, "items": items}
with open(OUT, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
from collections import Counter
cnt = Counter(i["category"] for i in items)
for c in categories:
    print(c["slug"], cnt.get(c["slug"], 0))
print("TOTAL", len(items), "confirmed", sum(i["confirmed"] for i in items))
