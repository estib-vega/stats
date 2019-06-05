from __future__ import division

values = """0.7421875
0.407407407407
0.90625
0.47641509434
0.991573033708
0.153846153846
0.314685314685
0.144981412639
0.489583333333
0.382284382284
0.614797864226
0.283582089552
0.61220043573
0.740157480315
0.410138248848
0.3779342723
0.280120481928
0.41134751773"""
total = 0

value_list = values.split('\n')

for val in value_list:
    num_val = float(val)
    total += num_val

average = total / len(value_list)
error_sum = 0

for val in value_list:
    error = abs(float(val) - average)
    error_sum += error

mean = error_sum / len(value_list)

print "average", average, "mean", mean