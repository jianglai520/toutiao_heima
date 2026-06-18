"""
导入SQL文件到MySQL数据库
"""
import subprocess
import sys
import getpass


def run_mysql(extra_args, input_sql=None):
    """
    执行MySQL命令，自动处理密码输入
    """
    mysql_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
    password = getpass.getpass("请输入MySQL密码: ")
    
    cmd = [mysql_path, "-u", "root", f"-p{password}"] + extra_args
    
    result = subprocess.run(
        cmd,
        input=input_sql,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    return result


def import_sql():
    """导入SQL文件"""
    sql_file = "database.sql"
    database = "news_app"
    
    try:
        # 第一步：删除并重建数据库
        print("🔄 正在删除并重建数据库...")
        result = run_mysql(
            ["-e", f"DROP DATABASE IF EXISTS {database}; CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"]
        )
        
        if result.returncode != 0:
            print(f"❌ 数据库重建失败!\n{result.stderr}")
            return False
        print("✅ 数据库重建成功!")
        
        # 第二步：读取SQL文件
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 移除SQL文件中的CREATE DATABASE和USE语句（避免干扰）
        import re
        sql_content = re.sub(
            r"CREATE DATABASE IF NOT EXISTS \S+.*?;\s*", "", sql_content
        )
        sql_content = re.sub(
            r"USE \S+;\s*", "", sql_content
        )
        
        # 在SQL内容前后添加禁用/启用外键检查的语句
        sql_with_fk_check = (
            "SET FOREIGN_KEY_CHECKS = 0;\n"
            + sql_content +
            "\nSET FOREIGN_KEY_CHECKS = 1;\n"
        )
        
        # 第三步：导入SQL文件
        print("📥 正在导入SQL文件...")
        result = run_mysql(
            [f"--default-character-set=utf8mb4", database],
            input_sql=sql_with_fk_check
        )
        
        if result.returncode != 0:
            print(f"❌ 导入失败!\n{result.stderr}")
            return False
        
        print("✅ SQL文件导入成功!")
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("开始导入SQL文件...")
    print("=" * 50)
    success = import_sql()
    if success:
        print("🎉 完成！数据库已成功初始化!")
    else:
        print("⚠️  请检查错误信息")
