from motor.motor_asyncio import AsyncIOMotorClient
import os
from decouple import config


# MongoDB 连接配置
DB_URL = config('DB_URL', cast=str)
DB_NAME = config('DB_NAME', cast=str)
COLLECTION_NAME = config('COLLECTION_NAME', cast=str)

client = AsyncIOMotorClient(DB_URL)
db = client[DB_NAME]
articles_collection = db[COLLECTION_NAME]

# 读取 Markdown 文件并提取标题和内容
async def process_markdown_file(filepath):
    if os.path.exists(filepath) and filepath.endswith('.md'):
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            title = ""
            content = ""
            for i, line in enumerate(lines):
                if line.startswith('# '):  # 找到标题
                    title = line.strip('# ').strip()
                    content = "".join(lines[i:])  # 剩余的内容作为文章内容
                    break

            if title and content:
                # 创建 slug (通常是标题的 URL 友好版本)
                slug = title.lower().replace(' ', '-')

                # 插入到 MongoDB
                document = {
                    'title': title,
                    'content': content,
                    'slug': slug
                    # MongoDB 会自动生成 '_id'
                }
                result = await articles_collection.insert_one(document)
                print(f'Inserted article with _id: {result.inserted_id}')
            else:
                print("No title found in the document.")
    else:
        print("File does not exist or is not a Markdown file.")

# 异步事件循环
# async def main():
#     print(os.getcwd())
#     await process_markdown_file('articles/03 Next.js.md')
    
# 处理一个目录中的所有 Markdown 文件
async def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('summary.md'):
            filepath = os.path.join(directory, filename)
            print(f'Processing {filepath}...')
            await process_markdown_file(filepath)

# 异步事件循环
async def main(directory):
    await process_directory(directory)
    
# 运行事件循环
if __name__ == "__main__":
    import asyncio
    articles_directory = 'articles'  # 替换为你的 Markdown 文件目录
    asyncio.run(main(articles_directory))