# Unit Converter 📐
# Concepts: Nested Dicts, Functions, Lambda, Type Handling, Formatted Output

# ── Conversion Tables ─────────────────────────────────────────
# All units stored relative to a base unit (multiply to convert TO base)
LENGTH = {
    "Kilometer"  : 1000,
    "Meter"      : 1,
    "Centimeter" : 0.01,
    "Millimeter" : 0.001,
    "Mile"       : 1609.344,
    "Yard"       : 0.9144,
    "Foot"       : 0.3048,
    "Inch"       : 0.0254,
}

WEIGHT = {
    "Tonne"     : 1000,
    "Kilogram"  : 1,
    "Gram"      : 0.001,
    "Milligram" : 0.000001,
    "Pound"     : 0.453592,
    "Ounce"     : 0.028349,
}

AREA = {
    "Square Kilometer" : 1_000_000,
    "Square Meter"     : 1,
    "Square Centimeter": 0.0001,
    "Square Mile"      : 2_589_988.11,
    "Acre"             : 4046.856,
    "Hectare"          : 10_000,
    "Square Foot"      : 0.092903,
    "Square Inch"      : 0.00064516,
}

SPEED = {
    "Meters/second"    : 1,
    "Km/hour"          : 0.277778,
    "Miles/hour"       : 0.44704,
    "Knot"             : 0.514444,
    "Foot/second"      : 0.3048,
}

TEMPERATURE = "TEMPERATURE"   # handled separately — non-linear

CATEGORIES = {
    "1": ("📏  Length",      LENGTH),
    "2": ("⚖️  Weight/Mass", WEIGHT),
    "3": ("🌡️  Temperature",  TEMPERATURE),
    "4": ("🔲  Area",        AREA),
    "5": ("🚀  Speed",       SPEED),
}


# ── Temperature (special case — non-linear) ───────────────────
TEMP_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]

def convert_temperature(value, from_unit, to_unit):
    # First convert to Celsius
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value

    # Then convert Celsius to target
    if to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:
        return celsius


# ── Standard conversion (ratio-based) ────────────────────────
def convert_unit(value, from_unit, to_unit, table):
    base_value = value * table[from_unit]     # convert to base
    return base_value / table[to_unit]        # convert to target


# ── UI helpers ────────────────────────────────────────────────
def show_banner():
    print()
    print("  ╔════════════════════════════════════════╗")
    print("  ║        📐  UNIT  CONVERTER  📐         ║")
    print("  ╚════════════════════════════════════════╝")
    print()


def pick_category():
    print("  ┌────────────────────────────────────────┐")
    print("  │         Select Category:                │")
    print("  ├────────────────────────────────────────┤")
    for key, (label, _) in CATEGORIES.items():
        print(f"  │   {key}  ➜  {label:<34}│")
    print("  │   0  ➜  Exit                           │")
    print("  └────────────────────────────────────────┘")

    while True:
        choice = input("\n  👉  Select (0-5): ").strip()
        if choice == "0":
            return None, None
        if choice in CATEGORIES:
            label, table = CATEGORIES[choice]
            return label, table
        print("  ⚠️  Enter 0 to 5.")


def pick_unit(units, prompt):
    unit_list = list(units)
    for i, u in enumerate(unit_list, 1):
        print(f"    {i:>2})  {u}")
    while True:
        try:
            idx = int(input(f"  👉  {prompt}: ")) - 1
            if 0 <= idx < len(unit_list):
                return unit_list[idx]
            print(f"  ⚠️  Enter 1 to {len(unit_list)}.")
        except ValueError:
            print("  ⚠️  Enter a valid number.")


def get_value(from_unit):
    while True:
        try:
            val = float(input(f"\n  💡  Enter value in {from_unit}: ").strip())
            return val
        except ValueError:
            print("  ⚠️  Enter a valid number.")


def do_conversion(label, table):
    print(f"\n  ── {label} ──────────────────────────────")

    is_temp = (table == TEMPERATURE)
    units   = TEMP_UNITS if is_temp else list(table.keys())

    print("\n  From unit:")
    from_unit = pick_unit(units, "Select FROM unit")

    print("\n  To unit:")
    to_unit = pick_unit(units, "Select TO unit")

    value = get_value(from_unit)

    if is_temp:
        result = convert_temperature(value, from_unit, to_unit)
    else:
        result = convert_unit(value, from_unit, to_unit, table)

    # Smart formatting
    if abs(result) >= 1_000_000 or (abs(result) < 0.0001 and result != 0):
        result_str = f"{result:.6e}"
    elif result == int(result):
        result_str = f"{int(result):,}"
    else:
        result_str = f"{result:,.6f}".rstrip("0").rstrip(".")

    print()
    print("  ┌────────────────────────────────────────────────┐")
    print(f"  │  {value:>12g}  {from_unit:<16}")
    print(f"  │     =  {result_str:>12}  {to_unit:<16}")
    print("  └────────────────────────────────────────────────┘")
    print()


def main():
    show_banner()

    while True:
        label, table = pick_category()
        if label is None:
            print("\n  ════════════════════════════════════════")
            print("  📐  Goodbye! Keep converting! 👋\n")
            break

        do_conversion(label, table)

        again = input("  [Enter] ➜ Convert Again  |  [m] ➜ Main Menu\n  👉  ").strip().lower()
        if again != "m":
            # repeat same category
            continue
        print()


if __name__ == "__main__":
    main()
