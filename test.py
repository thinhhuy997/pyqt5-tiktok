dict_a = {"abc": 123, "xyz": 456}
dict_b = {"abc": 789}

dup_keys = set(dict_a.keys()).intersection(set(dict_b.keys()))

for dup_key in dup_keys:
    dict_b.pop(dup_key)

dict_a.update(dict_b)

print(dict_a)