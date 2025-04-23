000  move 1 # acc = 1
001  move 3 # acc = 3
002  move 7 # acc = 7
003  move 15 # acc = 15
004  move 31 # acc = 31
005  move 63 # acc = 63
006  move 127 # acc = 127
007  move 255 # acc = 255
008  add 1 # acc = 0
009  add 3 # acc = 3
010  add 7 # acc = 7
011  add 15 # acc = 15
012  add 31 # acc = 31
013  add 63 # acc = 63
014  add 127 # acc = 127
015  add 255 # acc = 127
016  sub 1 # acc = 127
017  sub 3 # acc = 127
018  sub 7 # acc = 127
019  sub 15 # acc = 127
020  sub 31 # acc = 127
021  sub 63 # acc = 127
022  sub 127 # acc = 127
023  sub 255 # acc = 127
024  and 255 # acc = 127
025  and 127 # acc = 127
026  and 63 # acc = 127
027  and 31 # acc = 127
028  and 15 # acc = 127
029  and 7 # acc = 127
030  and 3 # acc = 127
031  and 1 # acc = 127
032  move 1 # acc = 127
033  store 87 # acc = 127
034  move 3 # acc = 127
035  store 88 # acc = 127
036  move 7 # acc = 127
037  store 89 # acc = 127
038  move 15 # acc = 127
039  store 90 # acc = 127
040  move 31 # acc = 127
041  store 91 # acc = 127
042  move 63 # acc = 127
043  store 92 # acc = 127
044  move 127 # acc = 127
045  store 93 # acc = 127
046  move 255 # acc = 127
047  store 94 # acc = 127
048  load 87 # acc = 127
049  load 88 # acc = 127
050  load 89 # acc = 127
051  load 90 # acc = 127
052  load 91 # acc = 127
053  load 92 # acc = 127
054  load 93 # acc = 127
055  load 94 # acc = 127
056  addm 87 # acc = 127
057  addm 88 # acc = 127
058  addm 89 # acc = 127
059  addm 90 # acc = 127
060  addm 91 # acc = 127
061  addm 92 # acc = 127
062  addm 93 # acc = 127
063  addm 94 # acc = 127
064  subm 87 # acc = 127
065  subm 88 # acc = 127
066  subm 89 # acc = 127
067  subm 90 # acc = 127
068  subm 91 # acc = 127
069  subm 92 # acc = 127
070  subm 93 # acc = 127
071  subm 94 # acc = 127
072  and 0 # acc = 0
073  jumpz 75 # taken
074  move 255 # set acc to 255 if error
075  add 1 # acc = 1
076  jumpnz 78 # taken
077  move 255 # set acc to 255 if error
078  and 0 # acc = 0
079  jumpnz 81 # false
080  jumpu 82 # unconditional jump
081  move 255 # set acc to 255 if error
082  add 1 # acc = 1
083  jumpz 85 # false
084  jumpu 86 # unconditional jump
085  move 255 # set acc to 255 if error
086  jumpu 0 # jump back to 0
087  .data 0
088  .data 0
089  .data 0
090  .data 0
091  .data 0
092  .data 0
093  .data 0
094  .data 0
