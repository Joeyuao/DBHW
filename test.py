import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 示例：生成密码的 SHA-256 哈希值
print(hash_password("t123"))  # 教师密码
print(hash_password("s123"))  # 学生密码
print(hash_password("a123"))  # 管理员密码
# f6b6d0d62eb661c6d3fd7e35e972a8ed44b4aa2fd6c87b449b82b1b7b1a2319f
# a9dcdc7159d1a9daae0ccc718f5dbc2bb1c61e38873abc8074b374473d4d00b9
# 7c04837eb356565e28bb14e5a1dedb240a5ac2561f8ed318c54a279fb6a9665e
print(type(hash_password("t123")))