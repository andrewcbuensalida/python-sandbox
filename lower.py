job_title = 'Data Scientist'

black_list = ['dataa', 'scientista']

result = any(b_word in job_title.lower() for b_word in map(str.lower,black_list))

print(result)