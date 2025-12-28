# xACT — Action Composition Toolkit

> kz версия: [README.kz.md](README.kz.md)

> 🇷🇺 версия: [README.ru.md](README.ru.md)

Action-based robotics framework developed by **FTC Team “xCellence” #28300**.

xACT provides a simple and reliable way to build robot missions using **composable actions**
with **sequential and parallel execution**, without blocking code or complex state machines.

![](https://lh3.googleusercontent.com/pw/AP1GczOLE0Kpxbyx_1fXkmOTzH9ih937lW2BGf9cVE3qZZzHbBJl_omJeI8VTTCFN_YU8wNRqh55aTOvgKgmiLJ-2_ip0Kl2seVD7B4ByuaZvvL8bWYJoqXUP1YrLmh0S9WNEZvZsHYqrMdbxBhl1Kl8v233=w320-h320-s-no-gm?authuser=0)

---

## Core Idea

Everything in xACT is an **Action**.

Actions:
- are initialized once
- updated repeatedly
- finish by returning `True`

Actions can be composed into **sequences** and **parallel groups** to build clear
and maintainable mission logic.

![Action Lifecycle](https://lh3.googleusercontent.com/pw/AP1GczNqezDOXUzcrkP6RAvzna0RXF2N9e2q1V9_6PnwzLyzuhcGhiQMBvi_UczZpoN9oPHGJAd8JXL95QbWQJftHI1U3JlmdMnoDk-RHYN4v061Uzkz2ySRrm7GLgZOBDsALdtt2HxIXF2oHp-lJvXJQx0w=w1143-h406-s-no-gm?authuser=0)

---

## Scope

- Mission-level robot control
- Sequential and parallel behaviors
- Cooperative (non-blocking) execution
- Currently used with **SPIKE Prime / Pybricks**
- Primary application: **FLL Robot Game**

---

## Credits

**xACT — Action Composition Toolkit**  
Developed by **FTC Team “xCellence” #28300**

If you use this framework, please credit:  
*xACT by FTC Team “xCellence” #28300*
