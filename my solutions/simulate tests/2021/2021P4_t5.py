'''
Here is my understanding to this problem.

For each day, we define the following tables:
    1. Subway_route = [station1, station2, station3, ..., stationN] by order at which the train arrives.
    2. Time_subway_arrive[stationID] = the time at which the subway arrives at this station.
    
Now we can draw an important conclusion:
    If we can get (using walways) from start to any stationX in time t <= time_subway_arrive[stationX], we are definately able to get to any station after stationN in t=time_subway_arrive[stationID], including the end.

Based on the conclusion, there are four methods we can get to destination:
    1. start -> walways -> end
    2. start -> subway -> end
    3. start -> subway -> walways -> end
    4. start -> walways -> subway -> walways -> end
NOTE that any other moves that jumps between subway and walways, such as "start -> subway -> walways -> subway -> end" will be completely meaningless.
Because according to the conclusion, it will always take time_subway_arrive[stationID] much time to get to a station by subway.

So we can solve the problem by:
(Preparation)
    1. Using the dijkastra's algorithm, compute station_to_destination_time_walways[stationID] = the time needed to get from a station to stationN, using walkways only.
    2. Using the dijkastra's, compute start_to_station_walkways[stationID] = time needed to get from station0 to stationID, using walways only.
(Solution)
    3. For each day, compute subway_route and time_subway_arrive. 
        NOTE that we don't need to walk through all stations, just swap the two station.
    4. Create a variable called catch_subway_time for the minimum amount of time needed to get on the train.
        For any station i, if start_to_station_walkways[i] <= time_subway_arrive[i], catch_subway_time will be AT MOST time_subway_arrive[i] because we can catch the train at that station.
        NOTE that we don't need to look at all the stations, just look at the stations of which their subway arrival time are beeing swaped
    5. Now it will be very easy to compute the time needed to get from start to destination (we define as time_arrival), based on the travel method we use:
        (1: start -> walways -> end) time_arrival = start_to_station_walkways[0]
        (2: start -> subway -> end) time_arrival = time_subway_arrive[n]
        (3: start -> subway -> walways -> end) or (4: start -> walways -> subway -> walways -> end), we let stationT be the station at which you transfer from subway to walways
            time_arrival = time_subway_arrive[stationT] + station_to_destination_time_walways[stationT]
'''


import sys
# sys.setrecursionlimit(99999) # because who gives a

n, w, d = map(int, input().split())

walways = {}  # stores the walways, walways[stationX] = [station1, station2, ...], stations that stationX connects to
walways_reversed = {} # stores the walways, but reversed, walways_reversed[stationX] = [station1, station2, ...], stations that connects to stationX
for i in range(w): # input the walways
    start, end = map(int, input().split())
    # we change every point to 0~n-1
    start -= 1
    end -= 1
    # add them to the table
    if start in walways:
       walways[start].append(end) 
    else:
       walways[start] = [end]
    if end in walways_reversed:
       walways_reversed[end].append(start)
    else:
       walways_reversed[end] = [start]



# run the dijkastra's to find the time needed to get from a station to stationN, using walkways only
'''
test data:
200 199 200
1 2
2 3
3 4
4 5
5 6
6 7
7 8
8 9
9 10
10 11
11 12
12 13
13 14
14 15
15 16
16 17
17 18
18 19
19 20
20 21
21 22
22 23
23 24
24 25
25 26
26 27
27 28
28 29
29 30
30 31
31 32
32 33
33 34
34 35
35 36
36 37
37 38
38 39
39 40
40 41
41 42
42 43
43 44
44 45
45 46
46 47
47 48
48 49
49 50
50 51
51 52
52 53
53 54
54 55
55 56
56 57
57 58
58 59
59 60
60 61
61 62
62 63
63 64
64 65
65 66
66 67
67 68
68 69
69 70
70 71
71 72
72 73
73 74
74 75
75 76
76 77
77 78
78 79
79 80
80 81
81 82
82 83
83 84
84 85
85 86
86 87
87 88
88 89
89 90
90 91
91 92
92 93
93 94
94 95
95 96
96 97
97 98
98 99
99 100
100 101
101 102
102 103
103 104
104 105
105 106
106 107
107 108
108 109
109 110
110 111
111 112
112 113
113 114
114 115
115 116
116 117
117 118
118 119
119 120
120 121
121 122
122 123
123 124
124 125
125 126
126 127
127 128
128 129
129 130
130 131
131 132
132 133
133 134
134 135
135 136
136 137
137 138
138 139
139 140
140 141
141 142
142 143
143 144
144 145
145 146
146 147
147 148
148 149
149 150
150 151
151 152
152 153
153 154
154 155
155 156
156 157
157 158
158 159
159 160
160 161
161 162
162 163
163 164
164 165
165 166
166 167
167 168
168 169
169 170
170 171
171 172
172 173
173 174
174 175
175 176
176 177
177 178
178 179
179 180
180 181
181 182
182 183
183 184
184 185
185 186
186 187
187 188
188 189
189 190
190 191
191 192
192 193
193 194
194 195
195 196
196 197
197 198
198 199
199 200
'''

station_to_destination_time_walkways = dict()
for i in range(n-1):
   station_to_destination_time_walkways[i] = float("inf")
station_to_destination_time_walkways[n-1] = 0
visited_stations = set([n-1]) # start from station n
flag = True
while flag:
    flag = False
    for walkway_end in visited_stations:
        if walkway_end not in walways_reversed:
            continue
        for walkway_start in walways_reversed[walkway_end]:
            if station_to_destination_time_walkways[walkway_start] > station_to_destination_time_walkways[walkway_end]+1:
                station_to_destination_time_walkways[walkway_start] = station_to_destination_time_walkways[walkway_end]+1
                flag = True 
                break
        if flag:
            break
    if flag:
        visited_stations.add(walkway_start)

sta