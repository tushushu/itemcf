"""
@Author: tushushu
@Date: 2019-10-08 17:04:30
"""


"""
for post in newpost:
    value = newpost_beta.get(post[0], pre_value)
    value_arr = value.split("_")
    if len(value_arr) == 2:
        alpha = int(value_arr[0])
        beta = int(value_arr[1])
        score = np.random.beta(alpha, beta)
        ret_beta.append([post, score, value])
ret_sort = heapq.nlargest(len(ret_beta), ret_beta, key=lambda x: x[1])
"""