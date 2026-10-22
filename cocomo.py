"""Basic COCOMO estimation for the Library Management System."""

MODES = {
    # mode: (a, b, c, d)
    "Organic": (2.4, 1.05, 2.5, 0.38),
    "Semi-detached": (3.0, 1.12, 2.5, 0.35),
    "Embedded": (3.6, 1.20, 2.5, 0.32),
}


def cocomo(kloc, mode):
    a, b, c, d = MODES[mode]
    effort = a * kloc ** b          # person-months
    time = c * effort ** d          # months
    staff = effort / time           # people
    return effort, time, staff


if __name__ == "__main__":
    kloc = 10
    print(f"Project size: {kloc} KLOC\n")
    print(f"{'Mode':<15}{'Effort (PM)':>13}{'Time (months)':>15}{'Team size':>11}")
    for mode in MODES:
        e, t, s = cocomo(kloc, mode)
        print(f"{mode:<15}{e:>13.2f}{t:>15.2f}{s:>11.2f}")
