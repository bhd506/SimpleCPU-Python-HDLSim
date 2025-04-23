###################
# INSTRUCTION-SET #
###################

# INSTR   IR15 IR14 IR13 IR12 IR11 IR10 IR09 IR08 IR07 IR06 IR05 IR04 IR03 IR02 IR01 IR00
# MOVE    0    0    0    0    X    X    X    X    K    K    K    K    K    K    K    K
# ADD     0    0    0    1    X    X    X    X    K    K    K    K    K    K    K    K
# SUB     0    0    1    0    X    X    X    X    K    K    K    K    K    K    K    K
# AND     0    0    1    1    X    X    X    X    K    K    K    K    K    K    K    K

# LOAD    0    1    0    0    X    X    X    X    A    A    A    A    A    A    A    A
# STORE   0    1    0    1    X    X    X    X    A    A    A    A    A    A    A    A
# ADDM    0    1    1    0    X    X    X    X    A    A    A    A    A    A    A    A
# SUBM    0    1    1    1    X    X    X    X    A    A    A    A    A    A    A    A

# JUMPU   1    0    0    0    X    X    X    X    A    A    A    A    A    A    A    A
# JUMPZ   1    0    0    1    X    X    X    X    A    A    A    A    A    A    A    A
# JUMPNZ  1    0    1    0    X    X    X    X    A    A    A    A    A    A    A    A
# JUMPC   1    0    1    1    X    X    X    X    A    A    A    A    A    A    A    A        -- NOT IMPLEMENTED

########
# CODE #
########

start:
  move 1            # acc = 1
  move 3            # acc = 3
  move 7            # acc = 7
  move 15           # acc = 15
  move 31           # acc = 31
  move 63           # acc = 63
  move 127          # acc = 127
  move 255          # acc = 255

  add 1             # acc = 0
  add 3             # acc = 3
  add 7             # acc = 7 
  add 15            # acc = 15
  add 31            # acc = 31
  add 63            # acc = 63
  add 127           # acc = 127
  add 255           # acc = 127

  sub 1             # acc = 127
  sub 3             # acc = 127
  sub 7             # acc = 127
  sub 15            # acc = 127
  sub 31            # acc = 127
  sub 63            # acc = 127
  sub 127           # acc = 127
  sub 255           # acc = 127

  and 255           # acc = 127
  and 127           # acc = 127
  and 63            # acc = 127
  and 31            # acc = 127
  and 15            # acc = 127
  and 7             # acc = 127
  and 3             # acc = 127
  and 1             # acc = 127

  move 1            # acc = 127
  store A           # acc = 127
  move 3            # acc = 127
  store B           # acc = 127
  move 7            # acc = 127
  store C           # acc = 127
  move 15           # acc = 127
  store D           # acc = 127
  move 31           # acc = 127
  store E           # acc = 127
  move 63           # acc = 127
  store F           # acc = 127
  move 127          # acc = 127         
  store G           # acc = 127
  move 255          # acc = 127
  store H           # acc = 127

  load A            # acc = 127
  load B            # acc = 127
  load C            # acc = 127
  load D            # acc = 127
  load E            # acc = 127
  load F            # acc = 127
  load G            # acc = 127
  load H            # acc = 127

  addm A            # acc = 127
  addm B            # acc = 127
  addm C            # acc = 127
  addm D            # acc = 127
  addm E            # acc = 127
  addm F            # acc = 127
  addm G            # acc = 127
  addm H            # acc = 127

  subm A            # acc = 127
  subm B            # acc = 127
  subm C            # acc = 127
  subm D            # acc = 127
  subm E            # acc = 127
  subm F            # acc = 127
  subm G            # acc = 127
  subm H            # acc = 127

  and 0             # acc = 0
  jumpz b1          # TAKEN
  move 255          # set acc to 255 if error

b1:
  add 1             # acc = 1
  jumpnz b2         # TAKEN
  move 255          # set acc to 255 if error

b2:
  and 0             # acc = 0
  jumpnz b3         # FALSE
  jumpu b4          # unconditional jump
b3:
  move 255          # set acc to 255 if error

b4:
  add 1             # acc = 1
  jumpz b5          # FALSE
  jumpu b6          # unconditional jump
b5:
  move 255          # set acc to 255 if error

b6:
  jumpu start       # jump back to start

A:
  .data 0
B:
  .data 0
C:
  .data 0
D:
  .data 0
E:
  .data 0
F:
  .data 0
G:
  .data 0
H:
  .data 0




  
