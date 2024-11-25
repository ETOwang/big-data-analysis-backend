from flask import Blueprint, request, jsonify
from app.models import Paper

search_papers = Blueprint('search_papers', __name__)

# 论文搜索接口
@search_papers.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    page = int(request.args.get('page', 1))
    per_page = 10  # 每页显示 10 条记录

    # 搜索数据库中包含 query 的论文标题或关键词
    papers = Paper.query.filter(
        Paper.title.contains(query) | Paper.keywords.contains(query)
    ).paginate(page, per_page, False)

    # 结果转换成字典格式，准备返回给前端
    results = [{
        'id': paper.id,
        'title': paper.title,
        'author': paper.author,
        'keywords': paper.keywords,
        'published_date': paper.published_date.strftime('%Y-%m-%d')
    } for paper in papers.items]

    return jsonify({
        'papers': results,
        'total': papers.total,
        'pages': papers.pages,
        'page': page
    })


