Explanation is discussion that clarifies and illuminates a 
particular topic. Explanation is understanding-oriented.

# Interface
Interface between GUI (at this time only kivy), and solver which
makes calculations. Thist interface separate GUI and solver.

## Data format

Python dictionary as input and output
example looks like:
```python
    {
        section: speaker,
        item: name,
        action: set,
        value: Visaton,
    }
```
where:  
- section: name of the solver module to work with  
- item: name of some value  
- action: set, get, answer, confirm, calculate, error  
- value: used for set, answer or error  
any additional value possible  
list of dictionaries are possible

## interface.py
file responsible for data change.
at this time only synchronously, but full asyn. in planned.

```mermaid
---
title: interface.py chart
---

flowchart TB
    start([start]) --> gd[/"ask():<br>get data from GUI"/]
    gd --> convey{"convey()"}
    convey -- version --> attr{"solver_attribute()"}
    convey -- name --> attr
    convey -- list quantities --> slq["solver_list_quantities()"]
    slq --> loq[list of quantities]
    loq --> ans
    convey -- list sections --> sls["solver_list_sections()"]
    sls --> lof[list of sections]
    lof --> ans
    convey -- file.ini --> sec["section():<br>set section"]
    sec --> rf["read_form_file()"]
    rf --> ans
    convey -- input dir --> id["TODO"]
    convey -- else --> attr
    attr -- get --> val([value])
    val --> ans
    attr -- set --> set[set value]
    set --> con[confirmation]
    con --> ans["update():<br>create answer"]
    ans --> stop([send answer])
```
